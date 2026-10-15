""" Management command for finding (and optionally deleting) abandoned sign-ups.

    A user is considered abandoned if all of the following are true:
    - they have no verified email address
    - they have never logged in
    - they joined more than --older-than-days days ago (and after --joined-after, if given)
    - they are not linked to a member
    - they are not staff or a superuser

    Usage:
    python manage.py purge_unverified_users

    Optional arguments:
    --older-than-days <n> : Only include users who joined more than n days ago. Defaults to 7.
    --joined-after <YYYY-MM-DD> : Only include users who joined on or after this date.
    --delete : Delete the matching users. Without this flag the users are only listed.
"""

from datetime import datetime, timedelta

from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from core.models import CshcUser


class Command(BaseCommand):
    help = (
        "Lists users who never verified their email address or logged in, "
        "optionally deleting them."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--older-than-days',
            dest='older_than_days',
            type=int,
            default=7,
            help='Only include users who joined more than this many days ago. Defaults to 7.',
        )
        parser.add_argument(
            '--joined-after',
            dest='joined_after',
            help='Only include users who joined on or after this date (YYYY-MM-DD).',
        )
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Delete the matching users. Without this flag the users are only listed.',
        )

    def handle(self, *args, **options):
        older_than_days = options['older_than_days']
        delete = options['delete']
        if older_than_days < 0:
            raise CommandError('--older-than-days cannot be negative')

        joined_after = None
        if options['joined_after']:
            try:
                joined_after = timezone.make_aware(datetime.strptime(options['joined_after'], '%Y-%m-%d'))
            except ValueError:
                raise CommandError('--joined-after must be a date in the format YYYY-MM-DD')

        users = list(self.get_abandoned_users(older_than_days, joined_after))

        joined_after_suffix = ' and on or after {}'.format(options['joined_after']) if joined_after else ''
        self.stdout.write(
            'Found {} unverified, never-logged-in users who joined more than {} days ago{}.'.format(
                len(users),
                older_than_days,
                joined_after_suffix,
            )
        )
        for user in users:
            self.stdout.write('  {}'.format(self.format_user(user)))

        if not users:
            return

        if delete:
            deleted_count = CshcUser.objects.filter(pk__in=[user.pk for user in users]).delete()[0]
            self.stdout.write('Deleted {} objects (users and related records).'.format(deleted_count))
        else:
            self.stdout.write('No users deleted. Re-run with --delete to remove them.')

    def get_abandoned_users(self, older_than_days, joined_after=None):
        cutoff = timezone.now() - timedelta(days=older_than_days)
        verified_user_ids = EmailAddress.objects.filter(verified=True).values_list('user_id', flat=True)

        users = CshcUser.objects.filter(
            last_login__isnull=True,
            date_joined__lt=cutoff,
            member__isnull=True,
            is_staff=False,
            is_superuser=False,
        ).exclude(
            pk__in=verified_user_ids,
        )
        if joined_after is not None:
            users = users.filter(date_joined__gte=joined_after)

        return users.order_by('date_joined')

    def format_user(self, user):
        return 'id={} {} <{}> joined {}'.format(
            user.pk,
            user.get_full_name() or '-',
            user.email,
            user.date_joined.strftime('%Y-%m-%d %H:%M'),
        )
