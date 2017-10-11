"""
GraphQL Schema for Awards and Award Winners
"""

import graphene
from graphene_django import DjangoObjectType
from .models import MatchAward, EndOfSeasonAward, MatchAwardWinner, EndOfSeasonAwardWinner


class MatchAwardType(DjangoObjectType):
    """ GraphQL node representing a match award """
    class Meta:
        model = MatchAward


class EndOfSeasonAwardType(DjangoObjectType):
    """ GraphQL node representing an end-of-season award """
    class Meta:
        model = EndOfSeasonAward


class MatchAwardWinnerType(DjangoObjectType):
    """ GraphQL node representing a match award winner """
    class Meta:
        model = MatchAwardWinner


class EndOfSeasonAwardWinnerType(DjangoObjectType):
    """ GraphQL node representing an end-of-season award winner """
    class Meta:
        model = EndOfSeasonAwardWinner


class Query(graphene.ObjectType):
    """ GraphQL query for awards and award winners """
    match_awards = graphene.List(MatchAwardType)
    end_of_season_awards = graphene.List(EndOfSeasonAwardType)
    match_award_winners = graphene.List(MatchAwardWinnerType)
    end_of_season_award_winners = graphene.List(EndOfSeasonAwardWinnerType)

    def resolve_match_awards(self):
        return MatchAward.objects.all()

    def resolve_end_of_season_awards(self):
        return EndOfSeasonAward.objects.all()

    def resolve_match_award_winners(self):
        return MatchAwardWinner.objects.all()

    def resolve_end_of_season_award_winners(self):
        return EndOfSeasonAwardWinner.objects.all()
