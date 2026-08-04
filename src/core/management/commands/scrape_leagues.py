""" Management command that sccrapes England Hockey website for league tables

    Usage:
    python manage.py scrape_leagues                                 # Scrapes all teams for the current season
    python manage.py scrape_leagues --season 2024-2025              # Scrapes all teams for the 2024-2025 season
    python manage.py scrape_leagues --team m1                       # Scrapes M1 for the current season
    python manage.py scrape_leagues --team m1 --season 2024-2025    # Scrapes M1 for the 2024-2025 season
"""

import logging
from django.db.models import Q
from django.core.management.base import BaseCommand
from competitions.models import Season
from teams import league_scraper
from teams.models import ClubTeamSeasonParticipation, ClubTeam

LOG = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Command for scraping league tables from England Hockey."

    def add_arguments(self, parser):
        parser.add_argument(
            '--team',
            type=str,
            help='Optional: Slug of a specific team to scrape (e.g., m1). If omitted, all teams for the target season will be scraped.',
        )
        parser.add_argument(
            '--season',
            type=str,
            help='Optional: Slug of a specific season to scrape (e.g., 2024-2025). If omitted, the current season will be used.',
        )

    def _scrape_single_participation(self, participation, errors_list):
        """Helper method to encapsulate the scraping logic for a single participation."""
        LOG.debug(f"Scraping for Team: {participation.team}")
        LOG.debug(f"  Gender:   {participation.team.gender}")
        LOG.debug(f"  Division: {participation.division}")
        LOG.debug(f"  URL:      {participation.division_tables_url}")

        try:
            # Call the new API-based scraper function
            league_scraper.get_east_england_hockey_division(
                participation.division_tables_url,
                participation.division,
                participation.season,
                participation.team
            )
            LOG.debug(f'Successfully scraped league table for {participation.division_tables_url}')
        except Exception as e:
            errors_list.append(f"Failed to scrape league table from {participation.division_tables_url}: {e}")
            LOG.error(self.style.ERROR(f"  Error: {e}")) # Also print error immediately for context

    def handle(self, *args, **options):
        errors = []
        team_slug = options['team']
        season_slug = options['season']

        target_season_obj = None
        target_team_obj = None
        
        # 1. Determine the target season
        if season_slug:
            try:
                target_season_obj = Season.objects.get(slug=season_slug)
                LOG.info(f"Targeting season: {target_season_obj.slug}")
            except Season.DoesNotExist:
                errors.append(f"ERROR: Season with slug '{season_slug}' not found.")
                LOG.error(self.style.ERROR(errors[-1]))
                return # Cannot proceed without a valid season
        else:
            target_season_obj = Season.current()
            LOG.info(f"No season specified. Defaulting to current season: {target_season_obj.slug}")

        # 2. Determine the target team (if any)
        if team_slug:
            try:
                target_team_obj = ClubTeam.objects.get(slug=team_slug)
                LOG.info(f"Targeting team: {target_team_obj.short_name}")
            except ClubTeam.DoesNotExist:
                errors.append(f"ERROR: Team with slug '{team_slug}' not found.")
                LOG.error(self.style.ERROR(errors[-1]))
                return # Cannot proceed without a valid team if specified

        # 3. Build the initial queryset for participations
        participations_queryset = ClubTeamSeasonParticipation.objects.filter(
            season=target_season_obj
        )

        # 4. Apply team filter if a specific team was provided
        if target_team_obj:
            participations_queryset = participations_queryset.filter(team=target_team_obj)
            LOG.info(f"Scraping specific participation for team '{target_team_obj.short_name}' in season '{target_season_obj.slug}'...")
        else:
            LOG.info(f"Scraping all teams for season '{target_season_obj.slug}'...")

        # 5. Always filter out participations without a division_tables_url and select related objects
        participations_queryset = participations_queryset.exclude(
            Q(division_tables_url__isnull=True) | Q(division_tables_url='')
        ).select_related('team', 'division')

        if not participations_queryset.exists():
            LOG.info(f"No relevant participations found with a league table URL for "
                              f"team: {target_team_obj.short_name if target_team_obj else 'all'} "
                              f"in season: {target_season_obj.slug}.")
            return # Exit if no participations to process

        # 6. Iterate and scrape
        for participation in participations_queryset:
            self._scrape_single_participation(participation, errors)

        if errors:
            LOG.error(self.style.ERROR("\n--- Scraping Errors ---"))
            for error in errors:
                LOG.error(self.style.ERROR(error))
            LOG.error(self.style.ERROR("--- End Errors ---"))
        else:
            LOG.info(self.style.SUCCESS("\nLeague scraping completed successfully with no errors."))
