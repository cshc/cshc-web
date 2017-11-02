"""
Venue views
"""
from django.views.generic import ListView, TemplateView
from django.shortcuts import get_object_or_404
from django.http import Http404
from competitions.models import Season
from core.views import kwargs_or_none, add_season_selector
from .models import ClubTeam, ClubTeamSeasonParticipation


class ClubTeamListView(ListView):
    """
    List of all the CSHC teams.
    """
    context_object_name = 'teams'
    model = ClubTeam

    def get_context_data(self, **kwargs):
        context = super(ClubTeamListView, self).get_context_data(**kwargs)

        return context


class ClubTeamDetailView(TemplateView):
    """
    Details of a particular team.
    """
    model = ClubTeam
    template_name = 'teams/clubteam_detail.html'

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

        add_season_selector(context, season, part_seasons)

        context['props'] = {
            'teamId': team.id,
            'teamGenderlessName': team.genderless_abbr_name(),
            'seasonId': season.id,
            'division': {
                'id': participation.division.id,
                'name': "{}".format(participation.division),
                'fixturesUrl': participation.division_fixtures_url,
                'leagueTableUrl': participation.division_tables_url,
            },
            'matchFilters': {
                'ourTeam_Slug': team.slug,
                'season_Slug': season.slug,
            },
        }

        return context
