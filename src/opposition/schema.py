"""
GraphQL Schema for opposition clubs and teams etc
"""

import graphene
from graphene_django import DjangoObjectType
from .models import Club, Team


class ClubType(DjangoObjectType):
    """ GraphQL node representing an opposition club """
    class Meta:
        model = Club


class TeamType(DjangoObjectType):
    """ GraphQL node representing an opposition team """
    class Meta:
        model = Team


class Query(graphene.AbstractType):
    """ GraphQL query for members etc """
    opposition_clubs = graphene.List(ClubType)
    opposition_teams = graphene.List(TeamType)

    @graphene.resolve_only_args
    def resolve_opposition_clubs(self):
        return Club.objects.all()

    @graphene.resolve_only_args
    def resolve_opposition_teams(self):
        return Team.objects.all()
