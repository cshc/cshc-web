"""
GraphQL Schema for Core models
"""

import graphene
from graphene_django_extras import DjangoListObjectType, DjangoObjectType
from graphene_django_optimizedextras import OptimizedDjangoListObjectField, get_paginator
from .models import CshcUser, ClubInfo


class CshcUserType(DjangoObjectType):
    """ GraphQL node representing a CSHC user """
    class Meta:
        model = CshcUser


class CshcUserList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a CSHC user list "
        model = CshcUser
        pagination = get_paginator()


class ClubInfoType(DjangoObjectType):
    """ GraphQL node representing a club info entry """
    class Meta:
        model = ClubInfo


class ClubInfoList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a club info list "
        model = ClubInfo
        pagination = get_paginator()


class Query(graphene.ObjectType):
    """ GraphQL query for Core models """
    users = OptimizedDjangoListObjectField(CshcUserList)
    all_club_info = OptimizedDjangoListObjectField(ClubInfoList)
