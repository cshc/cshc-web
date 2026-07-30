""" Django views that don't fit nicely into one of the other apps.
"""

from datetime import datetime
from django.views.generic import TemplateView
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from graphene_django.views import GraphQLView
from training.views import UpcomingTrainingSessionsView
from core.models import TeamGender
from core.views import get_season_from_kwargs, add_season_selector
from competitions.models import Season
from teams.models import ClubTeam, TeamCaptaincy
from matches.models import Match, Appearance
from members.models import CommitteeMembership
from members.utils import member_from_request


class HomeView(TemplateView):
    """ The main home page of the Cambridge South Hockey Club website. """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        member = member_from_request(self.request)
        self.addLatestResultsToContext(context)
        self.addNextFixturesToContext(context)

        # Upcoming Training
        UpcomingTrainingSessionsView.addUpcomingTrainingToContext(context)

        # Sub-navigation elements
        context['sub_nav_items'] = [
            {'id': 'news', 'label': 'Latest News'},
            {'id': 'comments', 'label': 'Recent Comments'},
            {'id': 'tweets', 'label': 'Tweets'},
            {'id': 'strava', 'label': 'Strava'},
        ]

        if member:
            try:
                context['last_appearance_match_id'] = Appearance.objects.by_member(
                    member).order_by('-match__date').values_list('match_id', flat=True).first()
            except Appearance.DoesNotExist:
                pass
        return context

    def addLatestResultsToContext(self, context):
        """ Helper method to add latest results to a context dictionary.
            context = the view context (a dictionary)
            Adds a 'latest_results' entry to the context dictionary
            containing a list of dates, with each date containing the matches
            played on that date, ordered by team position

            The latest_results list contains a maximum of one result per team.
            Results are only included if the team is active and the match was
            played this season.
        """
        latest_results = []
        current_season = Season.current()
        today = timezone.now().date()
        dt_now = datetime.now()
        for team in ClubTeam.objects.active().only('pk'):
            match_qs = Match.objects.select_related('our_team', 'opp_team__club', 'venue',
                                                    'division__league', 'cup', 'season')

            match_qs = match_qs.filter(our_team_id=team.pk,
                                       date__lte=today,
                                       season=current_season)

            match_qs = match_qs.order_by('-date', '-time')

            # Have to ignore matches that are today but still in future.
            for m in match_qs:
                if m.datetime() < dt_now:
                    latest_results.append(m)
                    break

        context['latest_results'] = self.group_by_date(latest_results, True)

    def addNextFixturesToContext(self, context):
        """ Helper method to add next fixtures to a context dictionary.
            context = the view context (a dictionary)
            Returns: the context dictionary, with a 'next_fixtures' entry
                     containing a list of fixtures

            The next_fixtures list contains a maximum of one fixture per team.
        """
        next_fixtures = []
        today = timezone.now().date()
        dt_now = datetime.now()
        for team in ClubTeam.objects.active().only('pk'):
            match_qs = Match.objects.select_related('our_team', 'opp_team__club', 'venue',
                                                    'division__league', 'cup', 'season')
            match_qs = match_qs.filter(our_team_id=team.pk, date__gte=today)
            match_qs = match_qs.order_by('date', 'time')
            # Have to ignore matches that are today but in the past.
            for m in match_qs:
                if m.datetime() > dt_now:
                    next_fixtures.append(m)
                    break

        context['next_fixtures'] = self.group_by_date(next_fixtures)

    def group_by_date(self, matches, reverse=False):
        """ 
        Groups the matches by date (in ascending order), with each date's matches
        being ordered by team position.

        Returns a list of objects with 'date' and 'matches' properties.
        """
        matches = sorted(matches, key=lambda m: m.datetime())
        if reverse:
            matches = reversed(matches)

        match_dates = []
        for match in matches:
            if len(match_dates) > 0 and match.date == match_dates[-1]['date']:
                match_dates[-1]['matches'].append(match)
            else:
                match_dates.append(dict(date=match.date, matches=[match]))

        # Sort each date's matches by team position
        for date in match_dates:
            date['matches'] = sorted(
                date['matches'], key=lambda r: r.our_team.position)

        return match_dates


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

    def get_context_data(self, **kwargs):
        context = super(CommitteeSeasonView, self).get_context_data(**kwargs)

        season = get_season_from_kwargs(kwargs)
        current_season_obj = Season.current()

        all_committee_memberships = CommitteeMembership.objects.select_related(
            'position', 'member', 'season').filter(season=season).order_by('position__index')

        mens_captains_list = []
        ladies_captains_list = []
        mixed_captains_list = []

        if season == current_season_obj:
            participating_teams_qs = ClubTeam.objects.active().order_by('position')
        else:
            participating_teams_qs = ClubTeam.objects.filter(
                clubteamseasonparticipation__season=season
            ).active().order_by('position').distinct()

        for team in participating_teams_qs:
            team.name = team.long_name

            captains_qs = TeamCaptaincy.get_captains(team=team, season=season)
            vice_captains_qs = TeamCaptaincy.get_vice_captains(team=team, season=season)

            if team.gender == TeamGender.Mixed:
                co_captains = list(captains_qs)
                if len(co_captains) > 0:
                    team.captain = co_captains[0]
                    if len(co_captains) > 1:
                        team.vice_captain = co_captains[1]
                    else:
                        team.vice_captain = None
                else:
                    team.captain = None
                    team.vice_captain = None
                mixed_captains_list.append(team)
            else:
                team.captain = captains_qs.first()
                team.vice_captain = vice_captains_qs.first()
                if team.gender == TeamGender.Mens:
                    mens_captains_list.append(team)
                elif team.gender == TeamGender.Ladies:
                    ladies_captains_list.append(team)

        context['mens_captains'] = mens_captains_list
        context['ladies_captains'] = ladies_captains_list
        context['mixed_captains'] = mixed_captains_list

        context['general_committee'] = [
            m for m in all_committee_memberships
            if not ("Captain" in m.position.name or "Co-Captain" in m.position.name)
        ]

        season_slug_list = list(Season.objects.filter(
            clubteamseasonparticipation__isnull=False
        ).values_list('slug', flat=True).distinct().order_by('-start'))
        add_season_selector(context, season, season_slug_list)

        return context


@user_passes_test(lambda u: u.is_superuser)
def templateTestView(request, template):
    """
    This is a debug utility, restricted to super-users. It lets you enter a url like 
    '/test-template/my-template.html' and view the rendered HTML in the browser.

    You can enter simple key/value context items as URL params. For example:
    '/test-template/my-template.html?key1=value1&key2=value2'

    """
    context = dict(request.GET.items())
    return render(request, template, context)


class CshcGraphQLView(UserPassesTestMixin, GraphQLView):
    """ Restrict GraphQLView to super-users """

    def test_func(self):
        return self.request.method == 'POST' or self.request.user.is_superuser
