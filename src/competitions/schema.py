"""
GraphQL Schema for Competitions
"""

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from core import schema_helper
from .models import Season, League, Division, Cup

division_field_map = {
    "league": ("league", "select"),
}


class SeasonNode(DjangoObjectType):
    """ GraphQL node representing a season """
    class Meta:
        model = Season
        interfaces = (graphene.Node, )
        filter_fields = ['slug']


class DivisionNode(DjangoObjectType):
    """ GraphQL node representing a division """
    class Meta:
        model = Division
        interfaces = (graphene.Node, )
        filter_fields = ['name', 'league__name']


class LeagueNode(DjangoObjectType):
    """ GraphQL node representing a league """
    class Meta:
        model = League
        interfaces = (graphene.Node, )
        filter_fields = ['name']

    divisions = schema_helper.OptimizableFilterConnectionField(DivisionNode)

    def resolve_divisions(self, info, *args):
        return schema_helper.optimize(Division.objects.filter(league=self, *args),
                                      info,
                                      division_field_map)


class CupNode(DjangoObjectType):
    """ GraphQL node representing a cup """
    class Meta:
        model = Cup
        interfaces = (graphene.Node, )
        filter_fields = ['name', 'league__name']


class Query(graphene.ObjectType):
    """ GraphQL query for competitions """
    season = graphene.Node.Field(SeasonNode)
    league = graphene.Node.Field(LeagueNode)
    division = graphene.Node.Field(DivisionNode)
    cup = graphene.Node.Field(CupNode)

    seasons = DjangoFilterConnectionField(SeasonNode)
    leagues = schema_helper.OptimizableFilterConnectionField(LeagueNode)
    divisions = schema_helper.OptimizableFilterConnectionField(DivisionNode)
    cups = DjangoFilterConnectionField(CupNode)

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
