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
from core.models import make_unique_filename, Gender, Position


def get_file_name(instance, filename):
    """ Returns a unique filename for profile pictures."""
    filename = make_unique_filename(filename)
    return os.path.join('uploads/profile_pics', filename)


class Member(models.Model):
    """ Represents a member of Cambridge South Hockey Club. Alternatively this can
        be thought of as a 'Player' model.

        User accounts will be associated with a member instance wherever possible.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True,
                                on_delete=models.SET_NULL)

    # Members first name (required)
    first_name = models.CharField(max_length=100, default=None)

    # Members surname (required)
    last_name = models.CharField(max_length=100, default=None)

    # An optional profile picture of the member
    profile_pic = ResizedImageField("Profile picture", size=[400, 400],
                                    upload_to=get_file_name, null=True, blank=True)

    # Image cropping support
    profile_pic_cropping = ImageRatioField('profile_pic', '400x400')

    # The member's gender
    gender = models.CharField("Gender", max_length=6,
                              choices=Gender.Choices, default=Gender.Male)

    # The member's preferred playing position. Defaults to 'not known'.
    pref_position = models.IntegerField("Preferred position", choices=Position.Choices,
                                        default=Position.Other)

    # Indicates whether this member is a current member of the club. Useful for filtering etc.
    is_current = models.BooleanField(default=True)

    # Players shirt number
    shirt_number = models.CharField(max_length=4, blank=True)

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
