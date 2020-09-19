""" Management command that automates tasks that need to run on a
    periodic basis (typically daily).

    This command is run on the production site by a cronjob.

    Usage:
    python manage.py nightly_tasks
"""

from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from django.core.management.base import BaseCommand
from django.core.management import call_command
from matches.models import GoalKing
from competitions.models import Season
from teams import league_scraper
from teams.models import ClubTeamSeasonParticipation
from teams.stats import update_southerners_stats_for_season, update_participation_stats_for_season
from opposition.stats import update_all_club_stats
from training.models import TrainingSession


class Command(BaseCommand):
    help = "Tasks that should be run each night."

    def handle(self, *args, **options):
        errors = []
        season = Season.current()

        try:
            call_command('clearsessions')
        except Exception as e:
            errors.append("Failed to clear old exceptions: {}".format(e))
  
        try:
            # Update goal king
            GoalKing.update_for_season(season)
            print('Updated Goal King entries for the current season')
        except Exception as e:
            errors.append("Failed to update Goal-King: {}".format(e))

        try:
            # Update Southerners league
            update_southerners_stats_for_season(season)
            print('Updated Southerners league for the current season')
        except Exception as e:
            errors.append("Failed to update Southerners League: {}".format(e))

        try:
            # Update opposition stats
            update_all_club_stats()
            print('Updated all opposition club stats')
        except Exception as e:
            errors.append(
                "Failed to update Opposition Club Stats: {}".format(e))

        try:
            # Update ClubTeamSeasonParticipation stats
            update_participation_stats_for_season(season)
            print('Updated Club Team Season Participation stats for the current season')
        except Exception as e:
            errors.append(
                "Failed to update Club Team Season Participation Stats: {}".format(e))

        try:
            # Delete all training session entries from before yesterday
            # (we don't care about training sessions in the past)
            yesterday = timezone.now() - timedelta(days=1)
            TrainingSession.objects.before(yesterday).delete()
            print("Purged all training sessions from before yesterday")
        except Exception as e:
            errors.append("Failed to purge training sessions: {}".format(e))

        # Scrape league tables
        query = Q(division_tables_url__isnull=True) | Q(division_tables_url='')
        participations = ClubTeamSeasonParticipation.objects.current(
        ).exclude(query).select_related('team', 'division')

        for participation in participations:
            try:
                league_scraper.get_hockey_east_division(
                    participation.division_tables_url, participation.division, season)
                print('Scraped league table for ' +
                      participation.division_tables_url)
            except Exception as e:
                errors.append("Failed to scrape league table from {}: {}".format(
                    participation.division_tables_url, e))

        # Backup database
        try:
            call_command('dbbackup', clean=True)
        except Exception as e:
            errors.append("Failed to backup database")

        for error in errors:
            print(error)
