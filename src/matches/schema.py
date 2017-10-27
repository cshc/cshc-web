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


class MatchNode(DjangoObjectType):
    """ GraphQL node representing a match/fixture """
    model_id = graphene.String()
    has_report = graphene.Boolean()
    kit_clash = graphene.Boolean()

    class Meta:
        model = Match
        interfaces = (graphene.relay.Node, )
        filter_fields = ['venue__name', 'opp_team__name',
                         'our_team__slug', 'season__slug']

    def resolve_model_id(self, info):
        return self.id

    def resolve_has_report(self, info):
        return self.has_report()

    def resolve_kit_clash(self, info):
        return self.kit_clash()


class AppearanceNode(DjangoObjectType):
    """ GraphQL node representing a member's appearance in a match """
    class Meta:
        model = Appearance
        # interfaces = (graphene.relay.Node, )
        # filter_fields = {
        #     'goals': ['gte'],
        # }


class GoalKingType(DjangoObjectType):
    """ GraphQL node representing an entry in the Goal King stats """
    class Meta:
        model = GoalKing


class Query(graphene.ObjectType):
    """ GraphQL query for members etc """
    matches = schema_helper.OptimizableFilterConnectionField(MatchNode)
    appearances = graphene.List(AppearanceNode)
    goal_king_entries = graphene.List(GoalKingType)

    def resolve_matches(self, info, **kwargs):
        appearances_qs = Appearance.objects.select_related('member')
        appearances_prefetch = Prefetch('appearances', queryset=appearances_qs)
        award_winners_qs = MatchAwardWinner.objects.select_related(
            'member', 'award')
        award_winner_prefetch = Prefetch(
            'award_winners', queryset=award_winners_qs)
        return Match.objects.filter(**kwargs).select_related('our_team', 'opp_team__club', 'venue').prefetch_related(appearances_prefetch, award_winner_prefetch)

    def resolve_appearances(self):
        return Appearance.objects.all()

    def resolve_goal_king_entries(self):
        return GoalKing.objects.all()
