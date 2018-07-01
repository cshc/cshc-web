""" Management command used to copy all ClubTeamSeasonParticipations from the previous
    season to the latest season.

    Usage:
    python manage.py copy_participation
"""

from django.core.management.base import BaseCommand
from teams.models import ClubTeamSeasonParticipation
from competitions.models import Season


class Command(BaseCommand):
    """ Management command used to copy all ClubTeamSeasonParticipations from the previous
        season to the latest season.
    """
    help = "Copies all Club Team Season Participation records from the previous season to the current season."

    def add_arguments(self, parser):
        parser.add_argument(
            '--sim',
            action='store_true',
            dest='simulate',
            default=False,
            help='Simulation mode (database will not be written to)',
        )

    def handle(self, *args, **options):
        season = Season.objects.latest()
        prev_season = Season.objects.previous(season)

        if ClubTeamSeasonParticipation.objects.by_season(season).exists():
            print "ERROR: ClubTeamSeasonParticipation entries already exist for {0}. To run this command, first delete all ClubTeamSeasonParticipation entries for {0}".format(season)
            return

        prev_parts = ClubTeamSeasonParticipation.objects.by_season(prev_season)

        for part in prev_parts:
            part_copy = ClubTeamSeasonParticipation(team=part.team,
                                                    season=season,
                                                    division=part.division,
                                                    team_photo=part.team_photo,
                                                    team_photo_caption=part.team_photo_caption,
                                                    division_tables_url=part.division_tables_url,
                                                    division_fixtures_url=part.division_fixtures_url,
                                                    cup=part.cup)
            if not options['simulate']:
                part_copy.save()
            else:
                print "Saving new participation: {}".format(part_copy)
