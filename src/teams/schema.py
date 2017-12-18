"""
GraphQL Schema for Club Teams etc
"""

import graphene
from core.cursor import PageableDjangoObjectType
from .models import ClubTeam, ClubTeamSeasonParticipation, TeamCaptaincy


class ClubTeamNode(PageableDjangoObjectType):
    """ GraphQL node representing a club team """
    genderless_abbr_name = graphene.String()

    def resolve_genderless_abbr_name(self, info):
        return self.genderless_abbr_name()

    class Meta:
        model = ClubTeam
        interfaces = (graphene.relay.Node, )


class ClubTeamSeasonParticipationNode(PageableDjangoObjectType):
    """ GraphQL node representing a club team's participation in a division in a particular season """
    class Meta:
        model = ClubTeamSeasonParticipation
        interfaces = (graphene.relay.Node, )


class TeamCaptaincyNode(PageableDjangoObjectType):
    """ GraphQL node representing a club team (vice-)captaincy for a particular team and season """
    class Meta:
        model = TeamCaptaincy
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    """ GraphQL query for club teams etc """
    club_teams = graphene.List(ClubTeamNode)
    participations = graphene.List(ClubTeamSeasonParticipationNode)
    captaincies = graphene.List(TeamCaptaincyNode)

    def resolve_club_teams(self, info):
        return ClubTeam.objects.all()

    def resolve_participations(self):
        return ClubTeamSeasonParticipation.objects.all()

    def resolve_captaincies(self):
        return TeamCaptaincy.objects.all()
