"""
Views related to matches
"""
from braces.views import SelectRelatedMixin
from django.views.generic import DetailView, ListView, TemplateView
from django.db.models import Q
from awards.models import MatchAward
from competitions.models import Season
from core.models import ClubInfo, Gender
from core.views import get_season_from_kwargs, add_season_selector
from .models import Match, GoalKing, Appearance


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


class GoalKingView(TemplateView):
    """ View for displaying the Goal King stats for a particular season. """
    template_name = 'matches/goalking.html'

    def get_context_data(self, **kwargs):
        context = super(GoalKingView, self).get_context_data(**kwargs)
        context['props'] = {
            'seasons':  list(GoalKing.objects.order_by('-season').values_list('season__slug', flat=True).distinct()),
            'current_season': Season.current().slug,
        }
        return context


class NaughtyStepView(TemplateView):
    """ Table of all players who have received cards, ordered by:
        i) most red cards
        ii) most yellow cards
        iii) most green cards
    """

    template_name = 'matches/naughty_step.html'

    def get_context_data(self, **kwargs):
        context = super(NaughtyStepView, self).get_context_data(**kwargs)

        query = Q(red_card=True) | Q(yellow_card=True) | Q(green_card=True)
        card_apps = Appearance.objects.select_related(
            'match', 'member').filter(query).order_by('match__date')

        players = {}
        for app in card_apps:
            if app.member not in players:
                players[app.member] = NaughtyPlayer(app.member)
            players[app.member].add_appearance(app)

        # Cumulative sort in ascending order of priority
        # (first by green, then by yellow then by red)
        players = sorted(players.values(), key=lambda p: len(
            p.green_cards), reverse=True)
        players = sorted(players, key=lambda p: len(
            p.yellow_cards), reverse=True)
        players = sorted(players, key=lambda p: len(p.red_cards), reverse=True)
        context['players'] = players
        return context


class NaughtyPlayer(object):
    """ Encapsulates a member who has received at least one card. """

    def __init__(self, member):
        self.member = member
        self.red_cards = []
        self.yellow_cards = []
        self.green_cards = []

    def add_appearance(self, appearance):
        """ Adds the cards from an appearance to the running totals for this member."""
        if appearance.member != self.member:
            raise AssertionError(
                "This appearance, {}, does not relate to {}.".format(appearance, self.member))
        if appearance.red_card:
            self.red_cards.append(appearance)
        elif appearance.yellow_card:
            self.yellow_cards.append(appearance)
        elif appearance.green_card:
            self.green_cards.append(appearance)


class AccidentalTouristSeasonView(TemplateView):
    """ View for displaying the Accidental Tourist (total miles travelled)
        stats for a particular season
    """
    template_name = 'matches/accidental_tourist.html'

    def get_goalking_list(self, season):
        """ Returns a list of GoalKing items for the specified season. """

        # We convert the queryset to a list so we can add a 'rank' attribute to each item
        goalking_list = list(GoalKing.objects.accidental_tourist(season).filter(games_played__gt=0).select_related(
            'member'))

        # Apply ranking
        if len(goalking_list) > 0:
            m_list = [x for x in goalking_list if x.member.gender ==
                      Gender.Male]
            l_list = [x for x in goalking_list if x.member.gender ==
                      Gender.Female]
            self.apply_ranking(m_list)
            self.apply_ranking(l_list)

        return goalking_list

    def apply_ranking(self, goalking_list):
        """ Adds a rank attribute to each GoalKing instance in the given list.
            based on the total number of miles travelled by that person.
        """
        if len(goalking_list) == 0:
            return
        rank = 1
        previous = goalking_list[0]
        previous.rank = 1
        for i, entry in enumerate(goalking_list[1:]):
            if entry.total_miles != previous.total_miles:
                rank = i + 2
                entry.rank = str(rank)
            else:
                entry.rank = "%s=" % rank
                previous.rank = entry.rank
            previous = entry

    def get_context_data(self, **kwargs):
        """ Gets the context data for the view.

            In addition to the 'goalking_list' item, the following are also added to the context:
            - season:               the season these stats applies to
            - season_list:          a list of all seasons
        """
        context = super(AccidentalTouristSeasonView,
                        self).get_context_data(**kwargs)
        season = get_season_from_kwargs(kwargs)

        context['goalking_list'] = self.get_goalking_list(season)

        add_season_selector(context, season, Season.objects.reversed())

        return context
