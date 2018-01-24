"""
Management command that copies the media folder (uploads etc) from the production
Amazon S3 bucket to one or more of the following destinations:
1: --staging: the new staging media Amazon S3 bucket.
2. --new-prod: the new production media Amazon S3 bucket.
3. --local: the local media folder (in your dev environment)

Note that all copied files will have the ACL 'public-read'
"""

import os
import traceback
import boto3
from django.core.management.base import BaseCommand

OLD_PROD_BUCKET_NAME = 'cshc'
NEW_PROD_BUCKET_NAME = 'cshc-v3'
NEW_STAGING_BUCKET_NAME = 'cshc-staging-v3'

extra_args = {'ACL': 'public-read'}


class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()

    def add_arguments(self, parser):
        parser.add_argument(
            '--local',
            action='store_true',
            dest='local',
            default=False,
            help='Copy to the local media folder as well',
        )
        parser.add_argument(
            '--new-prod',
            action='store_true',
            dest='new_prod',
            default=False,
            help='Copy to the new production media folder as well',
        )
        parser.add_argument(
            '--staging',
            action='store_true',
            dest='staging',
            default=False,
            help='Copy to the new staging media folder as well',
        )

    def handle(self, *args, **options):
        try:
            s3 = boto3.resource('s3')
            old_prod_bucket = s3.Bucket(OLD_PROD_BUCKET_NAME)
            new_staging_bucket = s3.Bucket(NEW_STAGING_BUCKET_NAME)
            new_prod_bucket = s3.Bucket(NEW_PROD_BUCKET_NAME)
            for obj_summary in old_prod_bucket.objects.filter(Prefix='media'):
                copy_source = {
                    'Bucket': OLD_PROD_BUCKET_NAME,
                    'Key': obj_summary.key,
                }
                print('Copying ' + obj_summary.key)

                if options['new_prod']:
                    new_prod_bucket.copy(
                        copy_source, obj_summary.key, ExtraArgs=extra_args)

                if options['staging']:
                    new_staging_bucket.copy(
                        copy_source, obj_summary.key, ExtraArgs=extra_args)

                if options['local'] and not obj_summary.key.endswith('/'):
                    if not os.path.isfile(obj_summary.key):
                        os.makedirs(os.path.dirname(
                            obj_summary.key), exist_ok=True)
                        old_prod_bucket.download_file(
                            obj_summary.key, obj_summary.key)
        except:
            traceback.print_exc()
