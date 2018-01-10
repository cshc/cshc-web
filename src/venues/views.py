"""
Venue views
"""
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import DetailView, TemplateView
from django.urls import reverse
from competitions.models import Season, Division
from competitions.views import js_divisions
from teams.models import ClubTeam
from teams.views import js_clubteams
from .models import Venue


def js_venues():
    """
    Return a list of all venues, with id and name properties,
    suitable for passing to JavaScript.
    """
    return list(Venue.objects.values('id', 'name'))


class VenueListView(TemplateView):
    """
    List of all the match venues.
    """
    template_name = 'venues/venue_list.html'

    def get_context_data(self, **kwargs):
        context = super(VenueListView, self).get_context_data(**kwargs)

        current_season = Season.current()

        context['props'] = {
            'currentSeason': current_season.slug,
            'teams': js_clubteams(True),
            'divisions': js_divisions(current_season),
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
                'venue_Slug': venue.slug,
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
