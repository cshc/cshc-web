"""
Initializes the database data

Usage:
python manage.py init_site

Options:
-b, --blog_entries_file         The CSV dump of Zinnia blog entries (default: './fixtures/zinnia_entry.csv')
-p, --prod_dump_sql             The SQL dump of data from the previous database (default: '/home/ec2-user/prod_dump.sql')

Positional Arguments:
domain                          The site domain (default: 'cshc-web-prod.eu-west-1.elasticbeanstalk.com')

"""

import traceback
import os
import stat
import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from django.core.management import call_command
from allauth.socialaccount.models import SocialApp


SOCIAL_APPS = [
    {
        'provider': 'facebook',
        'name': 'Facebook',
        'client_id': os.environ['SOCIALACCOUNT_FACEBOOK_CLIENT_ID'],
        'secret': os.environ['SOCIALACCOUNT_FACEBOOK_SECRET'],
    },
    {
        'provider': 'twitter',
        'name': 'Twitter',
        'client_id': os.environ['SOCIALACCOUNT_TWITTER_CLIENT_ID'],
        'secret': os.environ['SOCIALACCOUNT_TWITTER_SECRET'],
    },
    {
        'provider': 'google',
        'name': 'Google',
        'client_id': os.environ['SOCIALACCOUNT_GOOGLE_CLIENT_ID'],
        'secret': os.environ['SOCIALACCOUNT_GOOGLE_SECRET'],
    },
    {
        'provider': 'linkedin_oauth2',
        'name': 'LinkedIn',
        'client_id': os.environ['SOCIALACCOUNT_LINKEDIN_CLIENT_ID'],
        'secret': os.environ['SOCIALACCOUNT_LINKEDIN_SECRET'],
    },
]


class Command(BaseCommand):
    """Management Command for one-time initialization of the database data"""

    help = "One-time initialization of the database data"

    def add_arguments(self, parser):
        parser.add_argument(
            'domain',
            nargs='?',
            default='cshc-web-prod.eu-west-1.elasticbeanstalk.com',
            help='The site domain')
        parser.add_argument(
            '-b', '--blog_entries_file',
            dest='blog_entry_file',
            default='./fixtures/zinnia_entry.csv',
            help='The CSV dump of Zinnia blog entries')
        parser.add_argument(
            '-p', '--prod_dump_sql',
            dest='prod_dump_sql',
            default='/home/ec2-user/prod_dump.sql',
            help='The SQL dump of data from the previous database')

    def handle(self, *args, **options):
        # Sanity-check
        prod_dump_file = options.get('prod_dump_sql')
        if not os.path.isfile(prod_dump_file):
            raise CommandError('No prod dump file found at: ' + prod_dump_file)

        # 1. Flush the Database first
        print('Flushing DB tables')
        os.chmod('../deployment/flush_db.sh', stat.S_IXOTH)
        subprocess.call(['../deployment/flush_db.sh'])

        # 2. Migrate the saved blog entry data
        print('Migrating Zinnia blog entries')
        call_command('migrate_blog_entries', options['blog_entries_file'])

        # 3. Import the rest of the data from the previous database
        print('Importing data from previous database')
        os.chmod('../deployment/import_db.sh', stat.S_IXOTH)
        subprocess.call(['../deployment/import_db.sh', prod_dump_file])

        # 4. Update the default/first site object with the correct name and domain (provided on the command line)
        print('Updating default site object')
        try:
            site = Site.objects.get(id=1)
            site.name = 'CSHC'
            site.domain = options['domain']
            site.save()
        except Site.DoesNotExist:
            traceback.print_exc()

        # 5. Add SocialApps
        for app in SOCIAL_APPS:
            app_obj, created = SocialApp.objects.get_or_create(
                name=app['name'], defaults=app)
            if created:
                print('Added SocialApp ' + app['name'])
            else:
                print('SocialApp ' + app['name'] + ' already exists')
            if app_obj.sites.count() == 0:
                app_obj.sites.add(site)
                app_obj.save()

        # 6. Add fixtures
        call_command('loaddata', 'fixtures/documents.json',
                     'fixtures/offers.json', 'fixtures/flatpages.json')

        # 7. Initialize file-based database data
        call_command('init_data')
