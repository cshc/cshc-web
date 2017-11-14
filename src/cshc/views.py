""" Django views that don't fit nicely into one of the other apps.
"""

from datetime import datetime
from django.views.generic import TemplateView
from django.utils import timezone
from training.views import UpcomingTrainingSessionsView
from core.models import TeamGender
from core.views import get_season_from_kwargs, add_season_selector
from competitions.models import Season
from teams.models import ClubTeam
from matches.models import Match
from members.models import CommitteeMembership


class HomeView(TemplateView):
    """ The main home page of the Cambridge South Hockey Club website. """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        self.addLatestResultsToContext(context)
        self.addNextFixturesToContext(context)

        # Upcoming Training
        UpcomingTrainingSessionsView.addUpcomingTrainingToContext(context)

        # Sub-navigation elements
        context['sub_nav_items'] = [
            {'id': 'training', 'label': 'Next Training'},
            {'id': 'comments', 'label': 'Recent Comments'},
            {'id': 'news', 'label': 'Latest News'},
            {'id': 'tweets', 'label': 'Tweets'},
        ]

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


class CalendarView(TemplateView):
    """ Displays an embedded Google Calendar view of the various fixtures, social events
        and training sessions for the current season.
    """
    template_name = 'club_info/calendar.html'

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)

        context['teams'] = ClubTeam.objects.active()

        context['all_gcal'] = 'i7ngcunrs8icf3btp6llk1eav1bvuqol@import.calendar.google.com'
        context['training_gcal'] = '55b76kp09vmmck17985jt8qce08e9jee@import.calendar.google.com'
        context['events_gcal'] = 't7dhl1k54rqb6mmt0huu778ac8@group.calendar.google.com'
        context['juniors_gcal'] = '4oati7ee6231hb6gtajift5hvs@group.calendar.google.com'
        return context


class CommitteeSeasonView(TemplateView):
    """ View for displaying the Club Committee members for a particular season. """
    template_name = 'club_info/committee.html'

    def get_captains(self, committee_list, team_names):
        """ 
        Gets a list of team objects with captains and vice-captains populated

        Returns: a list of objects, each with name, captain and vice_captain fields
        """
        return [
            {
                'name': team_name,
                'captain': next((m for m in committee_list if m.position.name == "{} Captain".format(team_name)), None),
                'vice_captain': next((m for m in committee_list if m.position.name == "{} Vice-Captain".format(team_name)), None)
            } for team_name in team_names
        ]

    def get_context_data(self, **kwargs):
        context = super(CommitteeSeasonView, self).get_context_data(**kwargs)

        # If we're viewing this season's committee we may not have a season_slug keyword arg.
        season = get_season_from_kwargs(kwargs)

        all_members = CommitteeMembership.objects.select_related(
            'position', 'member', 'season').filter(season=season).order_by('position__index')

        context['general_committee'] = [
            m for m in all_members if m.position.gender == TeamGender.Mixed]
        ladies_committee = [
            m for m in all_members if m.position.gender == TeamGender.Ladies]
        mens_committee = [
            m for m in all_members if m.position.gender == TeamGender.Mens]

        ladies_team_names = list(
            ClubTeam.objects.ladies().values_list('long_name', flat=True))
        mens_team_names = list(
            ClubTeam.objects.mens().values_list('long_name', flat=True))

        context['mens_captains'] = self.get_captains(
            mens_committee, mens_team_names)

        context['ladies_captains'] = self.get_captains(
            ladies_committee, ladies_team_names)

        context['mixed_captains'] = {
            'name': "Mixed XI",
            'captain': next((m for m in mens_committee if m.position.name == "Men's Mixed XI Co-Captain"), None),
            'vice_captain': next((m for m in ladies_committee if m.position.name == "Ladies' Mixed XI Co-Captain"), None)
        }

        add_season_selector(context, season, Season.objects.reversed())
        return context
