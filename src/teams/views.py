"""
Venue views
"""
import logging
from itertools import groupby
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404
from competitions.models import Season
from core.utils import get_thumbnail_url
from core.views import kwargs_or_none, add_season_selector, get_season_from_kwargs
from .models import ClubTeam, ClubTeamSeasonParticipation, Southerner

LOG = logging.getLogger(__name__)


def js_clubteams(active_only=False):
    """ Return a list of all club teams, with 'long_name' and 'slug' properties, suitable for passing to JavaScript """
    teams = ClubTeam.objects.all()
    if active_only:
        teams = teams.filter(active=True)
    return list(teams.values('long_name', 'slug'))


class ClubTeamListView(TemplateView):
    """ View of a list of all CSHC teams. """

    model = ClubTeam
    template_name = 'teams/clubteam_list.html'

    def get_context_data(self, **kwargs):
        context = super(ClubTeamListView, self).get_context_data(**kwargs)

        all_teams = list(ClubTeam.objects.all())

        for team in all_teams:
            team.category = 'Inactive' if not team.active else (team.get_gender_display() if (team.long_name.startswith('Men\'s') or team.long_name.startswith('Ladies'))
                                                                else 'Other')

            team.participation = team.current_participation()

            if team.participation and team.participation.team_photo:
                photo_url = get_thumbnail_url(
                    team.participation.team_photo, '600x393', 'center', team.participation.team_photo_cropping),
                if photo_url:
                    team.photo_url = photo_url[0] if isinstance(photo_url, tuple) else photo_url

            team.ical = reverse('clubteam_ical_feed',
                                kwargs={'slug': team.slug})
            team.rss = reverse('clubteam_match_rss_feed',
                               kwargs={'slug': team.slug})

        context['teams'] = all_teams
        return context


class ClubTeamDetailView(TemplateView):
    """
    Details of a particular team.
    """
    model = ClubTeam
    template_name = 'teams/clubteam_detail.html'

    def dispatch(self, request, *args, **kwargs):
        # If the team did not participate in the season specified, redirect to the current season's view
        if 'season_slug' in kwargs:
            if (not ClubTeamSeasonParticipation.objects.filter(
                    team__slug=kwargs['slug'], season__slug=kwargs['season_slug']).exists()):
                LOG.warning("Team %s did not participate in %s. Defaulting to current/latest season",
                            kwargs['slug'], kwargs['season_slug'])
                return redirect('clubteam_detail', slug=kwargs['slug'])

        return super(ClubTeamDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClubTeamDetailView, self).get_context_data(**kwargs)

        # The team is specified in the URL by its slug
        team = get_object_or_404(ClubTeam, slug=kwargs['slug'])
        context['team'] = team

        # Get the seasons in which this team competed
        part_seasons = Season.objects.filter(
            clubteamseasonparticipation__team=team).order_by('-start')

        # The season may or may not be specified in the URL by its slug.
        # If it isn't, we use the current season
        season_slug = kwargs_or_none('season_slug', **kwargs)
        if season_slug is not None:
            season = Season.objects.get(slug=season_slug)
        else:
            # Default to the most recent season
            season = part_seasons[0]

        # Get the participation information for this team and season
        try:
            participation = ClubTeamSeasonParticipation.objects.select_related(
                'division__league', 'season').get(team=team, season=season)
            context['participation'] = participation
        except ClubTeamSeasonParticipation.DoesNotExist:
            raise Http404

        add_season_selector(
            context, season, list(part_seasons.values_list('slug', flat=True)))

        context['props'] = {
            'teamId': team.id,
            'teamGenderlessName': team.genderless_abbr_name(),
            'seasonId': season.id,
            'division': {
                'id': participation.division.id if participation.division else None,
                'name': "{}".format(participation.division),
                'fixturesUrl': participation.division_fixtures_url,
                'leagueTableUrl': participation.division_tables_url,
            },
            'matchFilters': {
                'pageSize': 1000,
                'ourTeam_Slug': team.slug,
                'season_Slug': season.slug,
            },
        }

        return context


class SouthernersSeasonView(TemplateView):
    """ View for displaying the Southerners League stats for a particular season"""

    template_name = 'teams/southerners_league.html'

    def get_southerners_list(self, season):
        """ Returns a list of Southerners League items for the specified season"""

        # We convert the queryset to a list so we can add a 'rank' attribute to each item
        team_list = list(Southerner.objects.by_season(season))

        # Apply ranking
        if len(team_list) > 0:
            rank = 1
            previous = team_list[0]
            previous.rank = 1
            for i, entry in enumerate(team_list[1:]):
                if entry.avg_points_per_game != previous.avg_points_per_game:
                    rank = i + 2
                    entry.rank = str(rank)
                else:
                    entry.rank = "%s=" % rank
                    previous.rank = entry.rank
                previous = entry

        return team_list

    def get_context_data(self, **kwargs):
        """ Gets the context data for the view.

            In addition to the 'team_list' item, the following are also added to the context:
            - season:               the season these stats applies to
            - season_slug_list:     a list of all seasons
            - is_current_season:    True if season == Season.current()
        """
        context = super(SouthernersSeasonView, self).get_context_data(**kwargs)
        season = get_season_from_kwargs(kwargs)

        context['team_list'] = self.get_southerners_list(season)

        season_slug_list = list(Southerner.objects.order_by(
            '-season').values_list('season__slug', flat=True).distinct())

        add_season_selector(context, season, season_slug_list)

        return context


class PlayingRecordView(TemplateView):
    """ View of the playing record stats for each team in the club"""

    template_name = 'teams/playing_record.html'

    def get_all_playing_records(self):
        """ Returns a dictionary of Playing Records, keyed by team """

        # Get all participation entries
        participations = ClubTeamSeasonParticipation.objects.select_related(
            'team', 'season').order_by('team', '-season')

        grouped_by_team = groupby(participations, lambda x: x.team)
        parts = []
        for team, seasons in grouped_by_team:
            team_parts = []
            for participation in seasons:
                team_parts.append(participation)
            parts.append([team, team_parts])
        return parts

    def get_context_data(self, **kwargs):
        context = super(PlayingRecordView, self).get_context_data(**kwargs)
        context['participation'] = self.get_all_playing_records()
        return context
