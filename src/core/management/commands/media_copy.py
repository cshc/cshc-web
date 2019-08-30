"""
Management command that copies the media folder (uploads etc) from the production
Amazon S3 bucket to one or more of the following destinations:
1: --staging: the staging media Amazon S3 bucket.
2. --local: the local media folder (in your dev environment)

Note that all copied files will have the ACL 'public-read'
"""

import os
import traceback
import boto3
from django.core.management.base import BaseCommand

PROD_BUCKET_NAME = 'cshc-v3'
STAGING_BUCKET_NAME = 'cshc-staging-v3'

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

    def handle(self, *args, **options):
        try:
            s3 = boto3.resource('s3')
            prod_bucket = s3.Bucket(PROD_BUCKET_NAME)
            staging_bucket = s3.Bucket(STAGING_BUCKET_NAME)
            new_objects = {}

            if staging_bucket:
                new_objects = dict(
                    ((elt.key, elt.size), elt.last_modified)
                    for elt in staging_bucket.objects.filter(Prefix='media')
                )

            for obj_summary in prod_bucket.objects.filter(Prefix='media'):
                copy_source = {
                    'Bucket': PROD_BUCKET_NAME,
                    'Key': obj_summary.key,
                }

                if staging_bucket:
                    ts = new_objects.get((obj_summary.key, obj_summary.size))
                    if ts is not None and ts >= obj_summary.last_modified:
                        print('Skipping {}'.format(obj_summary.key))
                        continue

                print('Copying {}'.format(obj_summary.key))

                if staging_bucket:
                    staging_bucket.copy(
                        copy_source,
                        obj_summary.key,
                        ExtraArgs=extra_args,
                    )

                if options['local'] and not obj_summary.key.endswith('/'):
                    if not os.path.isfile(obj_summary.key):
                        os.makedirs(os.path.dirname(
                            obj_summary.key), exist_ok=True)
                        prod_bucket.download_file(
                            obj_summary.key, obj_summary.key)
        except:
            traceback.print_exc()
