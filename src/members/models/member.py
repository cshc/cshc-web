""" The Member model represents a club member - specifically someone who
    participates in matches or holds a committee position.

    Members may be linked to website Users (CshcUser) - this enables the
    user's profile page to display stats and details pertaining to their
    member model. In particular, it lets the user upload a profile picture
    for their member model.
"""

import os
from django.conf import settings
from django.db import models
from django_resized import ResizedImageField
from image_cropping import ImageRatioField
from geoposition.fields import GeopositionField
from core.models import make_unique_filename, Gender, Position, EmergencyContactRelationship
from members import settings as member_settings


def get_file_name(instance, filename):
    """ Returns a unique filename for profile pictures."""
    filename = make_unique_filename(filename)
    return os.path.join(member_settings.MEMBERS_PHOTO_DIR, filename)


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

    is_coach = models.BooleanField(
        "Coach?", default=False, help_text='Does this member possess a hockey coaching qualification?')
    """ Indicates whether this member is a coach """

    is_umpire = models.BooleanField(
        "Umpire?", default=False, help_text='Is this member a qualified hockey umpire (including probationer)?')
    """ Indicates whether this member is a umpire """

    dob = models.DateField(
        'Date of birth', help_text="Used for medical information", null=True, blank=True)
    """ Member's date of birth - used for medical information """

    emergency_contact = models.CharField(
        max_length=255, null=True, blank=True, help_text="Name of person to contact in an emergency")
    """ Name of person to contact in an emergency """

    emergency_relationship = models.CharField(
        "Emergency contact relationship", help_text="The member's emergency contact's relationship to them",
        max_length=100, choices=EmergencyContactRelationship, default=EmergencyContactRelationship.Other)
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

    class Meta:
        """ Meta-info for the Member model."""
        app_label = 'members'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return str(self.full_name())

    @models.permalink
    def get_absolute_url(self):
        """ Returns the url for this member instance."""
        return ('member_detail', [self.pk])

    def full_name(self):
        """ Returns the member's full name."""
        return u"{} {}".format(self.first_name, self.last_name)

    def first_name_and_initial(self):
        """ Returns the shortened name display for this member."""
        return u"{} {}".format(self.first_name, self.last_name[0])

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
