"""
GraphQL Schema for Venues
"""

import graphene
from geoposition.fields import GeopositionField
from graphene_django_extras.converter import convert_django_field
from graphene_django_extras.utils import is_required
from graphene_django_extras import DjangoListObjectType, DjangoObjectType
from graphene_django_optimizedextras import OptimizedDjangoListObjectField, get_paginator
from .models import Venue


@convert_django_field.register(GeopositionField)
def convert_geofield_to_string(field, registry=None, input_flag=None, nested_fields=False):
    return graphene.String(description=field.help_text or field.verbose_name,
                           required=is_required(field) and input_flag == 'create')


class VenueType(DjangoObjectType):
    """ GraphQL node representing a match venue """

    class Meta:
        model = Venue
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'matches__division': ['exact'],
            'matches__season__slug': ['exact'],
            'matches__our_team__slug': ['exact'],
            'is_home': ['exact'],
        }


class VenueList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of venues"
        model = Venue
        pagination = get_paginator()


class Query(graphene.ObjectType):
    """ GraphQL query for venues """
    venues = OptimizedDjangoListObjectField(VenueList)
