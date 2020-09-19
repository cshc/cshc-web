""" These models keep track of all the times members won an award,
    be it a match award (POM, LOM) or an end of season award.
"""

from django.db import models
from django.core.exceptions import ValidationError
from matches.models import Match
from members.models import Member
from competitions.models import Season
from .award import MatchAward, EndOfSeasonAward


class AwardWinnerManager(models.Manager):
    """ AwardWinner base model mananger """

    def get_queryset(self):
        return super(AwardWinnerManager, self).get_queryset().select_related('member')

    def by_member(self, member):
        """ Returns only items for the specified member"""
        return self.get_queryset().filter(member=member)


class MatchAwardWinnerManager(AwardWinnerManager):
    """ Model manager for Match Award Winners """

    def pom(self):
        """Returns only Player of the Match award winners"""
        return self.get_queryset().filter(award__name=MatchAward.POM)

    def lom(self):
        """Returns only Lemon of the Match award winners"""
        return self.get_queryset().filter(award__name=MatchAward.LOM)

    def by_match(self, match):
        """Returns only award winners for the specified match"""
        return self.get_queryset().filter(match=match)


class EndOfSeasonAwardWinnerManager(AwardWinnerManager):
    """ Model manager for End Of Season Award Winners """

    def by_season(self, season):
        """Returns only award winners for the specified season"""
        return self.get_queryset().filter(season=season)


class AwardWinner(models.Model):
    """Abstract base class for an award winner"""

    # The member that won this award. Either this field or the awardee field must
    # be filled in (but not both).
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_awards",
                               null=True, blank=True, default=None,
                               help_text="(Leave blank if award winner is not a member)")

    # The name of the person that won this award (if not a member). Either this
    # field or the member field must be filled in (but not both).
    awardee = models.CharField("Award winner", max_length=255, blank=True,
                               help_text="Only use this field if the award winner is not a member")

    # A comment describing the award
    comment = models.TextField(help_text="Enter a short description of why this person " +
                               "received this award")

    class Meta:
        """ Meta-info on the AwardWinner model."""
        app_label = 'awards'
        abstract = True

    def clean(self):
        if self.member is None and (self.awardee is None or self.awardee == ""):
            raise ValidationError("You must specify either a member or an awardee " +
                                  "(if the awardee is not a member)")
        elif self.member != None and (self.awardee != None and self.awardee != ""):
            raise ValidationError(
                "You cannot specify both a member and an awardee")

    def awardee_name(self):
        """ Returns either the awardee or the member's full name"""
        if self.member is None:
            return self.awardee
        return self.member.full_name()


class MatchAwardWinner(AwardWinner):
    """A winner of an award associated with matches"""

    # The match that the award winner won the award for
    match = models.ForeignKey(
        Match, on_delete=models.CASCADE, related_name="award_winners")

    # The award that was won
    award = models.ForeignKey(
        MatchAward, on_delete=models.CASCADE, related_name="winners")

    objects = MatchAwardWinnerManager()

    def __str__(self):
        return str("{} - {} ({})".format(self.award, self.awardee_name(), self.match.date))


class EndOfSeasonAwardWinner(AwardWinner):
    """A winner of an End of Season award"""

    # The season in which the award winner won the award
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="award_winners")

    # The award that was won
    award = models.ForeignKey(
        EndOfSeasonAward, on_delete=models.CASCADE, related_name="winners")

    objects = EndOfSeasonAwardWinnerManager()

    class Meta:
        ordering = ['-season']

    def __str__(self):
        return str("{} - {} ({})".format(self.award, self.awardee_name(), self.season))
