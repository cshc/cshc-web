""" The MemberOffer model represents a special offer for club members.
"""

import os
from datetime import datetime
from django.db import models
from django.db.models import Q
from django_resized import ResizedImageField
from ckeditor.fields import RichTextField
from core.models import make_unique_filename
from offers import settings


def get_file_name(instance, filename):
    """ Returns a unique filename for uploaded offer images."""
    filename = make_unique_filename(filename)
    return os.path.join(settings.OFFERS_IMAGE_DIR, filename)


class MemberOfferManager(models.Manager):
    """ MemberOffer model manager """

    def active(self):
        """ Returns offers that have not yet expired """
        not_expired = Q(expiry__gt=datetime.now().date()
                        ) | Q(expiry__isnull=True)
        return self.get_queryset().filter(not_expired)


class MemberOffer(models.Model):
    """ Represents a special offer to club members """

    title = models.CharField(max_length=255, unique=True)
    """ The offer title (typically the company/organisation name) """

    description = RichTextField()
    """ The description of the offer details """

    image = ResizedImageField(
        size=[400, 100], upload_to=get_file_name, null=True, blank=True)
    """ Image for the offer """

    url = models.URLField(
        blank=True, help_text="Link to an external website with more information")
    """ The (external) URL to associate with this offer """

    modified = models.DateTimeField(auto_now=True)
    """ Timestamp for the offer being updated. Typically used for ordering offers. """

    expiry = models.DateField(blank=True, null=True)
    """ The date on which this offer expires. Expired offers will not be displayed. """

    objects = MemberOfferManager()

    class Meta:
        app_label = 'offers'
        ordering = ['-modified']

    def __str__(self):
        return self.title
