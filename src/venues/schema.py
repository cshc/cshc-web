"""
GraphQL Schema for Venues
"""

import graphene
from geoposition.fields import GeopositionField
from graphene_django_extras.converter import convert_django_field
from graphene_django_extras.utils import is_required
from graphene_django_extras import DjangoListObjectType, DjangoObjectType
from graphene_django_optimizedextras import OptimizedDjangoListObjectField, get_paginator
from core.filters import AndFilter
from .models import Venue


@convert_django_field.register(GeopositionField)
def convert_geofield_to_string(field, registry=None, input_flag=None, nested_fields=False):
    return graphene.String(description=field.help_text or field.verbose_name,
                           required=is_required(field) and input_flag == 'create')


class VenueFilter(AndFilter):

    class Meta:
        model = Venue
        fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'matches__division_id': ['exact'],
            'matches__season__slug': ['exact'],
            'matches__our_team__slug': ['exact'],
            'is_home': ['exact'],
        }


class VenueType(DjangoObjectType):
    """ GraphQL node representing a match venue """

    class Meta:
        model = Venue


class VenueList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of venues"
        model = Venue
        pagination = get_paginator()


# We're forced to call distinct() on the queryset as we're filtering
# on manytomany related fields and it returns duplicate entries
def post_optimize_venues(queryset, **kwargs):
    return queryset.distinct()


class Query(graphene.ObjectType):
    """ GraphQL query for venues """
    venues = OptimizedDjangoListObjectField(
        VenueList, filterset_class=VenueFilter, post_optimize=post_optimize_venues)
