""" The Member model represents a club member - specifically someone who
    participates in matches or holds a committee position.

    Members may be linked to website Users (CshcUser) - this enables the
    user's profile page to display stats and details pertaining to their
    member model. In particular, it lets the user upload a profile picture
    for their member model.
"""

import logging
import os
import geocoder
from django.conf import settings
from django.db import models
from django.db.models import Max, Q
from django.dispatch import receiver
from django_resized import ResizedImageField
from django.db.models.functions import Coalesce
from allauth.account.signals import email_changed
from image_cropping import ImageRatioField
from geoposition.fields import GeopositionField
from core.models import make_unique_filename, ClubInfo, Gender, Position, EmergencyContactRelationship
from members import settings as member_settings
from competitions.models import Season

LOG = logging.getLogger(__name__)


@receiver(email_changed)
def on_email_change(sender, **kwargs):
    """
    Handler for a user's email address being changed.

    Updates the associated member's email address (if there is a member associated with this user)
    """
    user = kwargs['user']
    if user.has_member():
        # Note that the to_email_address field is an instance of the allauth.EmailAddress model
        email_address_instance = kwargs['to_email_address']
        user.member.email = email_address_instance.email
        user.member.save()


def get_file_name(instance, filename):
    """ Returns a unique filename for profile pictures."""
    filename = make_unique_filename(filename)
    return os.path.join(member_settings.MEMBERS_PHOTO_DIR, filename)


class MemberManager(models.Manager):
    """ Model Manager for the Member model """

    def get_query_set(self):
        return super(MemberManager, self).get_query_set().annotate(pref_name=Coalesce('known_as', 'first_name')).order_by('pref_name', 'last_name')

    def safe_get(self, **kwargs):
        try:
            return self.get(**kwargs)
        except Member.DoesNotExist:
            return None

    def _get_members_with_active_shirt_numbers_queryset(self, gender):
        """
        Helper method to build the queryset of members whose shirt numbers
        should be considered 'in use' for a given gender, respecting
        is_current status and grace periods.
        """
        base_queryset = self.filter(gender=gender)

        shirt_number_include_not_current_obj, _ = ClubInfo.objects.get_or_create(
                key='ShirtNumIncNonCurr', defaults={'value': 'True'})
        include_not_current = shirt_number_include_not_current_obj.value in [
            'True', 'true', 'yes', '1']

        if include_not_current:
            shirt_number_grace_seasons_obj, _ = ClubInfo.objects.get_or_create(
                        key='ShirtNumGraceSeasons', defaults={'value': '1'})
            grace_seasons = int(shirt_number_grace_seasons_obj.value)

            annotated_queryset = base_queryset.annotate(
                last_appearance_season_start=Max('appearances__match__season__start')
            )
            stale_cutoff_season_start_date = None

            seasons = Season.objects.order_by('-start')
            if len(seasons) > grace_seasons:
                stale_cutoff_season_start_date = seasons[grace_seasons].start
            elif seasons: # If there are fewer seasons than grace_seasons, consider all existing seasons
                 stale_cutoff_season_start_date = seasons[-1].start # Oldest season start

            if stale_cutoff_season_start_date:
                return annotated_queryset.filter(
                    Q(is_current=True) |
                    (Q(is_current=False) & (
                        Q(last_appearance_season_start__isnull=False) &
                        Q(last_appearance_season_start__gte=stale_cutoff_season_start_date)
                    ))
                )
            else:
                return annotated_queryset.filter(is_current=True)
        else:
            return base_queryset.filter(is_current=True)

    def get_available_shirt_numbers(self, gender,
                                    max_count=None):
        """
        Returns a list of available *numerical* shirt numbers for a given gender.
        An available number is one not currently assigned to any member
        of the specified gender with a numerical shirt number.
        If max_count is None, returns all available numbers up to max_number.
        :param gender: The gender to filter by.
        :param max_count: The maximum number of available numbers to return.
        :return: A list of available shirt numbers.
        """
        if not gender:
            return []

        max_shirt_number_obj, _ = ClubInfo.objects.get_or_create(
                    key='ShirtNumMax', defaults={'value': '199'})
        max_shirt_number = int(max_shirt_number_obj.value)

        members_with_used_numbers = self._get_members_with_active_shirt_numbers_queryset(gender)

        used_shirt_numbers_str = members_with_used_numbers.filter(
            shirt_number__isnull=False
        ).exclude(shirt_number='').values_list('shirt_number', flat=True)

        used_numbers_set = set()
        for num_str in used_shirt_numbers_str:
            try:
                num_int = int(num_str)
                used_numbers_set.add(num_int)
            except ValueError:
                pass

        available_numbers = []
        for i in range(1, max_shirt_number + 1):
            if i not in used_numbers_set:
                available_numbers.append(i)
            if max_count is not None and len(available_numbers) >= max_count:
                break
        return available_numbers

    def is_shirt_number_available(self, gender, shirt_number_int):
        """
        Checks if a specific numerical shirt number is available for a given gender.
        An available number is one not currently assigned to any member
        of the specified gender with a numerical shirt number, considering
        'is_current' status and grace periods.
        :param gender: The gender to filter by.
        :param shirt_number_int: The specific shirt number (integer) to check.
        :return: True if available, False otherwise.
        """
        if not gender:
            return False

        max_shirt_number_obj, _ = ClubInfo.objects.get_or_create(
                    key='ShirtNumMax', defaults={'value': '199'})
        max_shirt_number = int(max_shirt_number_obj.value)

        if not (1 <= shirt_number_int <= max_shirt_number):
            return False

        shirt_number_str = str(shirt_number_int)

        members_with_active_numbers = self._get_members_with_active_shirt_numbers_queryset(gender)
        used_by_member_exists = members_with_active_numbers.filter(shirt_number=shirt_number_str).exists()

        return not used_by_member_exists

class Member(models.Model):
    """ Represents a member of Cambridge South Hockey Club. Alternatively this can
        be thought of as a 'Player' model.

        User accounts will be associated with a member instance wherever possible.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True,
                                on_delete=models.SET_NULL)
    """ The user (if any) associated with this member """

    first_name = models.CharField(max_length=100, default=None)
    """ Members first name (required) """

    known_as = models.CharField(
        max_length=100, default=None, null=True, blank=True)
    """ The first name by which the member is typically known (optional) """

    last_name = models.CharField(max_length=100, default=None)
    """ Members surname (required) """

    profile_pic = ResizedImageField("Profile picture", size=[400, 400],
                                    upload_to=get_file_name, null=True, blank=True)
    """ An optional profile picture of the member """

    profile_pic_cropping = ImageRatioField(
        'profile_pic', '400x400')
    """ Image cropping support """

    gender = models.CharField("Gender", max_length=6,
                              choices=Gender.Choices, default=Gender.Male)
    """ The member's gender """

    pref_position = models.IntegerField("Preferred position", choices=Position.Choices,
                                        default=Position.Other)
    """ The member's preferred playing position. Defaults to 'not known'. """

    is_current = models.BooleanField(
        "Current", help_text="Is this member currently part of the club?", default=True)
    """ Indicates whether this member is a current member of the club. Useful for filtering etc. """

    shirt_number = models.CharField(max_length=4, blank=True)
    """ Players shirt number """

    is_coach = models.NullBooleanField(
        "Coach?", null=True, blank=True, default=False, help_text='Does this member possess a hockey coaching qualification?')
    """ Indicates whether this member is a coach """

    is_umpire = models.NullBooleanField(
        "Umpire?", null=True, blank=True, default=False, help_text='Is this member a qualified hockey umpire (including probationer)?')
    """ Indicates whether this member is a umpire """

    dob = models.DateField(
        'Date of birth', help_text="Used for medical information", null=True, blank=True)
    """ Member's date of birth - used for medical information """

    emergency_contact = models.CharField(
        max_length=255, null=True, blank=True, help_text="Name of person to contact in an emergency")
    """ Name of person to contact in an emergency """

    emergency_relationship = models.CharField(
        "Emergency contact relationship", help_text="The member's emergency contact's relationship to them",
        max_length=100, choices=EmergencyContactRelationship, null=True, blank=True, default=EmergencyContactRelationship.Other)
    """ The member's emergency contact's relationship to them """

    emergency_phone = models.CharField(
        "Emergency contact phone", max_length=20, null=True, blank=True, help_text="Phone number of person to contact in an emergency")
    """ Phone number of person to contact in an emergency """

    medical_notes = models.TextField(
        help_text="E.g. allergies, etc. in case of medical treatment", null=True, blank=True)
    """Any additional medical notes about this member """

    email = models.EmailField(null=True, blank=True)
    """ Member's email address """

    phone = models.CharField(
        "Phone number", max_length=20, null=True, blank=True)
    """ Member's phone number """

    addr_street = models.CharField(
        "Address (street)", max_length=255, null=True, blank=True)
    """ Member's home address: house number and street """

    addr_line2 = models.CharField(
        "Address (line 2)", max_length=255, null=True, blank=True)
    """ Member's home address: optional second line """

    addr_town = models.CharField(
        "Address (town)", max_length=255, null=True, blank=True)
    """ Member's home address: city/town """

    addr_postcode = models.CharField(
        "Address (post code)", max_length=10, null=True, blank=True)
    """ Member's home address: post code """

    addr_position = GeopositionField(
        "Address (lat/long)", null=True, blank=True)
    """ Member's home address: lat/Long location (used for Google Maps etc) """

    objects = MemberManager()

    class Meta:
        """ Meta-info for the Member model."""
        app_label = 'members'
        ordering = ['first_name', 'last_name']
        permissions = (
            ("view_personal_data",
             "Can see the personal data (address, phone, email, medical notes etc) of a member"),
        )

    def __str__(self):
        return str(self.full_name())

    def save(self, *args, **kwargs):
        # Try to do a geocode lookup if the address is set and the position isn't known
        if self.addr_postcode and not self.addr_position:
            try:
                g = geocoder.google(self.full_address())
                if g.latlng:
                    self.addr_position = "{},{}".format(
                        g.latlng[0], g.latlng[1])
                else:
                    LOG.error("Failed to geocode position for member %s",
                              self.full_name(), exc_info=True)
            except:
                LOG.error("Failed to geocode position for member %s",
                          self.full_name(), exc_info=True)

        super(Member, self).save(*args, **kwargs)
        # If the first and/or last name has been changed, update the corresponding user fields
        # if there is a user associated with this member
        if self.user is not None:
            modified = False
            if self.user.first_name != self.first_name:
                self.user.first_name = self.first_name
                modified = True
            if self.user.last_name != self.last_name:
                self.user.last_name = self.last_name
                modified = True
            if modified:
                self.user.save()

    @models.permalink
    def get_absolute_url(self):
        """ Returns the url for this member instance."""
        return ('member_detail', [self.pk])

    def pref_first_name(self):
        """ Returns the member's preferred first name (known_as if set; otherwise first_name) """
        return self.known_as if self.known_as else self.first_name

    def full_name(self):
        """ Returns the member's full name."""
        return u"{} {}".format(self.pref_first_name(), self.last_name)

    def first_name_and_initial(self):
        """ Returns the shortened name display for this member."""
        return u"{} {}".format(self.pref_first_name(), self.last_name[0])

    @property
    def address_known(self):
        """ Returns True if the member's address is known.

            Currently this just checks if the postcode or position fields are
            populated.
        """
        return True if self.addr_postcode or self.addr_position else False

    def full_address(self, separator=", "):
        """ Returns the member's full home address with (not None) address items separated by commas.

            If the address is empty, returns 'Address unknown'.
        """
        addr = separator.join(filter(None, (self.addr_street, self.addr_line2,
                                            self.addr_town, self.addr_postcode)))
        if not addr.strip():
            return 'Address unknown'
        return addr

    def current_squad(self):
        """ Returns the member's current squad membership (if they are currently in a squad; otherwise None) """
        try:
            return self.squadmembership_set.current().first()
        except:
            return None
