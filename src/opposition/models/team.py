""" The Team model represents an opposition team within a club.

    Teams are simply identified by a name but are also marked as
    Mens/Ladies/Mixed.
"""

from django.db import models
from django.db.models.query import QuerySet
from django.template.defaultfilters import slugify
from core.models import TeamGender
from .club import Club


class TeamQuerySet(QuerySet):
    """Model manager for the Team model"""

    def mens(self):
        """Returns only men's teams"""
        return self.filter(gender=TeamGender.Mens)

    def ladies(self):
        """Returns only ladies teams"""
        return self.filter(gender=TeamGender.Ladies)

    def mixed(self):
        """Returns only mixed teams"""
        return self.filter(gender=TeamGender.Mixed)


class Team(models.Model):
    """Represents an opposition team"""

    # The club this team is a part of
    club = models.ForeignKey(Club, related_name="teams")

    # Full name of the team
    name = models.CharField("Team name", max_length=100, unique=True)

    # Abbreviated name of the team
    short_name = models.CharField("Abbreviated name", max_length=100)

    # Mens/ladies/mixed team
    gender = models.CharField(
        "Team gender (mens/ladies)", max_length=6, choices=TeamGender.Choices)

    # Auto-generated slug
    slug = models.SlugField("Slug")

    objects = TeamQuerySet.as_manager()

    class Meta:
        """ Meta-info for the Team model."""
        app_label = 'opposition'
        ordering = ['club', 'name']

    def clean(self):
        self.slug = slugify(self.name)

    def __str__(self):
        return str(self.name)

    def genderless_name(self):
        """ Utility method to get the team name without 'Mens' or 'Ladies' in it."""
        return self.name.replace(" Ladies", "").replace(" Mens", "")
