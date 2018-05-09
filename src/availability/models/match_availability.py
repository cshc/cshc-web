from django.utils.translation import ugettext as _
from django.utils import timezone
from django.db import models
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError
from model_utils import Choices
from model_utils.fields import MonitorField
from members.models import Member
from matches.models import Match


# When a player's availability is first requested, the availability
# status will be 'awaiting_response'. The player can then set it
# to 'available', 'not_available' or 'unsure'. The player can
# change their availability at any stage (prior to the match).
AVAILABILITY = Choices(
    ('awaiting_response', _('Awaiting response')),
    ('available', _('Available')),
    ('not_available', _('Not available')),
    ('unsure', _('Not sure')),
)

AVAILABILITY_TYPE = Choices(
    ('playing', _('Playing')),
    ('umpiring', _('Umpiring')),
)


class MatchAvailabilityQuerySet(QuerySet):
    """ Model Query Set for MatchAvailability models"""

    def playing(self):
        """ Returns just playing availabilities """
        return self.filter(availability_type=AVAILABILITY_TYPE.playing)

    def umpiring(self):
        """ Returns just umpiring availabilities """
        return self.filter(availability_type=AVAILABILITY_TYPE.umpiring)

    def for_member(self, member_id, future=True):
        """ Returns match availabilities for the specified member """
        queryset = self.upcoming() if future else self
        return queryset.filter(member_id=member_id)

    def upcoming(self):
        """ Returns only availabilities in the future """
        return self.filter(match__date__gt=timezone.now().date())


class MatchAvailability(models.Model):
    """ Represents a member's availability (either playing or umpiring) for a specific match """

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="availabilities")
    """ The member that this availability relates to """

    match = models.ForeignKey(
        Match, on_delete=models.CASCADE, related_name="availabilities")
    """ The match that this availability relates to """

    availability_type = models.CharField(
        choices=AVAILABILITY_TYPE, max_length=20, default=AVAILABILITY_TYPE.playing)
    """ The type of availability (e.g. umpiring/playing) """

    availability = models.CharField(
        choices=AVAILABILITY, max_length=20, default=AVAILABILITY.awaiting_response)
    """ The member's availability for this match """

    comment = models.TextField(null=True, blank=True,
                               help_text="Any additional details about this availability")

    availability_changed = MonitorField(monitor='availability')
    """ Automatically updated to the current datetime when the availability field is changed """

    objects = MatchAvailabilityQuerySet.as_manager()

    class Meta:
        """ Meta-info on the MatchAvailability model."""
        app_label = 'availability'
        verbose_name_plural = 'match availabilities'
        permissions = (
            ("manage_umpiring_matchavailability",
             "Can manage umpiring availabilities"),
        )

    def __str__(self):
        return "{} - {}".format(self.member, self.match)
