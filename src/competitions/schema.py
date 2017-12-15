"""
GraphQL Schema for Competitions
"""

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from core import schema_helper
from .models import Season, League, Division, Cup, DivisionResult

division_field_map = {
    "league": ("league", "select"),
}


class SeasonNode(DjangoObjectType):
    """ GraphQL node representing a season """
    model_id = graphene.String()

    def resolve_model_id(self, info):
        return self.id

    class Meta:
        model = Season
        interfaces = (graphene.relay.Node, )
        filter_fields = ['slug']


class SeasonConnection(graphene.relay.Connection):
    class Meta:
        node = SeasonNode


class DivisionNode(DjangoObjectType):
    """ GraphQL node representing a division """
    model_id = graphene.String()

    def resolve_model_id(self, info):
        return self.id

    class Meta:
        model = Division
        interfaces = (graphene.relay.Node, )
        filter_fields = ['name', 'league__name']

    def prefetch_league(queryset, related_queryset):
        return queryset.select_related('league')


class DivisionConnection(graphene.relay.Connection):
    class Meta:
        node = DivisionNode


class LeagueNode(DjangoObjectType):
    """ GraphQL node representing a league """
    class Meta:
        model = League
        interfaces = (graphene.relay.Node, )
        filter_fields = ['name']

    divisions = schema_helper.OptimizableFilterConnectionField(DivisionNode)

    def resolve_divisions(self, info, *args):
        return schema_helper.optimize(Division.objects.filter(league=self, *args),
                                      info,
                                      division_field_map)


class LeagueConnection(graphene.relay.Connection):
    class Meta:
        node = LeagueNode


class CupNode(DjangoObjectType):
    """ GraphQL node representing a cup """
    class Meta:
        model = Cup
        interfaces = (graphene.relay.Node, )
        filter_fields = ['name', 'league__name']

    def prefetch_league(queryset, related_queryset):
        return queryset.select_related('league')


class CupConnection(graphene.relay.Connection):
    class Meta:
        node = CupNode


class DivisionResultNode(DjangoObjectType):
    """ GraphQL node representing an entry in a league table """
    team_name = graphene.String()

    def resolve_team_name(self, info):
        return self.team_name

    class Meta:
        model = DivisionResult
        interfaces = (graphene.relay.Node, )
        filter_fields = ['season__slug', 'division__id', 'season_id']


class Query(graphene.ObjectType):
    """ GraphQL query for competitions """
    season = graphene.Node.Field(SeasonNode)
    league = graphene.Node.Field(LeagueNode)
    division = graphene.Node.Field(DivisionNode)
    cup = graphene.Node.Field(CupNode)
    division_result = graphene.Node.Field(DivisionResultNode)

    seasons = DjangoFilterConnectionField(SeasonNode)
    leagues = schema_helper.OptimizableFilterConnectionField(LeagueNode)
    divisions = schema_helper.OptimizableFilterConnectionField(DivisionNode)
    cups = DjangoFilterConnectionField(CupNode)
    division_results = DjangoFilterConnectionField(
        DivisionResultNode, ['division__name', 'division__id', 'season__id'])

    def resolve_divisions(self, info, **kwargs):
        return schema_helper.optimize(Division.objects.filter(**kwargs),
                                      info,
                                      division_field_map)
    # def resolve_seasons(self):
    #     return Season.objects.all()

    # def resolve_leagues(self):
    #     return League.objects.all()

    # def resolve_divisions(self):
    #     return Division.objects.all()

    # def resolve_cups(self):
    #     return Cup.objects.all()
