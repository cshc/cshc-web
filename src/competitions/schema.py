"""
GraphQL Schema for Competitions
"""

import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django_extras import DjangoListObjectType, DjangoObjectType
from graphene_django_optimizedextras import OptimizedDjangoListObjectField, get_paginator
from .models import Season, League, Division, Cup, DivisionResult


class SeasonType(DjangoObjectType):
    """ GraphQL node representing a season """
    class Meta:
        model = Season
        filter_fields = ['slug']


class SeasonList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a season list "
        model = Season
        pagination = get_paginator()


class DivisionType(DjangoObjectType):
    """ GraphQL node representing a division """
    class Meta:
        model = Division
        filter_fields = ['name', 'league__name']


class DivisionList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a division list "
        model = Division
        pagination = get_paginator()


class LeagueType(DjangoObjectType):
    """ GraphQL node representing a league """
    class Meta:
        model = League
        filter_fields = ['name']

    divisions = OptimizedDjangoListObjectField(DivisionList)


class LeagueList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a league list "
        model = League
        pagination = get_paginator()


class CupType(DjangoObjectType):
    """ GraphQL node representing a cup """
    class Meta:
        model = Cup
        filter_fields = ['name', 'league__name']


class CupList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a cup list "
        model = Cup
        pagination = get_paginator()


class DivisionResultType(DjangoObjectType):
    """ GraphQL node representing an entry in a league table """
    team_name = graphene.String()

    def resolve_team_name(self, info):
        return self.team_name

    class Meta:
        model = DivisionResult
        filter_fields = ['season__slug', 'division_id', 'season_id']


class DivisionResultList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a division result list "
        model = DivisionResult
        pagination = get_paginator()


class Query(graphene.ObjectType):
    """ GraphQL query for competitions """
    seasons = OptimizedDjangoListObjectField(SeasonList)
    leagues = OptimizedDjangoListObjectField(LeagueList)
    divisions = OptimizedDjangoListObjectField(DivisionList)
    cups = OptimizedDjangoListObjectField(CupList)
    division_results = OptimizedDjangoListObjectField(DivisionResultList)
