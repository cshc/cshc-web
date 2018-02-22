"""
  Views for Awards and Award Winners
"""

from django.views.generic import TemplateView
from members.models import Member
from .models import EndOfSeasonAwardWinner, EndOfSeasonAward


class EndOfSeasonAwardWinnersView(TemplateView):
    """ View with a list of all members"""
    template_name = 'awards/eos_list.html'

    def get_context_data(self, **kwargs):
        context = super(EndOfSeasonAwardWinnersView,
                        self).get_context_data(**kwargs)

        season_list = list(EndOfSeasonAwardWinner.objects.values_list(
            'season__slug', flat=True).distinct())
        award_list = list(EndOfSeasonAward.objects.order_by('name').values(
            'name', 'id').distinct())
        awardee_list = list(Member.objects.filter(awards_endofseasonawardwinner_awards__isnull=False).values(
            'first_name', 'last_name', 'id').distinct())
        context['props'] = {
            'seasons': season_list,
            'awards': award_list,
            'awardees': awardee_list,
        }
        return context
