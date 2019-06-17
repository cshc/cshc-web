"""
Views for Opposition Clubs etc
"""
from braces.views import SelectRelatedMixin
from django.views.generic import TemplateView, DetailView
from .models import Club, ClubStats


def js_opposition_clubs():
    """
    Return a list of all opposition clubs, with 'id' and 'name' properties
    (suitable for passing to JavaScript)
    """
    return list(Club.objects.values('slug', 'name'))


class ClubListView(TemplateView):
    """ View for a list of opposition clubs"""

    template_name = 'opposition/club_list.html'
    model = Club


class ClubDetailView(SelectRelatedMixin, DetailView):
    """ View for a particular opposition club.
    """
    template_name = 'opposition/club_detail.html'
    model = Club
    context_object_name = 'club'
    select_related = ['default_venue']

    def get_context_data(self, **kwargs):
        context = super(ClubDetailView, self).get_context_data(**kwargs)

        club = context['club']
        context['props'] = {
            'clubName': club.name,
            'matchFilters': {
                'pageSize': 1000,
                'oppTeam_Club_Slug': club.slug,
            },
        }
        return context
