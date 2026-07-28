"""
Management command that copies the latest database dump from the production
Amazon S3 bucket to the local file system and converts it to SQLite3 format
for development purposes.
"""

import os
import subprocess
import traceback
import boto3
from django.core.management.base import BaseCommand

PROD_BUCKET_NAME  = 'cshc-v3'                                   # Production S3 bucket name
DB_BACKUP_PATH    = 'backups/db-backups/'                       # Path in the S3 bucket where database dumps are stored
DB_DUMP_EXTENSION = '.dump'                                     # Extension of the database dump files
DB_DUMP_PREFIX    = 'default-cambridgesouthhockeyclub.co.uk-'   # Prefix of the database dump files

class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **options):
        try:
            s3 = boto3.resource('s3')
            prod_bucket = s3.Bucket(PROD_BUCKET_NAME)
            dump_objects = []

            # Find all backup files in the backup path
            for obj_summary in prod_bucket.objects.filter(Prefix=DB_BACKUP_PATH):
                if obj_summary.key.endswith(DB_DUMP_EXTENSION) and obj_summary.key.startswith(DB_BACKUP_PATH + DB_DUMP_PREFIX):
                    dump_objects.append(obj_summary)

            if not dump_objects:
                print('No dump files found')
                return

            # Sort by last_modified to get the latest dump
            latest_dump = sorted(dump_objects, key=lambda x: x.last_modified, reverse=True)[0]
            print('Latest dump file: {}'.format(latest_dump.key))

            # Download the latest dump file
            local_filename = os.path.basename(latest_dump.key)
                       
            if os.path.isfile(local_filename):
                print('File already exists locally: {}'.format(local_filename))
            else:
                print('Downloading {} ...'.format(latest_dump.key))
                prod_bucket.download_file(latest_dump.key, local_filename)
                print('Download complete.')

            # Use mysql2sqlite to convert the dump to SQLite format
            print('Converting dump file to SQLite3 format (this takes a while) ...')
            
            try:
                # Run mysql2sqlite and pipe to sqlite3
                with open('db.sqlite3', 'w') as db_file:
                    mysql2sqlite = subprocess.Popen(
                        ['mysql2sqlite', local_filename],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    sqlite3 = subprocess.Popen(
                        ['sqlite3', 'db.sqlite3'],
                        stdin=mysql2sqlite.stdout,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    mysql2sqlite.stdout.close()
                    
                    stdout, stderr = sqlite3.communicate()
                    
                    if sqlite3.returncode != 0:
                        print('Error converting database:')
                        print(stderr.decode())
                    else:
                        print('Conversion complete: db.sqlite3')
                        
            except FileNotFoundError:
                print('Error: mysql2sqlite command not found. Please install it first.')
            except Exception as e:
                print('Error during conversion: {}'.format(str(e)))

            # Remove the local dump file after successful conversion
            if os.path.isfile(local_filename):
                os.remove(local_filename)
                print('Removed dump file: {}'.format(local_filename))

        except:
            traceback.print_exc()
