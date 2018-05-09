"""
GraphQL Schema for Awards and Award Winners
"""

import logging
import traceback
import graphene
import django_filters
from graphene_django_extras import DjangoListObjectType, DjangoObjectType
from graphene_django_optimizedextras import OptimizedDjangoListObjectField, get_paginator
from core.filters import AndFilter
from .models import MatchAvailability
from matches.models import Match
from members.models import SquadMembership, Member
from .models import MatchAvailability, AVAILABILITY, AVAILABILITY_TYPE

LOG = logging.getLogger(__name__)


class MatchAvailabilityAction(graphene.Enum):
    SendReminder = 1
    Delete = 2


class MatchAvailabilityFilter(AndFilter):
    """ Filters for Match Availabilities """
    class Meta:
        model = MatchAvailability
        fields = {
            'member_id': ['exact'],
            'match_id': ['exact'],
            'match__date': ['gte'],
            'match__our_team_id': ['exact'],
            'availability_type': ['exact'],
            'availability': ['exact'],
        }

    order_by = django_filters.OrderingFilter(
        fields=(
            ('member__first_name', 'member'),
            ('match__date', 'match'),
        )
    )


class MatchAvailabilityType(DjangoObjectType):
    """ GraphQL node representing a match availability """
    class Meta:
        model = MatchAvailability


class MatchAvailabilityList(DjangoListObjectType):
    class Meta:
        description = "Type definition for match availability list "
        model = MatchAvailability
        pagination = get_paginator()


def create_or_update_availability(
        match_id,
        member_id,
        availability_type,
        availability=AVAILABILITY.awaiting_response,
        comment=None,
        message=None):
    """ Sets the match availability for the specified member and match. Emails the user if the availability is 'awaiting response' """
    member_availability, created = MatchAvailability.objects.select_related('member', 'match').get_or_create(
        match_id=match_id,
        member_id=member_id,
        availability_type=availability_type)
    member_availability.availability = availability
    member_availability.comment = comment
    member_availability.clean()
    member_availability.save()

    LOG.info('Set {} availability for {} in {} to {}'.format(
        availability_type.lower(), member_availability.member, member_availability.match, availability))

    if availability == AVAILABILITY.awaiting_response:
        # Send email to user asking for their availability. Include message if specified.
        pass

    return (member_availability, created)


class InitMatchAvailabilityInput(graphene.InputObjectType):
    """ Input Type for creating playing/umpiring availabilities for 
        a particular match. 
    """
    match_id = graphene.Int()
    availability_type = graphene.String()


class CreateMatchAvailability(graphene.relay.ClientIDMutation):
    """ This mutation creates the playing/umpiring availabilities for a particular match.
    """

    class Input:
        availability = graphene.Argument(InitMatchAvailabilityInput)

    errors = graphene.List(graphene.String)
    match_availabilities = graphene.List(MatchAvailabilityType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        availability_data = input['availability']
        errors = []
        availabilities = []
        try:
            match = Match.objects.get(id=availability_data.match_id)

            if availability_data.availability_type == AVAILABILITY_TYPE.umpiring:
                member_ids = list(Member.objects.filter(
                    is_current=True, is_umpire=True).values_list('id', flat=True))
            else:
                member_ids = list(SquadMembership.objects.current().by_team(
                    match.our_team).values_list('member__id', flat=True))

            for member_id in member_ids:
                availability, _ = create_or_update_availability(
                    availability_data.match_id,
                    member_id,
                    availability_data.availability_type,
                    AVAILABILITY.awaiting_response)

                availabilities.append(availability)

        except Match.DoesNotExist:
            errors.append('Can\'t find match {}'.format(
                availability_data.match_id))
        except Exception as e:
            traceback.print_exc()
            errors.append("{}".format(e))

        if errors:
            LOG.error('Failed to create {} availabilities for match {}: {}'.format(
                availability_data.availability_type.lower(), availability_data.match_id, errors))

        return cls(match_availabilities=availabilities, errors=errors)


class EditMatchAvailabilityInput(graphene.InputObjectType):
    """ Input Type for updating playing/umpiring availability for 
        a particular member and match. 
    """
    match_id = graphene.Int()
    member_id = graphene.Int()
    availability_type = graphene.String()
    availability = graphene.String()
    comment = graphene.String(required=False)
    message = graphene.String(required=False)


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
        errors = []
        try:
            availability, _ = create_or_update_availability(
                availability_data.match_id,
                availability_data.member_id,
                availability_data.availability_type,
                availability_data.availability,
                availability_data.comment)

        except Exception as e:
            traceback.print_exc()
            availability = None
            errors.append("{}".format(e))

        if errors:
            LOG.error('Failed to set {} availability for member {} in match {}: {}'.format(
                availability_data.availability_type.lower(), availability_data.member_id, availability_data.match_id, errors))
        return cls(availability=availability, errors=errors)


class MatchAvailabilityActionInput(graphene.InputObjectType):
    """ Input Type for actioning playing/umpiring availability for 
        a particular member and match. If no member is specified, 
        all availabilities (of the specified type) for that match are actioned.
    """
    match_id = graphene.Int()
    member_id = graphene.Int(required=False)
    availability_type = graphene.String()
    availability = graphene.String(required=False)
    action = MatchAvailabilityAction()


class ActionMatchAvailability(graphene.relay.ClientIDMutation):
    """ This mutation actions the playing/umpiring availability for a particular
        member and match. If no member is specified, all availabilities (of the specified type) 
        for that match are actioned.
    """

    class Input:
        availability = graphene.Argument(MatchAvailabilityActionInput)

    errors = graphene.List(graphene.String)
    match_availabilities = graphene.List(MatchAvailabilityType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        availability_data = input['availability']
        errors = []
        availabilities = []
        try:
            qs = MatchAvailability.objects.filter(
                match_id=availability_data.match_id,
                availability_type=availability_data.availability_type)
            if availability_data.member_id is not None:
                qs = qs.filter(member_id=availability_data.member_id)
            if availability_data.availability is not None:
                qs = qs.filter(availability=availability_data.availability)

            for availability in qs:
                if availability_data.action == MatchAvailabilityAction.SendReminder:
                    print('Sending reminder email to {}'.format(
                        availability.member))
                    # TODO: Send reminder email
                elif availability_data.action == MatchAvailabilityAction.Delete:
                    print('Deleting {}'.format(availability))
                    # TODO: Email member
                    availability.delete()
                else:
                    LOG.error('Unrecognised availability action: {}'.format(
                        availability_data.action))
                availabilities.append(availability)

        except Exception as e:
            traceback.print_exc()
            errors.append("{}".format(e))

        if errors:
            LOG.error('Failed to action {} availabilities for match {} (member = {}, action = {}): {}'.format(
                availability_data.availability_type.lower(),
                availability_data.match_id,
                availability_data.member_id,
                availability_data.action,
                errors))
        return cls(match_availabilities=availabilities, errors=errors)


class Query(graphene.ObjectType):
    """ GraphQL query for availabilities """
    match_availabilities = OptimizedDjangoListObjectField(
        MatchAvailabilityList, filterset_class=MatchAvailabilityFilter)


class Mutation(graphene.ObjectType):
    """ GraphQL mutations for availabilities """
    create_match_availability = CreateMatchAvailability.Field()
    update_match_availability = UpdateMatchAvailability.Field()
    action_match_availability = ActionMatchAvailability.Field()
