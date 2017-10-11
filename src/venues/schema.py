"""
GraphQL Schema for Venues
"""

import graphene
from graphene_django import DjangoObjectType
from .models import Venue

from graphene_django.converter import convert_django_field, convert_field_to_string
from geoposition.fields import GeopositionField


@convert_django_field.register(GeopositionField)
def convert_geofield_to_string(field, registry=None):
    return graphene.String(description=field.help_text, required=not field.null)


class VenueType(DjangoObjectType):
    """ GraphQL node representing a match venue """
    class Meta:
        model = Venue


class Query(graphene.ObjectType):
    """ GraphQL query for venues """
    venues = graphene.List(VenueType)

    def resolve_venues(self):
        return Venue.objects.all()
