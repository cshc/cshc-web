"""
Takes all existing CshcUser entries and creates an EmailAddress entry for each with
the email address verified and set as primary.

This script should be run once before going live (although it is idempotent).
That way existing users will not have to verify their email address when they
first log into the new site.

Usage:
python manage.py init_emailaddresses

"""

import traceback
from django.core.management.base import BaseCommand
from core.models import CshcUser
from allauth.account.models import EmailAddress


class Command(BaseCommand):
    """Management Command for one-time initialization of email addresses from users"""

    help = "One-time initialization of email addresses from users"

    def handle(self, *args, **options):
        defaults = {
            'verified': True,
        }
        try:
            for user in CshcUser.objects.all():
                email_address, created = EmailAddress.objects.get_or_create(
                    user=user, email=user.email, defaults=defaults)
                email_address.set_as_primary()
                print('{} email address {} for user {}'.format(
                    'Added' if created else 'Updated', user.email, user.get_full_name()))
        except Exception:
            traceback.print_exc()
