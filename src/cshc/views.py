""" Django views that don't fit nicely into one of the other apps.
"""

import csv
import hmac
from datetime import datetime
from django.views.generic import TemplateView
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseForbidden
from graphene_django.views import GraphQLView
from training.views import UpcomingTrainingSessionsView
from core.models import TeamGender, ClubInfo, Gender
from core.views import get_season_from_kwargs, add_season_selector
from competitions.models import Season
from teams.models import ClubTeam, TeamCaptaincy
from matches.models import Match, Appearance
from members.models import CommitteeMembership, Member
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
        all_committee_memberships = CommitteeMembership.objects.select_related(
            'position', 'member', 'season').filter(season=season).order_by('position__index')

        context['general_committee'] = [
            m for m in all_committee_memberships
            if not ("Captain" in m.position.name or "Co-Captain" in m.position.name)
        ]

        season_slug_list = list(Season.objects.filter(
            clubteamseasonparticipation__isnull=False
        ).values_list('slug', flat=True).distinct().order_by('-start'))
        add_season_selector(context, season, season_slug_list)

        return context


class CaptainsSeasonView(TemplateView):
    """ View for displaying the Club Captains for a particular season. """
    template_name = 'club_info/teamcaptains.html'

    def get_context_data(self, **kwargs):
        context = super(CaptainsSeasonView, self).get_context_data(**kwargs)

        season = get_season_from_kwargs(kwargs)
        current_season_obj = Season.current()

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


@require_http_methods(['GET', 'POST'])
def shirt_numbers_export(request):
    """ Password-protected CSV export of assigned shirt numbers per gender.

        The password is stored in ClubInfo under the key 'SuppliersPassword'. If
        the key is unset or empty, the endpoint returns 403 for all callers.

        GET renders a small form. POST validates the submitted password and
        streams the CSV attachment. The password only ever travels in the POST
        body, never in the URL.
    """
    try:
        expected = ClubInfo.objects.get(key='SuppliersPassword').value
    except ClubInfo.DoesNotExist:
        expected = ''

    if not expected:
        return HttpResponseForbidden('Forbidden')

    if request.method == 'GET':
        return render(request, 'club_info/shirt_numbers_export.html', {})

    supplied = request.POST.get('password', '')
    if not hmac.compare_digest(str(expected), str(supplied)):
        return HttpResponseForbidden('Incorrect password.')

    max_shirt_number_obj, _ = ClubInfo.objects.get_or_create(
        key='ShirtNumMax', defaults={'value': '199'})
    max_shirt_number = int(max_shirt_number_obj.value)

    gender_columns = ((Gender.Male, "Men's"), (Gender.Female, "Ladies'"))

    buckets_by_gender = {}
    for gender_value, _label in gender_columns:
        active = Member.objects._get_members_with_active_shirt_numbers_queryset(gender_value).only(
            'pk', 'first_name', 'known_as', 'last_name', 'shirt_number')
        buckets = {}
        for member in active:
            raw = (member.shirt_number or '').strip()
            if not raw:
                continue
            try:
                n = int(raw)
            except ValueError:
                continue
            if 1 <= n <= max_shirt_number:
                buckets.setdefault(n, []).append(member)
        buckets_by_gender[gender_value] = buckets

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="shirt-numbers.csv"'
    # UTF-8 BOM so Excel decodes accented characters correctly.
    response.write('﻿')
    writer = csv.writer(response)
    writer.writerow(['Number'] + [label for _, label in gender_columns])
    for n in range(1, max_shirt_number + 1):
        row = [n]
        for gender_value, _label in gender_columns:
            members = buckets_by_gender[gender_value].get(n, [])
            row.append('; '.join(m.full_name() for m in members))
        writer.writerow(row)
    return response
