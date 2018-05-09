"""
Views related to matches
"""
import logging
from functools import reduce
from braces.views import SelectRelatedMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, TemplateView
from django.db.models import Q
from awards.models import MatchAward
from competitions.models import Season
from competitions.views import js_divisions, js_seasons
from core.models import ClubInfo, Gender, TeamGender
from core.views import get_season_from_kwargs, add_season_selector, kwargs_or_none, MemberSelectionMixin
from teams.models import ClubTeam
from teams.views import js_clubteams
from opposition.views import js_opposition_clubs
from venues.views import js_venues
from members.views import js_members
from members.models import Member
from .models import Match, GoalKing, Appearance


LOG = logging.getLogger(__name__)


class MatchListView(TemplateView):
    """ A view of all matches - paginated, filterable, sortable"""
    template_name = 'matches/match_list.html'

    def get_context_data(self, **kwargs):
        context = super(MatchListView, self).get_context_data(**kwargs)
        context['props'] = {
            'teams': js_clubteams(),
            'divisions': js_divisions(),
            'opposition_clubs': js_opposition_clubs(),
            'seasons': js_seasons(),
            'venues': js_venues(),
            'members': js_members(),
        }
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

        # Get all the other matches on this date
        same_date_matches_qs = Match.objects.select_related('our_team', 'opp_team__club').filter(
            date=match.date).exclude(pk=match.pk).order_by('our_team__position')

        # Group other matches by team gender
        same_date_matches = []
        for other_match in same_date_matches_qs:
            if len(same_date_matches) > 0 and other_match.our_team.get_gender_display() == same_date_matches[-1]['gender']:
                same_date_matches[-1]['matches'].append(other_match)
            else:
                same_date_matches.append(
                    dict(gender=other_match.our_team.get_gender_display(), matches=[other_match]))

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

        if match.our_team.slug == 'indoor':
            context['background_image_full'] = "img/matches/indoor.jpg"
        else:
            context['background_image_full'] = "img/matches/{}.jpg".format(
                match.our_team.gender.lower())

        if not match.is_in_past():
            context['props'] = {
                'matchId': match.id,
                'ourTeam': {
                    'slug': match.our_team.slug,
                    'longName': match.our_team.long_name,
                },
                'oppTeam': {
                    'name': match.opp_team.name,
                    'club': {
                        'slug': match.opp_team.club.slug,
                        'name': match.opp_team.club.name,
                    },
                },
                'matchFilters': {
                    'pageSize': 5,
                    'orderBy': '-date',
                    'date_Lt': str(match.date),
                    'ourTeamId': match.our_team_id,
                    'oppTeamId': match.opp_team_id,
                },
            }
        return context


class MatchEditView(PermissionRequiredMixin, SelectRelatedMixin, MemberSelectionMixin, DetailView):
    """ View providing a form for editing a particular match's details """
    model = Match
    template_name = 'matches/match_edit.html'
    permission_required = (
        'matches.change_match',
        'matches.add_appearance',
        'matches.change_appearance',
        'awards.add_matchawardwinner',
        'awards.change_matchawardwinner')
    select_related = ['our_team', 'opp_team__club',
                      'venue', 'division__league', 'cup', 'season']

    def encode_cards(self, appearance):
        """ Encode the cards associated with an appearance as a comma-separated list (e.g. 'g,y') """
        cards = []
        if appearance.green_card:
            cards.append('g')
        if appearance.yellow_card:
            cards.append('y')
        if appearance.red_card:
            cards.append('r')
        return ",".join(cards)

    def list_appearances(self, match):
        """ Get a JS-friendly list of appearances for this match """
        appearances_qs = match.appearances.select_related(
            'member').order_by('member__first_name', 'member__last_name')
        appearances = []
        for appearance in appearances_qs:
            appearances.append({
                'member': self.encode_member(appearance.member),
                'cards': self.encode_cards(appearance),
                'goals': appearance.goals,
            })
        return appearances

    def list_award_winners(self, match):
        """ Get a JS-friendly list of award-winners for this match """
        award_winners_qs = match.award_winners.select_related(
            'member', 'award').order_by('-award__name')
        awards = []
        for award_winner in award_winners_qs:
            # We use a string ID as we create dummy id strings on the front-end for 'new' award winners
            # which we identify by prefixing with 'new-'.
            awards.append({
                'id': str(award_winner.id),
                'member': self.encode_member(award_winner.member),
                'awardee': award_winner.awardee,
                'comment': award_winner.comment,
                'award': award_winner.award.name,
            })
        return awards

    def get_context_data(self, **kwargs):
        context = super(MatchEditView, self).get_context_data(**kwargs)
        match = context["match"]

        member_fields = ['id', 'first_name', 'last_name', 'gender']
        player_suggestions = []

        # 1. Get all possible members
        member_qs = Member.objects.filter(is_current=True)
        if match.our_team.gender == TeamGender.Mens:
            member_qs = member_qs.filter(gender=Gender.Male)
        elif match.our_team.gender == TeamGender.Ladies:
            member_qs = member_qs.filter(gender=Gender.Female)
        else:
            member_qs = member_qs.order_by('gender')

        player_suggestions = self.to_player_list(
            member_qs.only(*member_fields))

        # 2. Get members who have played in this team before this season
        played_this_season_qs = Member.objects.filter(
            appearances__match__season_id=match.season_id,
            appearances__match__our_team_id=match.our_team_id).order_by(
                '-first_name', '-last_name').only(*member_fields)

        played_this_season = self.to_player_list(played_this_season_qs)

        for player in played_this_season:
            self.prioritize(player_suggestions, player)

        # 3. Get members who are in the squad
        squad_members_qs = Member.objects.filter(squadmembership__team_id=match.our_team_id,
                                                 squadmembership__season_id=match.season_id).order_by('-first_name', '-last_name').only(*member_fields)

        squad_members = self.to_player_list(squad_members_qs)

        for player in squad_members:
            self.prioritize(player_suggestions, player)

        # 4. Get members who played in the last match
        last_match_players = []
        try:
            last_match = Match.objects.filter(our_team_id=match.our_team_id,
                                              date__lt=match.date).order_by('-date').first()

            last_match_player_qs = Member.objects.filter(
                appearances__match_id=last_match.id).order_by('-first_name', '-last_name').only(*member_fields)

            last_match_players = self.to_player_list(last_match_player_qs)
        except Match.DoesNotExist:
            pass

        for player in last_match_players:
            self.prioritize(player_suggestions, player)

        context['props'] = {
            'matchId': match.id,
            'ourTeamGender': match.our_team.gender.upper(),
            'ourTeam': match.our_team.abbr_name(),
            'oppTeam': match.opp_team.name,
            'matchState': {
                'playerOptions': player_suggestions,
                'result': {
                    'errors': [],
                    'ourScore': match.our_score,
                    'oppScore': match.opp_score,
                    'ourHtScore': match.our_ht_score,
                    'oppHtScore': match.opp_ht_score,
                    'altOutcome': match.get_alt_outcome_display(),
                },
                'appearances': self.list_appearances(match),
                'awardWinners': self.list_award_winners(match),
                'report': {
                    'author': self.encode_member(match.report_author),
                    'title': match.report_title,
                    'content': match.report_body.content,
                },
            },
        }
        return context


class GoalKingView(TemplateView):
    """ View for displaying the Goal King stats for a particular season. """
    template_name = 'matches/goalking.html'

    def get_context_data(self, **kwargs):
        context = super(GoalKingView, self).get_context_data(**kwargs)
        context['props'] = {
            'seasons':  list(GoalKing.objects.order_by('-season').values_list('season__slug', flat=True).distinct()),
            'teams': list(ClubTeam.objects.active().values('long_name', 'slug')),
            'current_season': Season.current().slug,
        }
        return context


class NaughtyStepSeasonView(TemplateView):
    """ Table of all players who have received cards, ordered by:
        i) most red cards
        ii) most yellow cards
        iii) most green cards
    """

    template_name = 'matches/naughty_step.html'

    def get_context_data(self, **kwargs):
        context = super(NaughtyStepSeasonView, self).get_context_data(**kwargs)

        query = Q(red_card=True) | Q(yellow_card=True) | Q(green_card=True)
        qs = Appearance.objects.select_related('match', 'member').filter(query)

        season_slug = kwargs_or_none('season_slug', **kwargs)
        if season_slug is not None:
            qs = qs.filter(match__season__slug=season_slug)

        card_apps = qs.order_by('match__date')

        season_list = list(Appearance.objects.filter(
            query).order_by('-match__date').values_list('match__season__slug', flat=True))

        seasons = reduce(lambda l, x: l +
                         [x] if x not in l else l, season_list, [])

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

        context['season_slug'] = season_slug if season_slug else 'All seasons'
        context['season_slug_list'] = ['All seasons'] + seasons
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

        context['max_miles'] = context['goalking_list'][0].total_miles if context['goalking_list'] else 0

        season_slug_list = list(GoalKing.objects.order_by(
            '-season').values_list('season__slug', flat=True).distinct())

        add_season_selector(context, season, season_slug_list)

        return context
