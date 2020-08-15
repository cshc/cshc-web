""" The MemberOffer model represents a special offer for club members.
"""

import os
from datetime import datetime
from django.db import models
from django.db.models import Q
from ckeditor.fields import RichTextField

class AnnouncementManager(models.Manager):
    """ Announcement model manager """

    def active(self):
        """ Returns announcements that are currently active """
        dt_now = datetime.now().date()
        not_expired = Q(end_date__gt=dt_now) | Q(end_date__isnull=True)
        not_pending = Q(start_date__lt=dt_now) | Q(start_date__isnull=True)
        return self.get_queryset().filter(not_expired).filter(not_pending)


class AnnouncementStyle(object):
    """ Enumeration of announcement styles """
    Danger = 'danger'
    Success = 'success'
    Warning = 'warning'
    Info = 'info'
    Choices = [
        ('danger', 'Danger'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('info', 'Info'),
    ]


class Announcement(models.Model):
    """ Represents an announcement visible on the home page """

    title = models.CharField(max_length=255, unique=True)
    """ The announcement title """

    content = RichTextField()
    """ The announcement content """
    
    style = models.CharField("Style", max_length=8, choices=AnnouncementStyle.Choices, default=AnnouncementStyle.Info)

    modified = models.DateTimeField(auto_now=True)
    """ Timestamp for the announcement being updated. Typically used for ordering announcements. """

    start_date = models.DateField(blank=True, null=True, help_text="Optional: the date on which this announcement should start being displayed.")
    """ The date on which this announcement should start being displayed. """

    end_date = models.DateField(blank=True, null=True, help_text="Optional: the date on which this announcement should stop being displayed.")
    """ The date on which this announcement should stop being displayed. """

    objects = AnnouncementManager()

    class Meta:
        app_label = 'announcements'
        ordering = ['-modified']

    def __str__(self):
        return self.title
