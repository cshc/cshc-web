""" The GoalKing model tracks the cummulative number of goals scored
    by members (players) in a particular season.

    NOTE: the GoalKing model also tracks the cummulative miles travelled
    by a member in a particular season and is therefore used for the
    'Accidental Tourist' feature.

    There is a single record (instance) for each goal scorer in a season.

    This is another 'cache' model - the data is derived from other models but
    is calculated and stored in this database table for efficiency. A nightly
    cronjob task updates the goal king statistics automatically - so the GoalKing
    model is not accessible from the admin interface and should never be manually
    edited.
"""

import logging
from django.db import models
from core.models import TeamGender, TeamOrdinal
from members.models import Member
from competitions.models import Season
from matches.models import Appearance

LOG = logging.getLogger(__name__)


class GoalKingManager(models.Manager):
    """ Model manager for the GoalKing model"""

    def get_queryset(self):
        """ Gets the QuerySet, also selecting the related member (and user) and season models"""
        return super(GoalKingManager, self).get_queryset().select_related('member__user', 'season')

    def by_season(self, season):
        """ Filters the GoalKing entries by the specified season - and orders them in
            descending total number of goals.
        """
        return self.get_queryset().filter(season=season).order_by('-total_goals')

    def accidental_tourist(self, season):
        """ Filters the GoalKing entries by the specified season - and orders them in
            descending total number of miles travelled.
        """
        return self.get_queryset().filter(season=season).order_by('-total_miles', '-mpg')


class GoalKing(models.Model):
    """
    Represents a Goal King entry. Also used for Accidental Tourist.
    Note: This is a derivative model which is calculated and updated for reasons of efficiency.
    It should never be manually edited (any manual adjustments will be overridden the next time
    the update is run).
    """
    # The member this entry applies to
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    # The season this entry applies to
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    # The total number of games the member played in the season
    games_played = models.PositiveSmallIntegerField(
        "Number of games played", default=0)

    # The total number of miles travelled to matches by this member in this season
    total_miles = models.PositiveIntegerField(default=0)

    # Goal tallies for each team
    m1_goals = models.PositiveSmallIntegerField(
        "Goals for Mens 1sts", default=0)
    m2_goals = models.PositiveSmallIntegerField(
        "Goals for Mens 2nds", default=0)
    m3_goals = models.PositiveSmallIntegerField(
        "Goals for Mens 3rds", default=0)
    m4_goals = models.PositiveSmallIntegerField(
        "Goals for Mens 4ths", default=0)
    m5_goals = models.PositiveSmallIntegerField(
        "Goals for Mens 5ths", default=0)
    m6_goals = models.PositiveSmallIntegerField(
        "Goals for Mens 6ths", default=0)
    l1_goals = models.PositiveSmallIntegerField(
        "Goals for Ladies 1sts", default=0)
    l2_goals = models.PositiveSmallIntegerField(
        "Goals for Ladies 2nds", default=0)
    l3_goals = models.PositiveSmallIntegerField(
        "Goals for Ladies 3rds", default=0)
    l4_goals = models.PositiveSmallIntegerField(
        "Goals for Ladies 4ths", default=0)
    l5_goals = models.PositiveSmallIntegerField(
        "Goals for Ladies 5ths", default=0)
    mixed_goals = models.PositiveSmallIntegerField(
        "Goals for Mixed team", default=0)
    mind_goals = models.PositiveSmallIntegerField(
        "Goals for the Men's Indoor team", default=0)
    mv_goals = models.PositiveSmallIntegerField(
        "Goals for the Men's Vets team", null=True, blank=True, default=0)
    lind_goals = models.PositiveSmallIntegerField(
        "Goals for the Ladies' Indoor team", default=0)
    lv_goals = models.PositiveSmallIntegerField(
        "Goals for the Ladies' Vets team", null=True, blank=True, default=0)

    # Own-goal tallies for each team
    m1_own_goals = models.PositiveSmallIntegerField(
        "Own goals for Mens 1sts", default=0)
    m2_own_goals = models.PositiveSmallIntegerField(
        "Own goals for Mens 2nds", default=0)
    m3_own_goals = models.PositiveSmallIntegerField(
        "Own goals for Mens 3rds", default=0)
    m4_own_goals = models.PositiveSmallIntegerField(
        "Own goals for Mens 4ths", default=0)
    m5_own_goals = models.PositiveSmallIntegerField(
        "Own goals for Mens 5ths", default=0)
    m6_own_goals = models.PositiveSmallIntegerField(
        "Own goals for Mens 6ths", default=0)
    l1_own_goals = models.PositiveSmallIntegerField(
        "Own goals for Ladies 1sts", default=0)
    l2_own_goals = models.PositiveSmallIntegerField(
        "Own goals for Ladies 2nds", default=0)
    l3_own_goals = models.PositiveSmallIntegerField(
        "Own goals for Ladies 3rds", default=0)
    l4_own_goals = models.PositiveSmallIntegerField(
        "Own goals for Ladies 4ths", default=0)
    l5_own_goals = models.PositiveSmallIntegerField(
        "Own goals for Ladies 5ths", default=0)
    mixed_own_goals = models.PositiveSmallIntegerField(
        "Own goals for Mixed team", default=0)
    mind_own_goals = models.PositiveSmallIntegerField(
        "Own goals for the Men's Indoor team", default=0)
    mv_own_goals = models.PositiveSmallIntegerField(
        "Own goals for the Men's Vets team", null=True, blank=True, default=0)
    lind_own_goals = models.PositiveSmallIntegerField(
        "Own goals for the Ladies' Indoor team", default=0)
    lv_own_goals = models.PositiveSmallIntegerField(
        "Own goals for the Ladies' Vets team", null=True, blank=True, default=0)

    # These are attributes (db fields) rather than just methods so that we can take advantage of
    # SQL ordering - we typically want to order goal king entries by total goals.
    total_goals = models.PositiveSmallIntegerField(
        "Total goals", editable=False)
    total_own_goals = models.PositiveSmallIntegerField(
        "Total own goals", editable=False)

    gpg = models.FloatField("Goals per Game", editable=False, null=True)
    """ Average number of goals per game """

    mpg = models.FloatField("Miles per Game", editable=False, null=True)
    """ Average number of miles travelled per game """

    objects = GoalKingManager()

    class Meta:
        """ Meta-info for the GoalKing model."""
        app_label = 'matches'
        # One record for a member in a particular season
        unique_together = ('member', 'season')
        ordering = ['season', 'member']

    def __str__(self):
        return str("{} - {}".format(self.member, self.season))

    def save(self, *args, **kwargs):
        # Calculate non-editable, derived fields
        self.total_goals = (self.m1_goals + self.m2_goals + self.m3_goals + self.m4_goals +
                            self.m5_goals + self.m6_goals + self.l1_goals + self.l2_goals + self.l3_goals +
                            self.l4_goals + self.l5_goals + self.mixed_goals + self.mind_goals + 
                            self.mv_goals + self.lind_goals + self.lv_goals)
        self.total_own_goals = (self.m1_own_goals + self.m2_own_goals + self.m3_own_goals +
                                self.m4_own_goals + self.m5_own_goals + self.m6_own_goals + self.l1_own_goals +
                                self.l2_own_goals + self.l3_own_goals + self.l4_own_goals +
                                self.l5_own_goals + self.mixed_own_goals + self.mind_own_goals + 
                                self.mv_own_goals + self.lind_own_goals + self.lv_own_goals)

        self.gpg = self.goals_per_game()
        self.mpg = self.miles_per_game()

        super(GoalKing, self).save(*args, **kwargs)

    def miles_per_game(self):
        """ Returns the average number of miles travelled to a game.
        """
        if self.games_played == 0:
            return 0.0
        return float(self.total_miles) / float(self.games_played)

    def goals_per_game(self):
        """ Returns the number of goals scored per game"""
        if self.games_played == 0:
            return 0.0
        return float(self.total_goals) / float(self.games_played)

    def gender(self):
        """ Convenience method to fetch the gender of the member"""
        return self.member.gender

    def reset(self):
        """ Resets all tallies to zero """
        self.total_miles = 0
        self.games_played = 0
        self.m1_goals = 0
        self.m2_goals = 0
        self.m3_goals = 0
        self.m4_goals = 0
        self.m5_goals = 0
        self.m6_goals = 0
        self.mind_goals = 0
        self.mv_goals = 0
        self.l1_goals = 0
        self.l2_goals = 0
        self.l3_goals = 0
        self.l4_goals = 0
        self.l5_goals = 0
        self.lind_goals = 0
        self.lv_goals = 0
        self.mixed_goals = 0
        self.m1_own_goals = 0
        self.m2_own_goals = 0
        self.m3_own_goals = 0
        self.m4_own_goals = 0
        self.m5_own_goals = 0
        self.m6_own_goals = 0
        self.mind_own_goals = 0
        self.mv_own_goals = 0
        self.l1_own_goals = 0
        self.l2_own_goals = 0
        self.l3_own_goals = 0
        self.l4_own_goals = 0
        self.l5_own_goals = 0
        self.lind_own_goals = 0
        self.lv_own_goals = 0
        self.mixed_own_goals = 0

    def add_appearance(self, appearance):
        """ Adds the details of an appearance to the GoalKing stat"""
        self.games_played += 1

        # Add the 'return distance' to the venue to the total miles travelled
        if appearance.match.venue is not None:
            if appearance.match.venue.distance is not None:
                self.total_miles += appearance.match.venue.distance * 2
            else:
                LOG.warning("%s has no distance specified",
                            appearance.match.venue)
        else:
            LOG.warning("%s has no venue specified", appearance.match)

        if appearance.goals == 0 and appearance.own_goals == 0:
            return

        short_name = appearance.match.our_team.short_name

        if short_name == 'M1':
            self.m1_goals += appearance.goals
            self.m1_own_goals += appearance.own_goals
        elif short_name == 'M2':
            self.m2_goals += appearance.goals
            self.m2_own_goals += appearance.own_goals
        elif short_name == 'M3':
            self.m3_goals += appearance.goals
            self.m3_own_goals += appearance.own_goals
        elif short_name == 'M4':
            self.m4_goals += appearance.goals
            self.m4_own_goals += appearance.own_goals
        elif short_name == 'M5':
            self.m5_goals += appearance.goals
            self.m5_own_goals += appearance.own_goals
        elif short_name == 'M6':
            self.m6_goals += appearance.goals
            self.m6_own_goals += appearance.own_goals
        elif short_name == 'MInd':
            self.mind_goals += appearance.goals
            self.mind_own_goals += appearance.own_goals
        elif short_name == 'MV':
            self.mv_goals += appearance.goals
            self.mv_own_goals += appearance.own_goals
        elif short_name == 'L1':
            self.l1_goals += appearance.goals
            self.l1_own_goals += appearance.own_goals
        elif short_name == 'L2':
            self.l2_goals += appearance.goals
            self.l2_own_goals += appearance.own_goals
        elif short_name == 'L3':
            self.l3_goals += appearance.goals
            self.l3_own_goals += appearance.own_goals
        elif short_name == 'L4':
            self.l4_goals += appearance.goals
            self.l4_own_goals += appearance.own_goals
        elif short_name == 'L5':
            self.l5_goals += appearance.goals
            self.l5_own_goals += appearance.own_goals
        elif short_name == 'LInd':
            self.lind_goals += appearance.goals
            self.lind_own_goals += appearance.own_goals
        elif short_name == 'LV':
            self.lv_goals += appearance.goals
            self.lv_own_goals += appearance.own_goals
        elif short_name == 'Mixed':
            self.mixed_goals += appearance.goals
            self.mixed_own_goals += appearance.own_goals
        else:
            raise AssertionError(
                "Unexpected team: {}".format(short_name))

    @staticmethod
    def update_for_season(season):
        """ Updates the GoalKing entries for the specified season based on the
            Appearances in that season.
        """
        LOG.info("Updating Goal King stats for %s", season)
        gk_entries = GoalKing.objects.by_season(
            season).select_related('member__user')
        # A dictionary for goal kings, keyed by the member id
        gk_lookup = {}

        # Reset all the goals scored fields - but don't save anything yet.
        for gk_entry in gk_entries:
            gk_entry.reset()
            gk_lookup[gk_entry.member_id] = gk_entry

        # We just want the member id, the match team, the number of goals scored (and own goals)
        appearances = Appearance.objects.by_season(season).select_related('match__our_team', 'match__venue').filter(
            match__ignore_for_goal_king=False).only('match__season', 'member', 'goals', 'own_goals', 'match__our_team', 'match__venue')

        for appearance in appearances:
            if appearance.member_id not in gk_lookup:
                LOG.debug("Adding new Goal King entry for member %s",
                          appearance.member_id)
                gk_lookup[appearance.member_id] = GoalKing(
                    member=appearance.member, season=season)
            gk_lookup[appearance.member_id].add_appearance(appearance)

        # Save the updated entries back to the database
        for _, value in gk_lookup.items():
            value.save()
