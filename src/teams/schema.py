"""
GraphQL Schema for Club Teams etc
"""

import graphene
from graphene_django import DjangoObjectType
from .models import ClubTeam, ClubTeamSeasonParticipation, TeamCaptaincy


class ClubTeamType(DjangoObjectType):
    """ GraphQL node representing a club team """
    genderless_abbr_name = graphene.String()

    def resolve_genderless_abbr_name(self, info):
        return self.genderless_abbr_name()

    class Meta:
        model = ClubTeam


class ClubTeamSeasonParticipationType(DjangoObjectType):
    """ GraphQL node representing a club team's participation in a division in a particular season """
    class Meta:
        model = ClubTeamSeasonParticipation


class TeamCaptaincyType(DjangoObjectType):
    """ GraphQL node representing a club team (vice-)captaincy for a particular team and season """
    class Meta:
        model = TeamCaptaincy


class Query(graphene.ObjectType):
    """ GraphQL query for club teams etc """
    club_teams = graphene.List(ClubTeamType)
    participations = graphene.List(ClubTeamSeasonParticipationType)
    captaincies = graphene.List(TeamCaptaincyType)

    def resolve_club_teams(self):
        return ClubTeam.objects.all()

    def resolve_participations(self):
        return ClubTeamSeasonParticipation.objects.all()

    def resolve_captaincies(self):
        return TeamCaptaincy.objects.all()
