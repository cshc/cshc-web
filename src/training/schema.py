"""
GraphQL Schema for Training Sessions etc
"""

import graphene
from graphene_django_extras import DjangoListObjectType, DjangoObjectType
from graphene_django_optimizedextras import OptimizedDjangoListObjectField, get_paginator
from .models import TrainingSession


class TrainingSessionType(DjangoObjectType):
    """ GraphQL node representing a training session """
    class Meta:
        model = TrainingSession


class TrainingSessionList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of training sessions"
        model = TrainingSession
        pagination = get_paginator()


class Query(graphene.ObjectType):
    """ GraphQL query for members etc """
    training_sessions = OptimizedDjangoListObjectField(TrainingSessionList)
