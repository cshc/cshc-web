"""
GraphQL Schema for Club Teams etc
"""

import graphene
from graphene_django_extras import DjangoListObjectType, DjangoObjectType
from graphene_django_optimizedextras import OptimizedDjangoListObjectField, get_paginator
from core.filters import AndFilter
from .models import ClubTeam, ClubTeamSeasonParticipation, TeamCaptaincy


class ClubTeamSeasonParticipationFilter(AndFilter):

    class Meta:
        model = ClubTeamSeasonParticipation
        exclude = ['team_photo', 'team_photo_cropping']


class ClubTeamType(DjangoObjectType):
    """ GraphQL node representing a club team """
    genderless_abbr_name = graphene.String()

    def resolve_genderless_abbr_name(self, info):
        return self.genderless_abbr_name()

    class Meta:
        model = ClubTeam


class ClubTeamList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of club teams"
        model = ClubTeam
        pagination = get_paginator()


class ClubTeamSeasonParticipationType(DjangoObjectType):
    """ GraphQL node representing a club team's participation in a division in a particular season """
    class Meta:
        model = ClubTeamSeasonParticipation


class ClubTeamSeasonParticipationList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of club team season participations"
        model = ClubTeamSeasonParticipation
        pagination = get_paginator()


class TeamCaptaincyType(DjangoObjectType):
    """ GraphQL node representing a club team (vice-)captaincy for a particular team and season """
    class Meta:
        model = TeamCaptaincy


class TeamCaptaincyList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of team captaincies"
        model = TeamCaptaincy
        pagination = get_paginator()


class Query(graphene.ObjectType):
    """ GraphQL query for club teams etc """
    club_teams = OptimizedDjangoListObjectField(ClubTeamList)

    participations = OptimizedDjangoListObjectField(
        ClubTeamSeasonParticipationList, filterset_class=ClubTeamSeasonParticipationFilter)

    captaincies = OptimizedDjangoListObjectField(TeamCaptaincyList)
