"""
Venue views
"""
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import DetailView, TemplateView
from django.urls import reverse
from competitions.models import Season, Division
from teams.models import ClubTeam
from .models import Venue


class VenueListView(TemplateView):
    """
    List of all the match venues.
    """
    template_name = 'venues/venue_list.html'

    def get_context_data(self, **kwargs):
        context = super(VenueListView, self).get_context_data(**kwargs)

        current_season = Season.current()

        current_divisions = Division.objects.select_related('league').filter(
            clubteamseasonparticipation__season=current_season).order_by('clubteamseasonparticipation__team__position')

        divisions = [{'id': x.id, 'name': "{}".format(
            x)} for x in current_divisions]

        context['props'] = {
            'currentSeason': current_season.slug,
            'teams': list(ClubTeam.objects.active().values('long_name', 'slug')),
            'divisions': divisions,
        }
        return context


class VenueDetailView(DetailView):
    """
    Details of a particular venue.
    """
    context_object_name = 'venue'
    model = Venue

    def get_context_data(self, **kwargs):
        context = super(VenueDetailView, self).get_context_data(**kwargs)
        venue = context['venue']
        context['props'] = {
            'venueName': venue.name,
            'matchFilters': {
                'venue_Name': venue.name,
            },
        }
        return context


class DirectionsView(TemplateView):
    """ A simple view with an overview of the home venue and match tea locations.
    """
    template_name = "club_info/directions.html"

    def get_context_data(self, **kwargs):
        context = super(DirectionsView, self).get_context_data(**kwargs)
        homePitch = Venue.objects.get(slug='long-road')
        context['homePitch'] = homePitch
        return context
