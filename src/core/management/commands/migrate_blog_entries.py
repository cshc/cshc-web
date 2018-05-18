"""
One-time command for migrating zinnia blog entries from a CSV export of the old website's zinnia_entries table
into the new zinnia_entries table (which is incompatible so needs some custom migration logic).

This command is idempotent - it can be safely run multiple times without duplicating entries.
"""
import csv
import os.path
import traceback
from django.core.management.base import BaseCommand
from core.utils import get_aware_datetime
from zinnia.models import Entry


class Command(BaseCommand):
    help = "One-time migration of Zinnia blog entries from a CSV file into the zinnia_entries database"

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file', help='The CSV file to import blog entries from')
        parser.add_argument(
            '--sim',
            action='store_true',
            dest='sim',
            default=False,
            help='Simulation mode (database will not be written to)',
        )

    def parse_datetime(self, dt):
        return get_aware_datetime(dt) if dt != 'NULL' else None

    def handle(self, *args, **options):
        if not os.path.isfile(options['csv_file']):
            print("ERROR: No such file {}".format(options['csv_file']))
            return

        if not options['sim']:
            print('Deleting all Entry objects')
            Entry.objects.all().delete()

        count = 0
        with open(options['csv_file'], newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=';', escapechar='\\', strict=True)
            try:
                for row in reader:
                    entry, created = Entry.objects.get_or_create(
                        id=int(row['id']),
                        defaults={
                            'title': row['title'],
                            'status': int(row['status']),
                            'start_publication': self.parse_datetime(
                                row['start_publication']),
                            'end_publication': self.parse_datetime(
                                row['end_publication']),
                            'creation_date': self.parse_datetime(
                                row['creation_date']),
                            'last_update': self.parse_datetime(row['last_update']),
                            'publication_date': self.parse_datetime(
                                row['creation_date']),
                            'content': row['content'],
                            'comment_enabled': bool(int(row['comment_enabled'])),
                            'pingback_enabled': bool(int(row['pingback_enabled'])),
                            'trackback_enabled': bool(int(row['trackback_enabled'])),
                            'comment_count': int(row['comment_count']),
                            'pingback_count': int(row['pingback_count']),
                            'trackback_count': int(row['trackback_count']),
                            'excerpt': row['excerpt'],
                            'image': row['image'],
                            'featured': bool(int(row['featured'])),
                            'tags': row['tags'],
                            'login_required': bool(int(row['login_required'])),
                            'password': row['password'],
                            'content_template': row['content_template'],
                            'detail_template': row['detail_template'],
                            'image_caption': "",
                            'lead': "",
                            'slug': row['slug'],
                        }
                    )

                    if not options['sim']:
                        print('{} {}'.format(
                            'Saved' if created else 'Updated', entry.title))
                        entry.save()

                    count += 1
            except:
                traceback.print_exc()

            print('Saved {} blog entries'.format(count))
