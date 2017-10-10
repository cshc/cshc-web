"""
GraphQL Schema for Training Sessions etc
"""

import graphene
from graphene_django import DjangoObjectType
from .models import TrainingSession


class TrainingSessionType(DjangoObjectType):
    """ GraphQL node representing a training session """
    class Meta:
        model = TrainingSession


class Query(graphene.AbstractType):
    """ GraphQL query for members etc """
    training_sessions = graphene.List(TrainingSessionType)

    @graphene.resolve_only_args
    def resolve_training_sessions(self):
        return TrainingSession.objects.all()
