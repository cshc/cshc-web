""" Models relating to the CSHC committee.

    CommitteePosition   - defines a particular position on the committee.
    CommitteeMembership - specifies which member held a particular CommitteePosition
                          during a particular season.
"""

from django.db import models
from competitions.models import Season
from core.models import TeamGender


class CommitteePosition(models.Model):
    """ Represents the name of a position on the committee.
    """

    name = models.CharField(max_length=100, default=None)

    gender = models.CharField(
        "Mens/Ladies/Mixed", max_length=6, choices=TeamGender.Choices)

    index = models.PositiveSmallIntegerField("Index", default=0,
                                             help_text="Used for visual ordering of the committee")

    class Meta:
        """ Meta-info for the CommitteePosition model."""
        app_label = 'members'
        unique_together = ('gender', 'index')
        # By default, list the general committee members first, then ladies then men.
        ordering = ('-gender', 'index')

    def __str__(self):
        if self.gender == TeamGender.Mixed:
            return str(self.name)
        return str("{} ({})".format(self.name, self.gender))


class CommitteeMembershipManager(models.Manager):
    """ Queries that relate to Committee Membership"""

    def get_queryset(self):
        return super(CommitteeMembershipManager, self).get_queryset().select_related('season', 'member', 'position')

    def by_member(self, member):
        """Returns only committee membership for the specified member"""
        return self.get_queryset().filter(member=member)

    def by_position(self, position):
        """Returns only committee membership for the specified position"""
        return self.get_queryset().filter(position=position)

    def by_season(self, season):
        """Returns only committee membership for the specified season"""
        return self.get_queryset().filter(season=season).order_by('position__index')

    def current(self):
        """ Returns only current committee membership, if any."""
        return self.get_queryset().filter(season=Season.current()).order_by('position__index')


class CommitteeMembership(models.Model):
    """ This model represents membership of the club committee. A member
        may hold zero or more committee positions in a particular season.

        The actual positions may vary from season to season but are captured
        in the CommitteePosition model. If a new position is created, a new
        CommitteePosition entry should be added for it.
    """
    # The club member in the committee
    member = models.ForeignKey('Member')

    # The season in which the club member was on the committee
    season = models.ForeignKey('competitions.Season')

    # The committee position
    position = models.ForeignKey('CommitteePosition')

    objects = CommitteeMembershipManager()

    class Meta:
        """ Meta-info for the CommitteeMembership model."""
        app_label = 'members'
        ordering = ['member', 'position', 'season']
        # Only one person can hold a particular position in a particular season
        unique_together = ('position', 'season')

    def __str__(self):
        return str("{} - {} ({})".format(self.member, self.position, self.season))
