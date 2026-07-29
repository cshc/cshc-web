""" Management command that updates opposition stats for all clubs or a specific club.

    Usage:
    python manage.py update_oppo_stats
    Optional arguments:
    --club <club_name> : Update stats only for a specific opposition club (e.g., "Newmarket").
"""

import logging
from django.core.management.base import BaseCommand
from competitions.models import Season
from opposition.stats import update_all_club_stats, update_club_stats_for_club
from opposition.models import Club

LOG = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Updates all opposition stats or stats for a specific club."

    def add_arguments(self, parser):
        """Adds command line arguments to the management command."""
        parser.add_argument(
            '--club',
            type=str,
            help='Optional: Update stats only for a specific opposition club (e.g., "Newmarket").',
        )

    def handle(self, *args, **options):
        club_name = options.get('club')

        if club_name:
            LOG.info(f'Updating opposition club stats for: {club_name}')
            try:
                club = Club.objects.get(name=club_name)
                update_club_stats_for_club(club)
                LOG.info(f'Successfully updated opposition club stats for: {club_name}')
            except Club.DoesNotExist:
                LOG.error(f'Club "{club_name}" not found.')
            except Exception as e:
                LOG.error(f'Error updating stats for "{club_name}": {e}')
        else:
            LOG.info('Updating all opposition club stats')
            try:
                update_all_club_stats()
                LOG.info('Successfully updated all opposition club stats')
            except Exception as e:
                LOG.error(f'Error updating all opposition stats: {e}')
