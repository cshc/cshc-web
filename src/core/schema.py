"""
GraphQL Schema for Core models
"""

import graphene
from .cursor import PageableDjangoObjectType
from .models import CshcUser, ClubInfo


class CshcUserType(PageableDjangoObjectType):
    """ GraphQL node representing a CSHC user """
    class Meta:
        model = CshcUser


class ClubInfoType(PageableDjangoObjectType):
    """ GraphQL node representing a club info entry """
    class Meta:
        model = ClubInfo


class Query(graphene.ObjectType):
    """ GraphQL query for Core models """
    users = graphene.List(CshcUserType)
    all_club_info = graphene.List(ClubInfoType)

    def resolve_users(self):
        return CshcUser.objects.all()

    def resolve_all_club_info(self):
        return ClubInfo.objects.all()
