"""
Venue views
"""
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import ListView, DetailView
from django.urls import reverse

from .models import Venue


class VenueListView(ListView):
    """
    List of all the match venues.
    """
    context_object_name = 'venues'
    model = Venue

    def get_context_data(self, **kwargs):
        context = super(VenueListView, self).get_context_data(**kwargs)

        # TODO: Don't fetch all venues twice (once manually, once automatically)
        venues = Venue.objects.all()

        venue_details = map(lambda v: {
            'name': v.name,
            'short_name': v.short_name,
            'slug': v.slug,
            'url': v.url,
            'is_home': v.is_home,
            'phone': v.phone,
            'addr1': v.addr1,
            'addr2': v.addr2,
            'addr3': v.addr3,
            'addr_city': v.addr_city,
            'addr_postcode': v.addr_postcode,
            'full_address': v.full_address(),
            'notes': v.notes,
            'distance': v.distance,
            'position': v.position_list(),
            'url': reverse('venue_detail', kwargs={'slug': v.slug}),
        }, venues)

        context['venues_json'] = json.dumps(
            list(venue_details), cls=DjangoJSONEncoder)
        return context


class VenueDetailsView(DetailView):
    """
    Details of a particular venue.
    """
    context_object_name = 'venue'
    model = Venue

    def get_context_data(self, **kwargs):
        context = super(VenueDetailsView, self).get_context_data(**kwargs)
        # TODO: Add upcoming (and previous?) matches at this venue
        return context
