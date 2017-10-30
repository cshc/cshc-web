"""
Venue views
"""
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import ListView, DetailView
from django.urls import reverse
from competitions.models import Season, Division
from teams.models import ClubTeam
from .models import Venue


class VenueListView(ListView):
    """
    List of all the match venues.
    """
    context_object_name = 'venues'
    model = Venue

    def get_context_data(self, **kwargs):
        context = super(VenueListView, self).get_context_data(**kwargs)

        current_season = Season.current()

        current_divisions = Division.objects.filter(
            clubteamseasonparticipation__season=current_season).order_by('clubteamseasonparticipation__team__position')

        divisions = [{'id': x.id, 'name': "{}".format(
            x)} for x in current_divisions]

        context['props'] = {
            'currentSeason': current_season.slug,
            'teams': list(ClubTeam.objects.active().values('long_name', 'slug')),
            'divisions': divisions,
        }
        return context


class VenueDetailsView(DetailView):
    """
    Details of a particular venue.
    """
    context_object_name = 'venue'
    model = Venue
