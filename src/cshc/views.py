""" Django views that don't fit nicely into one of the other apps.
"""

from datetime import datetime
from django.views.generic import TemplateView
from django.utils import timezone
from training.views import UpcomingTrainingSessionsView
from competitions.models import Season
from teams.models import ClubTeam
from matches.models import Match


class HomeView(TemplateView):
    """ The main home page of the Cambridge South Hockey Club website. """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        self.addLatestResultsToContext(context)
        self.addNextFixturesToContext(context)

        # Upcoming Training
        UpcomingTrainingSessionsView.addUpcomingTrainingToContext(context)

        return context

    def addLatestResultsToContext(self, context):
        """ Helper method to add latest results to a context dictionary.
            context = the view context (a dictionary)
            Returns: the context dictionary, with a 'latest_results' entry
            containing a list of results

            The latest_results list contains a maximum of one result per team.
            Results are only included if the team is active and the match was
            played this season.
        """
        latest_results = []
        current_season = Season.current()
        today = timezone.now().date()
        for team in ClubTeam.objects.only('pk'):
            match_qs = Match.objects.select_related('our_team', 'opp_team__club', 'venue',
                                                    'division__league', 'cup', 'season')
            match_qs = match_qs.filter(our_team__active=True, our_team_id=team.pk,
                                       date__lte=today, season=current_season)
            match_qs = match_qs.order_by('-date', '-time')
            if match_qs.exists():
                # Have to ignore matches that are today but still in future.
                dt_now = datetime.now()
                for m in match_qs:
                    if m.datetime() < dt_now:
                        latest_results.append(m)
                        break

        context['latest_results'] = latest_results

    def addNextFixturesToContext(self, context):
        """ Helper method to add next fixtures to a context dictionary.
            context = the view context (a dictionary)
            Returns: the context dictionary, with a 'next_fixtures' entry
                     containing a list of fixtures

            The next_fixtures list contains a maximum of one fixture per team.
        """
        next_fixtures = []
        today = timezone.now().date()
        for team in ClubTeam.objects.only('pk'):
            match_qs = Match.objects.select_related('our_team', 'opp_team__club', 'venue',
                                                    'division__league', 'cup', 'season')
            match_qs = match_qs.filter(our_team_id=team.pk, date__gte=today)
            match_qs = match_qs.order_by('date', 'time')
            if match_qs.exists():
                # Have to ignore matches that are today but in the past.
                dt_now = datetime.now()
                for m in match_qs:
                    if m.datetime() > dt_now:
                        next_fixtures.append(m)
                        break

        context['next_fixtures'] = next_fixtures
