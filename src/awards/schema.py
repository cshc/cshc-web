"""
GraphQL Schema for Awards and Award Winners
"""

import graphene
from graphene_django import DjangoObjectType
from core import schema_helper
from .models import MatchAward, EndOfSeasonAward, MatchAwardWinner, EndOfSeasonAwardWinner

end_of_season_award_winner_field_map = {
    "member": ("member", "select"),
    "season": ("season", "select"),
    "award": ("award", "select"),
}


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


class EndOfSeasonAwardWinnerNode(DjangoObjectType):
    """ GraphQL node representing an end-of-season award winner """
    class Meta:
        model = EndOfSeasonAwardWinner
        interfaces = (graphene.relay.Node, )
        filter_fields = {
            'member__id': ['exact'],
            'season__slug': ['exact'],
            'award__name': ['exact', 'icontains', 'istartswith'],
        }


class Query(graphene.ObjectType):
    """ GraphQL query for awards and award winners """
    match_awards = graphene.List(MatchAwardType)
    end_of_season_awards = graphene.List(EndOfSeasonAwardType)
    match_award_winners = graphene.List(MatchAwardWinnerType)
    end_of_season_award_winners = schema_helper.OptimizableFilterConnectionField(
        EndOfSeasonAwardWinnerNode)

    def resolve_match_awards(self):
        return MatchAward.objects.all()

    def resolve_end_of_season_awards(self):
        return EndOfSeasonAward.objects.all()

    def resolve_match_award_winners(self):
        return MatchAwardWinner.objects.all()

    def resolve_end_of_season_award_winners(self, info, **kwargs):
        return schema_helper.optimize(EndOfSeasonAwardWinner.objects.filter(**kwargs),
                                      info,
                                      end_of_season_award_winner_field_map)
