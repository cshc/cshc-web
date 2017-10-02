"""
  Venue views
"""

from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView


class VenueListView(TemplateView):
    template_name = 'venues/venue_list.html'


class VenueDetailsView(TemplateView):
    template_name = 'venues/venue_details.html'
