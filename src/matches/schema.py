"""
GraphQL Schema for matches etc
"""

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Prefetch
from core import schema_helper
from awards.models import MatchAwardWinner
from .models import Match, Appearance, GoalKing

match_field_map = {
    "venue": ("venue", "select"),
    "ourTeam": ("our_team", "select"),
    "oppTeam": ("opp_team__club", "select"),
    "awardWinners": ("award_winners", "prefetch"),
    "players": ("players", "prefetch"),
}


class MatchNode(DjangoObjectType):
    """ GraphQL node representing a match/fixture """
    class Meta:
        model = Match
        interfaces = (graphene.relay.Node, )
        filter_fields = ['venue__name', 'opp_team__name']


class AppearanceType(DjangoObjectType):
    """ GraphQL node representing a member's appearance in a match """
    class Meta:
        model = Appearance


class GoalKingType(DjangoObjectType):
    """ GraphQL node representing an entry in the Goal King stats """
    class Meta:
        model = GoalKing


class Query(graphene.ObjectType):
    """ GraphQL query for members etc """
    matches = schema_helper.OptimizableFilterConnectionField(MatchNode)
    appearances = graphene.List(AppearanceType)
    goal_king_entries = graphene.List(GoalKingType)

    def resolve_matches(self, info, **kwargs):
        appearancesQS = Appearance.objects.select_related('member')
        appearancesPrefetch = Prefetch('appearances', queryset=appearancesQS)
        awardWinnersQS = MatchAwardWinner.objects.select_related(
            'member', 'award')
        awardWinnerPrefetch = Prefetch(
            'award_winners', queryset=awardWinnersQS)
        return Match.objects.filter(**kwargs).select_related('our_team', 'opp_team__club', 'venue').prefetch_related(appearancesPrefetch, awardWinnerPrefetch)
        # return schema_helper.optimize(Match.objects.filter(**kwargs),
        #                               info,
        #                               match_field_map)

    def resolve_appearances(self):
        return Appearance.objects.all()

    def resolve_goal_king_entries(self):
        return GoalKing.objects.all()
