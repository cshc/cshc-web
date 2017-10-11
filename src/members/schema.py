"""
GraphQL Schema for Members etc
"""

import graphene
from graphene_django import DjangoObjectType
from .models import CommitteePosition, Member, CommitteeMembership, SquadMembership


class CommitteePositionType(DjangoObjectType):
    """ GraphQL node representing a committee position """
    class Meta:
        model = CommitteePosition


class CommitteeMembershipType(DjangoObjectType):
    """ GraphQL node representing a committee membership """
    class Meta:
        model = CommitteeMembership


class SquadMembershipType(DjangoObjectType):
    """ GraphQL node representing a member's squad membership """
    class Meta:
        model = SquadMembership


class MemberType(DjangoObjectType):
    """ GraphQL node representing a club member """
    class Meta:
        model = Member


class Query(graphene.ObjectType):
    """ GraphQL query for members etc """
    committee_positions = graphene.List(CommitteePositionType)
    committee_memberships = graphene.List(CommitteeMembershipType)
    squad_memberships = graphene.List(SquadMembershipType)
    members = graphene.List(MemberType)

    def resolve_committee_positions(self):
        return CommitteePosition.objects.all()

    def resolve_committee_memberships(self):
        return CommitteeMembership.objects.all()

    def resolve_squad_memberships(self):
        return SquadMembership.objects.all()

    def resolve_members(self):
        return Member.objects.all()
