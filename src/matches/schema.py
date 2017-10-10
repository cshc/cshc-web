"""
GraphQL Schema for matches etc
"""

import graphene
from graphene_django import DjangoObjectType
from .models import Match, Appearance, GoalKing


class MatchType(DjangoObjectType):
    """ GraphQL node representing a match/fixture """
    class Meta:
        model = Match


class AppearanceType(DjangoObjectType):
    """ GraphQL node representing a member's appearance in a match """
    class Meta:
        model = Appearance


class GoalKingType(DjangoObjectType):
    """ GraphQL node representing an entry in the Goal King stats """
    class Meta:
        model = GoalKing


class Query(graphene.AbstractType):
    """ GraphQL query for members etc """
    matches = graphene.List(MatchType)
    appearances = graphene.List(AppearanceType)
    goal_king_entries = graphene.List(GoalKingType)

    @graphene.resolve_only_args
    def resolve_matches(self):
        return Match.objects.all()

    @graphene.resolve_only_args
    def resolve_appearances(self):
        return Appearance.objects.all()

    @graphene.resolve_only_args
    def resolve_goal_king_entries(self):
        return GoalKing.objects.all()
