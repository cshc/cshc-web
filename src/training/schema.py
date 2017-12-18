"""
GraphQL Schema for Training Sessions etc
"""

import graphene
from core.cursor import PageableDjangoObjectType
from .models import TrainingSession


class TrainingSessionType(PageableDjangoObjectType):
    """ GraphQL node representing a training session """
    class Meta:
        model = TrainingSession


class Query(graphene.ObjectType):
    """ GraphQL query for members etc """
    training_sessions = graphene.List(TrainingSessionType)

    def resolve_training_sessions(self):
        return TrainingSession.objects.all()
