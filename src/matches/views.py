"""
Views related to matches
"""
from braces.views import SelectRelatedMixin
from django.views.generic import DetailView, ListView, TemplateView
from awards.models import MatchAward
from core.models import ClubInfo
from .models import Match


class MatchListView(ListView):
    """ A view of all matches - paginated, filterable, sortable"""
    model = Match

    def get_context_data(self, **kwargs):
        context = super(MatchListView, self).get_context_data(**kwargs)
        # match_qs = Match.objects.select_related('our_team', 'opp_team__club', 'venue',
        #                                         'division__league', 'cup', 'season')
        # match_qs = match_qs.prefetch_related('players')
        # match_qs = match_qs.defer('report_body', 'pre_match_hype')
        # match_qs = match_qs.order_by('-date', '-time')

        # context['filter'] = MatchFilter(self.request.GET, queryset=match_qs)
        return context


class MatchDetailView(SelectRelatedMixin, DetailView):
    """ View providing details of a particular match"""
    model = Match
    select_related = ['our_team', 'opp_team__club',
                      'venue', 'division__league', 'cup', 'season']

    def get_context_data(self, **kwargs):
        """
        Gets the context data for the view.

        In addition to the 'match' item, the following are also added to the context:
            - same_date_matches:    a list of matches on the same day (not including
                                    the match being viewed)
            - mom_winners:          a list of 'Man of the Match' award winners
            - lom_winners:          a list of 'Lemon of the Match' award winners
            - appearances:          a list of appearances in this match
            - prev_match:           the previous match this team played
            - next_match:           the next match this team played/is due to play
        """
        context = super(MatchDetailView, self).get_context_data(**kwargs)
        match = context["match"]

        # Add various bits of info to the context object
        same_date_matches = Match.objects.filter(
            date=match.date).exclude(pk=match.pk)

        award_winners = match.award_winners.select_related(
            'award', 'member__user').all()

        appearances = match.appearances.select_related('member__user').all()
        appearances = appearances.order_by('member__pref_position')

        scorers = []
        green_cards = []
        yellow_cards = []
        red_cards = []

        for app in appearances:
            if app.goals > 0:
                scorers.append(app)
            if app.green_card:
                green_cards.append(app.member)
            if app.yellow_card:
                yellow_cards.append(app.member)
            if app.red_card:
                red_cards.append(app.member)

        context['scorers'] = scorers
        context['green_cards'] = green_cards
        context['yellow_cards'] = yellow_cards
        context['red_cards'] = red_cards

        match_qs = Match.objects.select_related(
            'our_team', 'opp_team__club').filter(our_team=match.our_team)

        prev_match = match_qs.filter(
            date__lt=match.date).order_by('-date', '-time').first()

        next_match = match_qs.filter(date__gt=match.date).first()

        context["same_date_matches"] = same_date_matches
        context["mom_winners"] = [
            x for x in award_winners if x.award.name == MatchAward.MOM]
        context["lom_winners"] = [
            x for x in award_winners if x.award.name == MatchAward.LOM]
        context["appearances"] = appearances
        context["prev_match"] = prev_match
        context["next_match"] = next_match

        live_comments_enabled, _ = ClubInfo.objects.get_or_create(
            key='EnableLiveComments', defaults={'value': 'False'})

        context["enable_live_comments"] = live_comments_enabled.value in [
            'True', 'true', 'yes', '1']
        return context
