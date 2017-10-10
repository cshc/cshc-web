"""
GraphQL Schema for Club Teams etc
"""

import graphene
from graphene_django import DjangoObjectType
from .models import ClubTeam, ClubTeamSeasonParticipation, TeamCaptaincy


class ClubTeamType(DjangoObjectType):
    """ GraphQL node representing a club team """
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


class Query(graphene.AbstractType):
    """ GraphQL query for club teams etc """
    club_teams = graphene.List(ClubTeamType)
    participations = graphene.List(ClubTeamSeasonParticipationType)
    captaincies = graphene.List(TeamCaptaincyType)

    @graphene.resolve_only_args
    def resolve_club_teams(self):
        return ClubTeam.objects.all()

    @graphene.resolve_only_args
    def resolve_participations(self):
        return ClubTeamSeasonParticipation.objects.all()

    @graphene.resolve_only_args
    def resolve_captaincies(self):
        return TeamCaptaincy.objects.all()
