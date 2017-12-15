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


class MatchAwardNode(DjangoObjectType):
    """ GraphQL node representing a match award """
    class Meta:
        model = MatchAward
        interfaces = (graphene.relay.Node, )


class MatchAwardConnection(graphene.relay.Connection):
    class Meta:
        node = MatchAwardNode


class EndOfSeasonAwardNode(DjangoObjectType):
    """ GraphQL node representing an end-of-season award """
    class Meta:
        model = EndOfSeasonAward
        interfaces = (graphene.relay.Node, )


class EndOfSeasonAwardConnection(graphene.relay.Connection):
    class Meta:
        node = EndOfSeasonAwardNode


class MatchAwardConnection(graphene.relay.Connection):
    class Meta:
        node = MatchAwardNode


class MatchAwardWinnerNode(DjangoObjectType):
    """ GraphQL node representing a match award winner """
    class Meta:
        model = MatchAwardWinner
        interfaces = (graphene.relay.Node, )
        filter_fields = ['match__id']

    def prefetch_member(queryset, related_queryset):
        return queryset.select_related('member')

    def prefetch_match(queryset, related_queryset):
        return queryset.select_related('match')

    def prefetch_award(queryset, related_queryset):
        return queryset.select_related('award')


class MatchAwardWinnerConnection(graphene.relay.Connection):
    class Meta:
        node = MatchAwardWinnerNode


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

    def prefetch_member(queryset, related_queryset):
        return queryset.select_related('member')

    def prefetch_season(queryset, related_queryset):
        return queryset.select_related('season')

    def prefetch_award(queryset, related_queryset):
        return queryset.select_related('award')


class EndOfSeasonAwardWinnerConnection(graphene.relay.Connection):
    class Meta:
        node = MatchAwardWinnerNode


class Query(graphene.ObjectType):
    """ GraphQL query for awards and award winners """
    match_awards = graphene.List(MatchAwardNode)
    end_of_season_awards = graphene.List(EndOfSeasonAwardNode)
    match_award_winners = graphene.List(MatchAwardWinnerNode)
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
