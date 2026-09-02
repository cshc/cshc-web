""" Management command for validating current member records.

    Usage:
    python manage.py check_members

    Optional arguments:
    --inactive-seasons <n> : Report current members if they have been inactive for n full completed seasons.
    --include-never-played : Include current members who have never made an appearance.
    --email-to <address> : Override the report recipient for this run only.
    --no-email : Suppress sending email and only write output to the console.
"""

from collections import OrderedDict

from django.conf import settings
from django.core.mail import mail_admins, send_mail
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from competitions.models import Season
from matches.models import Appearance
from members.models import Member


class Command(BaseCommand):
    help = (
        "Checks current members for duplicate shirt numbers and prolonged inactivity, "
        "emailing website admins if any issues are found."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--inactive-seasons',
            dest='inactive_seasons',
            type=int,
            default=2,
            help=(
                "Number of full completed seasons of inactivity required before a member is reported. "
                "Defaults to 2."
            ),
        )
        parser.add_argument(
            '--no-email',
            action='store_true',
            dest='no_email',
            help='Suppress sending email and only write the validation report to the console.',
        )
        parser.add_argument(
            '--include-never-played',
            action='store_true',
            dest='include_never_played',
            help='Include current members who have never made an appearance in the stale-member report.',
        )
        parser.add_argument(
            '--email-to',
            dest='email_to',
            help='Override the recipient email address for this run only.',
        )

    def handle(self, *args, **options):
        inactive_seasons = options['inactive_seasons']
        no_email = options['no_email']
        include_never_played = options['include_never_played']
        email_to = options['email_to']
        if inactive_seasons < 1:
            raise CommandError('--inactive-seasons must be at least 1')
        if no_email and email_to:
            raise CommandError('--email-to cannot be used with --no-email')

        current_members = Member.objects.filter(is_current=True)
        duplicate_numbers = self.get_duplicate_shirt_numbers(current_members)
        activity_seasons = self.get_activity_seasons(inactive_seasons)
        inactive_members = self.get_inactive_members(
            current_members,
            activity_seasons,
            include_never_played=include_never_played,
        )

        self.write_console_summary(
            current_members.count(),
            duplicate_numbers,
            inactive_members,
            activity_seasons,
            include_never_played=include_never_played,
        )

        if duplicate_numbers or inactive_members:
            report = self.build_report(
                current_members.count(),
                inactive_seasons,
                activity_seasons,
                duplicate_numbers,
                inactive_members,
                include_never_played=include_never_played,
            )
            if no_email:
                self.stdout.write('Validation issues found. Email suppressed by --no-email.')
                self.stdout.write(report)
            elif email_to:
                send_mail(
                    'Member validation issues detected',
                    report,
                    settings.SERVER_EMAIL,
                    [email_to],
                )
                self.stdout.write('Validation report emailed to {}.'.format(email_to))
            else:
                mail_admins('Member validation issues detected', report)
                self.stdout.write('Validation report emailed to website admins.')
        else:
            self.stdout.write('No validation issues found. No email sent.')

    def get_duplicate_shirt_numbers(self, current_members):
        shirt_groups = OrderedDict()
        for member in current_members:
            shirt_number = (member.shirt_number or '').strip()
            if not shirt_number:
                continue
            group_key = (member.gender, shirt_number)
            shirt_groups.setdefault(group_key, []).append(member)

        return OrderedDict(
            (group_key, members)
            for group_key, members in sorted(shirt_groups.items(), key=self.shirt_group_sort_key)
            if len(members) > 1
        )

    def shirt_group_sort_key(self, item):
        gender, shirt_number = item[0]
        try:
            numeric_value = int(shirt_number)
            return (gender, 0, numeric_value, shirt_number)
        except ValueError:
            return (gender, 1, shirt_number)

    def get_activity_seasons(self, completed_season_count):
        seasons = []
        season = Season.current()

        while season is not None and len(seasons) < completed_season_count + 1:
            seasons.append(season)
            season = Season.objects.previous(season)

        return seasons

    def get_inactive_members(self, current_members, activity_seasons, include_never_played=False):
        today = timezone.now().date()
        recent_member_ids = set(Appearance.objects.filter(
            member__is_current=True,
            match__season__in=activity_seasons,
            match__date__lte=today,
        ).values_list('member_id', flat=True).distinct())

        inactive_members = list(current_members.exclude(pk__in=recent_member_ids))
        if not inactive_members:
            return []

        last_appearance_by_member = {}
        appearances = Appearance.objects.filter(
            member__in=inactive_members,
            match__date__lte=today,
        ).select_related('member', 'match__season').order_by('member_id', '-match__season__start', '-match__date')

        for appearance in appearances:
            if appearance.member_id not in last_appearance_by_member:
                last_appearance_by_member[appearance.member_id] = appearance.match.season.slug

        members_with_last_appearance = [
            (member, last_appearance_by_member.get(member.pk))
            for member in inactive_members
        ]

        if include_never_played:
            return members_with_last_appearance

        return [
            (member, last_season)
            for member, last_season in members_with_last_appearance
            if last_season is not None
        ]

    def write_console_summary(
            self,
            member_count,
            duplicate_numbers,
            inactive_members,
            activity_seasons,
            include_never_played=False):
        self.stdout.write('Checked {} current members.'.format(member_count))

        if duplicate_numbers:
            self.stdout.write('Found {} duplicate shirt number assignments.'.format(len(duplicate_numbers)))
            for (gender, shirt_number), members in duplicate_numbers.items():
                self.stdout.write(
                    '  {} shirt {}: {}'.format(
                        gender,
                        shirt_number,
                        ', '.join(member.full_name() for member in members),
                    )
                )
        else:
            self.stdout.write('No duplicate shirt numbers found.')

        season_list = ', '.join(season.slug for season in activity_seasons)
        never_played_suffix = ' (including never-played members)' if include_never_played else ''
        if inactive_members:
            self.stdout.write(
                'Found {} inactive current members with no appearances in: {}{}.'.format(
                    len(inactive_members),
                    season_list,
                    never_played_suffix,
                )
            )
            for member, last_season in inactive_members:
                self.stdout.write(
                    '  {}'.format(self.format_inactive_member(member, last_season))
                )
        else:
            self.stdout.write(
                'No inactive current members found when checking seasons: {}{}.'.format(
                    season_list,
                    never_played_suffix,
                )
            )

    def build_report(
            self,
            member_count,
            inactive_seasons,
            activity_seasons,
            duplicate_numbers,
            inactive_members,
            include_never_played=False):
        lines = [
            'Member validation report',
            '',
            'Current members checked: {}'.format(member_count),
            'Inactive completed season threshold: {}'.format(inactive_seasons),
            'Seasons checked for recent activity: {}'.format(', '.join(season.slug for season in activity_seasons)),
            'Include never-played members: {}'.format('yes' if include_never_played else 'no'),
            '',
        ]

        if duplicate_numbers:
            lines.append('### Duplicate shirt numbers ###')
            lines.append('Action: investigate these duplicate shirt numbers and resolve any incorrect assignments.')
            lines.append('')
            for (gender, shirt_number), members in duplicate_numbers.items():
                lines.append(
                    '{} shirt {}: {}'.format(
                        gender,
                        shirt_number,
                        ', '.join(member.full_name() for member in members),
                    )
                )
            lines.append('')

        if inactive_members:
            lines.append('### Inactive current members ###')
            lines.append('Action: review these members and unset "current" for anyone who is no longer a current player.')
            lines.append('')
            for member, last_season in inactive_members:
                lines.append(self.format_inactive_member(member, last_season))

            lines.append('')

        return '\n'.join(lines)

    def format_inactive_member(self, member, last_season):
        return '{} (shirt: {}; last appearance: {})'.format(
            member.full_name(),
            (member.shirt_number or '').strip() or '-',
            last_season or 'never',
        )
