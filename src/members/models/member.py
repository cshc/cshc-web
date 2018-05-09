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
from django.dispatch import receiver
from django_resized import ResizedImageField
from allauth.account.signals import email_changed
from image_cropping import ImageRatioField
from geoposition.fields import GeopositionField
from core.models import make_unique_filename, Gender, Position, EmergencyContactRelationship
from members import settings as member_settings
from teams.models import TeamCaptaincy
from competitions.models import Season

LOG = logging.getLogger(__name__)


@receiver(email_changed)
def on_email_change(sender, **kwargs):
    """
    Handler for a user's email address being changed.

    Updates the associated member's email address (if there is a member associated with this user)
    """
    user = kwargs['user']
    if user.member is not None:
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

    def safe_get(self, **kwargs):
        try:
            return self.get(**kwargs)
        except Member.DoesNotExist:
            return None


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
        "Emergency contact phone", max_length=15, null=True, blank=True, help_text="Phone number of person to contact in an emergency")
    """ Phone number of person to contact in an emergency """

    medical_notes = models.TextField(
        help_text="E.g. allergies, etc. in case of medical treatment", null=True, blank=True)
    """Any additional medical notes about this member """

    email = models.EmailField(null=True, blank=True)
    """ Member's email address """

    phone = models.CharField(
        "Phone number", max_length=15, null=True, blank=True)
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

    def current_captaincies(self):
        """ Returns the member's current captaincies/vice-captaincies (if any). """
        return TeamCaptaincy.objects.by_member(self).current().select_related('team')
