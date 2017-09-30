"""
  Venue views
"""

from django.http import HttpResponse
from django.template import loader


def index(request):
    """
      Get the list of venues.
    """
    template = loader.get_template('venues/index.html')
    context = {}
    return HttpResponse(template.render(context, request))
