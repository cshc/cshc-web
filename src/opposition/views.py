"""
Views for Opposition Clubs etc
"""
from braces.views import SelectRelatedMixin
from django.views.generic import TemplateView, DetailView
from .models import Club, ClubStats


class ClubListView(TemplateView):
    """ View for a list of opposition clubs"""

    template_name = 'opposition/club_list.html'
    model = Club

    def get_context_data(self, **kwargs):
        context = super(ClubListView, self).get_context_data(**kwargs)

        all_club_stats = ClubStats.objects.totals()
        context['clubstats_list'] = [
            x for x in all_club_stats if x.total_played > 0]
        return context


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
                'oppTeam_Club_Slug': club.slug,
            },
        }
        return context
