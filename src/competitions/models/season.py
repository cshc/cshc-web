""" The Season model represents a single season (year)
    in which the club played hockey.
"""

import logging
from datetime import datetime
from django.db import models
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError

# Define the default season start/end dates
SEASON_START_MONTH = 9  # Sept
SEASON_END_MONTH = 8    # Aug
SEASON_START_DAY = 1
SEASON_END_DAY = 31

LOG = logging.getLogger(__name__)


class SeasonQuerySet(QuerySet):
    """ Model Manager for Season models"""

    def by_date(self, date):
        """ Returns the season in which the specified date falls"""
        return self.get(start__lte=date, end__gte=date)

    def reversed(self):
        """ Returns the seasons in reverse chronological order."""
        return self.order_by('-start')

    def latest(self):
        """ Returns the latest season (this may be 'next season')"""
        return self.order_by('-start').first()

    def previous(self, season):
        """ Returns the previous season to the given one (or None if the given
            season is the first one)
        """
        return self.filter(end__lt=season.start).order_by('-start').first()

    def next(self, season):
        """ Returns the next season to the given one (or None if the given
            season is the last one)
        """
        return self.filter(start__gt=season.end).order_by('start').first()


class Season(models.Model):
    """ Represents a season during which matches are played"""

    # The first date of the season
    start = models.DateField(
        "Season start", help_text="(Approx) first day of the season")

    # The last date of the season
    end = models.DateField(
        "Season end", help_text="(Approx) last day of the season")

    # A slug to identify the season. This will be automatically created.
    # This field is most often used in urls.
    slug = models.SlugField()

    objects = SeasonQuerySet.as_manager()

    class Meta:
        """ Meta-info for the Season  model."""
        app_label = 'competitions'
        ordering = ['start']
        get_latest_by = "start"

    def __str__(self):
        return str(self.slug)
    __str__.short_description = 'Season'

    def clean(self):
        # Make sure the start is before the end!
        if self.start is not None and self.end is not None and self.start >= self.end:
            raise ValidationError(
                "The start of the season must be before the end of the season")

        # Prevent any overlapping seasons
        if Season.objects.exclude(pk=self.pk).filter(start__lte=self.start, end__gte=self.start).exists():
            raise ValidationError(
                "The starting date of this season overlaps with another season")
        elif Season.objects.exclude(pk=self.pk).filter(start__lte=self.end, end__gte=self.end).exists():
            raise ValidationError(
                "The end date of this season overlaps with another season")

        # Automatically set the slug field
        self.slug = "{}-{}".format(self.start.year, self.end.year)

    @staticmethod
    def current():
        """ Returns the current season (or creates it if it doesn't exist)"""
        try:
            return Season.objects.by_date(datetime.now().date())
        except Season.DoesNotExist:
            LOG.warning("Current season not found. Creating now")
            return Season.create_current_season()

    @staticmethod
    def is_current_season(season_id):
        """ Returns true if the specified season ID is the ID of the current season"""
        return Season.current().pk == season_id

    @staticmethod
    def create_current_season():
        """ Utility method to create the current season."""
        current = Season()
        dtnow = datetime.now()
        if dtnow.month >= 9:
            start_year = dtnow.year
        else:
            start_year = dtnow.year - 1

        current.start = datetime(
            year=start_year, month=SEASON_START_MONTH, day=SEASON_START_DAY)
        current.end = datetime(year=start_year + 1,
                               month=SEASON_END_MONTH, day=SEASON_END_DAY)
        current.save()
        return current
