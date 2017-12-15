"""
GraphQL Schema for Club Teams etc
"""

import graphene
from graphene_django import DjangoObjectType
from .models import ClubTeam, ClubTeamSeasonParticipation, TeamCaptaincy


class ClubTeamNode(DjangoObjectType):
    """ GraphQL node representing a club team """
    genderless_abbr_name = graphene.String()

    def resolve_genderless_abbr_name(self, info):
        return self.genderless_abbr_name()

    class Meta:
        model = ClubTeam
        interfaces = (graphene.relay.Node, )


class ClubTeamConnection(graphene.relay.Connection):
    class Meta:
        node = ClubTeamNode


class ClubTeamSeasonParticipationNode(DjangoObjectType):
    """ GraphQL node representing a club team's participation in a division in a particular season """
    class Meta:
        model = ClubTeamSeasonParticipation
        interfaces = (graphene.relay.Node, )

    def prefetch_team(queryset, related_queryset):
        return queryset.select_related('team')

    def prefetch_season(queryset, related_queryset):
        return queryset.select_related('season')

    def prefetch_division(queryset, related_queryset):
        return queryset.select_related('division')

    def prefetch_cup(queryset, related_queryset):
        return queryset.select_related('cup')


class ClubTeamSeasonParticipationConnection(graphene.relay.Connection):
    class Meta:
        node = ClubTeamSeasonParticipationNode


class TeamCaptaincyNode(DjangoObjectType):
    """ GraphQL node representing a club team (vice-)captaincy for a particular team and season """
    class Meta:
        model = TeamCaptaincy
        interfaces = (graphene.relay.Node, )

    def prefetch_member(queryset, related_queryset):
        return queryset.select_related('member')

    def prefetch_team(queryset, related_queryset):
        return queryset.select_related('team')

    def prefetch_season(queryset, related_queryset):
        return queryset.select_related('season')


class TeamCaptaincyConnection(graphene.relay.Connection):
    class Meta:
        node = TeamCaptaincyNode


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
