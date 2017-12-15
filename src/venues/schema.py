"""
GraphQL Schema for Venues
"""

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from core import schema_helper
from .models import Venue

from graphene_django.converter import convert_django_field, convert_field_to_string
from geoposition.fields import GeopositionField

field_map = {
    "matches": ("matches", "select"),
    "matches__division": ("matches__division", "select"),
    "amtches__season": ("amtches__season", "select"),
    "matches__our_team": ("matches__our_team", "select"),
}


@convert_django_field.register(GeopositionField)
def convert_geofield_to_string(field, registry=None):
    return graphene.String(description=field.help_text, required=not field.null)


class VenueNode(DjangoObjectType):
    """ GraphQL node representing a match venue """
    model_id = graphene.String()

    class Meta:
        model = Venue
        interfaces = (graphene.relay.Node, )
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'matches__division': ['exact'],
            'matches__season__slug': ['exact'],
            'matches__our_team__slug': ['exact'],
            'is_home': ['exact'],
        }

    def resolve_model_id(self, info):
        return self.id


class Query(graphene.ObjectType):
    """ GraphQL query for venues """
    venues = schema_helper.OptimizableFilterConnectionField(VenueNode)

    relay_venues = schema_helper.OptimizableFilterConnectionField(VenueNode)

    def resolve_venues(self, info, **kwargs):
        return schema_helper.optimize(Venue.objects.filter(**kwargs),
                                      info,
                                      field_map).distinct()
