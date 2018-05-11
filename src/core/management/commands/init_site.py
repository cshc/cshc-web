import traceback
import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.core.management import call_command
from allauth.socialaccount.models import SocialApp

social_apps = [
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
    help = "One-time (idempotent) initialization of the Sites data"

    def add_arguments(self, parser):
        parser.add_argument(
            'domain', help='The site domain')
        parser.add_argument(
            'blog_entries_file', help='The CSV dump of Zinnia blog entries')

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **options):
        # Update the default/first site object with the correct name and domain (provided on the command line)
        print('Updating default site object')
        try:
            site = Site.objects.get(id=1)
            site.name = 'CSHC'
            site.domain = options['domain']
            site.save()
        except Site.DoesNotExist:
            traceback.print_exc()

        # Add SocialApps
        for app in social_apps:
            app_obj, created = SocialApp.objects.get_or_create(
                name=app['name'], defaults=app)
            if created:
                print('Added SocialApp ' + app['name'])
            else:
                print('SocialApp ' + app['name'] + ' already exists')
            if app_obj.sites.count() == 0:
                app_obj.sites.add(site)
                app_obj.save()

        # Add fixtures
        call_command('loaddata', 'fixtures/documents.json',
                     'fixtures/offers.json', 'fixtures/flatpages.json')

        # Initialize file-based database data
        call_command('init_data')

        # Migrate the saved blog entry data
        call_command('migrate_blog_entries', options['blog_entries_file'])
