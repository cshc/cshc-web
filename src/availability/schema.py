"""
GraphQL Schema for Awards and Award Winners
"""

import logging
import traceback
import graphene
import django_filters
from graphene_django_extras import DjangoListObjectType, DjangoObjectType
from graphene_django_optimizedextras import OptimizedDjangoListObjectField, get_paginator
from .models import MatchAvailability

LOG = logging.getLogger(__name__)


class MatchAvailabilityFilter(django_filters.FilterSet):
    """ Filters for Match Availabilities """
    class Meta:
        model = MatchAvailability
        fields = {
            'member_id': ['exact'],
            'match_id': ['exact'],
            'match__date': ['gte'],
            'match__our_team_id': ['exact'],
        }

    order_by = django_filters.OrderingFilter(
        fields=(
            ('member__first_name', 'member'),
            ('match__date', 'match'),
        )
    )


class MatchAvailabilityType(DjangoObjectType):
    """ GraphQL node representing a match availability """
    can_play = graphene.Boolean()
    can_umpire = graphene.Boolean()

    class Meta:
        model = MatchAvailability

    def resolve_can_play(self, info):
        return self.can_play

    def resolve_can_umpire(self, info):
        return self.can_umpire


class MatchAvailabilityList(DjangoListObjectType):
    class Meta:
        description = "Type definition for match availability list "
        model = MatchAvailability
        pagination = get_paginator()


class EditMatchAvailabilityInput(graphene.InputObjectType):
    """ Input Type for updating playing/umpiring availability for 
        a particular member and match. 
    """
    match_id = graphene.Int()
    member_id = graphene.Int()
    playing_availability = graphene.String()
    umpiring_availability = graphene.String()
    comment = graphene.String(required=False)


class UpdateMatchAvailability(graphene.relay.ClientIDMutation):
    """ This mutation updates the playing/umpiring availability for a particular
        member and match.
    """

    class Input:
        availability = graphene.Argument(EditMatchAvailabilityInput)

    errors = graphene.List(graphene.String)
    availability = graphene.Field(MatchAvailabilityType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        availability_data = input['availability']
        context = 'playing' if availability_data.playing_availability is not None else 'umpiring'
        errors = []
        try:
            availability = MatchAvailability.objects.get(
                match_id=availability_data.match_id, member_id=availability_data.member_id)
            availability.playing_availability = availability_data.playing_availability
            availability.umpiring_availability = availability_data.umpiring_availability
            availability.comment = availability_data.comment
            availability.clean()
            availability.save()

            LOG.info('Set {} availability for {} in {} to {}'.format(
                context, availability.member, availability.match,
                getattr(availability, '{}_availability'.format(context))))
        except MatchAvailability.DoesNotExist:
            errors.append('Can\'t find match availability for match {} and member {}'.format(
                availability_data.match_id, availability_data.member_id))
            availability = None
        except Exception as e:
            traceback.print_exc()
            availability = None
            errors.append("{}".format(e))

        if errors:
            LOG.error('Failed to set {} availability for member {} in match {}: {}'.format(
                context, availability_data.member_id, availability_data.match_id, errors))
        return cls(availability=availability, errors=errors)


class Query(graphene.ObjectType):
    """ GraphQL query for availabilities """
    match_availabilities = OptimizedDjangoListObjectField(
        MatchAvailabilityList, filterset_class=MatchAvailabilityFilter)


class Mutation(graphene.ObjectType):
    """ GraphQL mutations for availabilities """
    update_match_availability = UpdateMatchAvailability.Field()
