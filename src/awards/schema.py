"""
GraphQL Schema for Awards and Award Winners
"""

import graphene
import django_filters
from graphene_django_extras import DjangoListObjectType, DjangoObjectType
from graphene_django_optimizedextras import OptimizedDjangoListObjectField, get_paginator
from .models import MatchAward, EndOfSeasonAward, MatchAwardWinner, EndOfSeasonAwardWinner


class EndOfSeasonAwardWinnerFilter(django_filters.FilterSet):

    class Meta:
        model = EndOfSeasonAwardWinner
        fields = {
            'season__slug': ['exact'],
            'award': ['exact'],
            'member_id': ['in', 'exact'],
        }

    order_by = django_filters.OrderingFilter(
        fields=(
            ('award__name', 'award'),
            ('season__slug', 'season'),
            ('member__id', 'member'),
        )
    )


class MatchAwardType(DjangoObjectType):
    """ GraphQL node representing a match award """
    class Meta:
        model = MatchAward


class MatchAwardList(DjangoListObjectType):
    class Meta:
        description = "Type definition for match award list "
        model = MatchAward
        pagination = get_paginator()


class EndOfSeasonAwardType(DjangoObjectType):
    """ GraphQL node representing an end-of-season award """
    class Meta:
        model = EndOfSeasonAward


class EndOfSeasonAwardList(DjangoListObjectType):
    class Meta:
        description = "Type definition for end of season award list "
        model = EndOfSeasonAward
        pagination = get_paginator()


class MatchAwardWinnerType(DjangoObjectType):
    """ GraphQL node representing a match award winner """
    class Meta:
        model = MatchAwardWinner
        filter_fields = ['match__id']


class MatchAwardWinnerList(DjangoListObjectType):
    class Meta:
        description = "Type definition for match award winner list "
        model = MatchAwardWinner
        pagination = get_paginator()


class EndOfSeasonAwardWinnerType(DjangoObjectType):
    """ GraphQL node representing an end-of-season award winner """
    class Meta:
        model = EndOfSeasonAwardWinner
        filter_fields = {
            'member_id': ['exact'],
            'season__slug': ['exact'],
            'award__name': ['exact', 'icontains', 'istartswith'],
        }


class EndOfSeasonAwardWinnerList(DjangoListObjectType):
    class Meta:
        description = "Type definition for end of season award winner list "
        model = EndOfSeasonAwardWinner
        pagination = get_paginator()


class MatchAwardWinnerInput(graphene.InputObjectType):
    match_id = graphene.Int(required=False)
    member_id = graphene.Int(required=False)
    awardee = graphene.String(required=False)
    comment = graphene.String()
    award = graphene.String()


class Query(graphene.ObjectType):
    """ GraphQL query for awards and award winners """
    match_awards = OptimizedDjangoListObjectField(MatchAwardList)
    end_of_season_awards = OptimizedDjangoListObjectField(EndOfSeasonAwardList)
    match_award_winners = OptimizedDjangoListObjectField(MatchAwardWinnerList)
    end_of_season_award_winners = OptimizedDjangoListObjectField(
        EndOfSeasonAwardWinnerList, filterset_class=EndOfSeasonAwardWinnerFilter)
