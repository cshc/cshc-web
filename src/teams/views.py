"""
Venue views
"""
from django.views.generic import DetailView

from .models import ClubTeam


class ClubTeamDetailsView(DetailView):
    """
    Details of a particular venue.
    """
    context_object_name = 'team'
    model = ClubTeam

    def get_context_data(self, **kwargs):
        context = super(ClubTeamDetailsView, self).get_context_data(**kwargs)
        return context
