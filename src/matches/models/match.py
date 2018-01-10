""" The Match model is at the heart of the CSHC website. Most of the
    data in the database is in some way linked to matches.
"""

from datetime import datetime, time, timedelta
from django.db import models
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError
from model_utils.fields import SplitField
from teams.models import ClubTeam, ClubTeamSeasonParticipation
from opposition.models import Team
from members.models import Member
from venues.models import Venue
from competitions.models import Season, Division, Cup


class HomeAway(object):
    """ Each match is either a home or away fixture """
    Home = 'Home'
    Away = 'Away'
    Choices = (
        ('Home', 'Home'),
        ('Away', 'Away'),
    )


class AlternativeOutcome(object):
    """ If the match wasn't played, an alternative outcome should be entered """
    Postponed = 'Postponed'
    Cancelled = 'Cancelled'
    Walkover = 'Walkover'
    BYE = 'BYE'
    Abandoned = 'Abandoned'
    Choices = (
        ('Postponed', 'Postponed'),
        ('Cancelled', 'Cancelled'),
        ('Walkover', 'Walkover'),
        ('BYE', 'BYE'),
        ('Abandoned', 'Abandoned'),
    )


class FixtureType(object):
    """ We keep track of whether a match is a league, cup or just a friendly match """
    Friendly = 'Friendly'
    League = 'League'
    Cup = 'Cup'
    Choices = (
        ('Friendly', 'Friendly'),
        ('League', 'League'),
        ('Cup', 'Cup'),
    )


class MatchQuerySet(QuerySet):
    """ Queries that relate to Matches"""

    def fixtures(self):
        """ Returns only matches in the future, ordered by date"""
        return self.filter(date__gte=datetime.now().date()).order_by('date', 'time')

    def results(self):
        """ Returns only matches in the past, ordered by date"""
        return self.filter(date__lt=datetime.now().date()).order_by('date', 'time')

    def reports(self):
        """ Returns only results with match reports"""
        return self.results().exclude(report_body__isnull=True).exclude(report_body='')

    def this_season(self):
        """ Returns only this season's matches"""
        return self.by_season(Season.current())

    def by_season(self, season):
        """ Returns only matches in the specified season"""
        return self.filter(season=season)

    def by_date(self, date):
        """ Returns only matches on the specified date"""
        return self.filter(date=date).order_by('our_team__position')

    def by_report_author(self, member):
        """ Returns only matches whose match report was written by the specified member"""
        return self.filter(report_author=member)


class Match(models.Model):
    """ Represents a match.

        Note: both fixtures and results are classed as matches:
            Fixtures are just matches in the future
            Results are matches in the past
    """

    # Avoid magic numbers. However this simple constant definition is insufficient if
    # these values ever change!
    POINTS_FOR_WIN = 3
    POINTS_FOR_DRAW = 1
    POINTS_FOR_LOSS = 0

    # Walk-over matches must be either 3-0 or 5-0 (depending on the league)
    WALKOVER_SCORE_W1 = 3
    WALKOVER_SCORE_W2 = 5
    WALKOVER_SCORE_L = 0

    COMMENTARY_START_MINS = 15
    COMMENTARY_END_MINS = 120

    # The Cambridge South team playing in this match
    our_team = models.ForeignKey(ClubTeam, verbose_name="Our team")

    # The opposition team
    opp_team = models.ForeignKey(Team, verbose_name="Opposition team")

    # The match venue
    venue = models.ForeignKey(
        Venue, null=True, blank=True, on_delete=models.SET_NULL, related_name="matches")

    # Is the match a home or away fixture for South
    home_away = models.CharField("Home/Away", max_length=5, choices=HomeAway.Choices,
                                 default=HomeAway.Home)

    # The type of fixture
    fixture_type = models.CharField("Fixture type", max_length=10, choices=FixtureType.Choices,
                                    default=FixtureType.League)

    # The fixture date
    date = models.DateField("Fixture date")

    # The fixture start time. This can be left blank if its not known.
    time = models.TimeField("Start time", null=True, blank=True, default=None)

    # The alternative match outcome if it wasn't actually played
    alt_outcome = models.CharField("Alternative outcome", max_length=10, null=True,
                                   blank=True, default=None, choices=AlternativeOutcome.Choices)

    # Cambridge South's final score
    our_score = models.PositiveSmallIntegerField(
        "Our score", null=True, blank=True, default=None)

    # The opposition's final score
    opp_score = models.PositiveSmallIntegerField("Opposition's score", null=True,
                                                 blank=True, default=None)

    # Cambridge South's half time score
    our_ht_score = models.PositiveSmallIntegerField("Our half-time score", null=True,
                                                    blank=True, default=None)

    # The opposition's half time score
    opp_ht_score = models.PositiveSmallIntegerField("Opposition's half-time score", null=True,
                                                    blank=True, default=None)

    # The total number of own goals scored by the opposition.
    # Note - Cambs South own goals are recored in the Appearance model (as we care about
    # who scored the own goal!)
    opp_own_goals = models.PositiveSmallIntegerField(
        "Opposition own-goals", default=0)

    # A short paragraph that can be used to hype up the match before its played - can be HTML
    # TODO: Prevent entering pre-match hype for matches in the past?
    pre_match_hype = SplitField("Pre-match hype", blank=True)

    # The (optional) title of the match report
    report_title = models.CharField(
        "Match report title", max_length=200, blank=True)

    # The (optional) match report author
    report_author = models.ForeignKey(Member, verbose_name="Match report author", null=True, blank=True,
                                      on_delete=models.SET_NULL, related_name="match_reports")

    # The actual match report text - can be HTML
    report_body = SplitField("Match report", blank=True)

    # The datetime at which the report was first published
    report_pub_timestamp = models.DateTimeField("Match report publish timestamp", editable=False,
                                                default=None, null=True)

    # Advanced fields - typically leave as default value ######################

    # If True, this match should NOT count towards Goal King stats
    ignore_for_goal_king = models.BooleanField(default=False,
                                               help_text="Ignore this match when compiling Goal King stats")

    # If True, this match should NOT count towards Southerners League stats
    ignore_for_southerners = models.BooleanField(default=False,
                                                 help_text="Ignore this match when compiling Southerners League stats")

    # Sometimes despite the clubs' kit clashing, we still play in our normal home kit. This can be recorded here.
    override_kit_clash = models.BooleanField(default=False,
                                             help_text="Ignore normal kit-clash with this club for this match")

    # Sometimes goals scored in shorter matches (e.g. in a tournament) will count a different amount towards the 'goals-per-game' stats
    gpg_pro_rata = models.FloatField(default=1.0,
                                     help_text="Goals-per-game multiplier. Only change this from the default value for matches of a different length.")

    # Derived attributes ######################################################
    # - these values cannot be entered in a form - they are derived based on the other attributes
    season = models.ForeignKey('competitions.Season', editable=False)
    division = models.ForeignKey('competitions.Division', null=True, blank=True, editable=False,
                                 on_delete=models.PROTECT)
    cup = models.ForeignKey('competitions.Cup', null=True, blank=True, editable=False,
                            on_delete=models.PROTECT)

    # Convenience attribute listing all members who made an appearance in this match
    players = models.ManyToManyField(
        'members.Member', through="Appearance", related_name="matches")

    objects = MatchQuerySet.as_manager()

    class Meta:
        """ Meta-info for the Match model."""
        app_label = 'matches'
        verbose_name_plural = "matches"
        ordering = ['date', 'time', 'our_team__position']

    def __str__(self):
        return str("{} vs {} ({}, {})".format(self.our_team, self.opp_team, self.fixture_type, self.date))

    @models.permalink
    def get_absolute_url(self):
        """ Returns the url for this match."""
        return ('match_detail', [self.pk])

    def clean(self):
        # If its a walkover, check the score is a valid walkover score
        if (self.alt_outcome == AlternativeOutcome.Walkover and
                not Match.is_walkover_score(self.our_score, self.opp_score)):
            raise ValidationError(
                "A walk-over score must be 3-0, 5-0, 0-3 or 0-5. Score = {}-{}".format(self.our_score, self.opp_score))

        # If its cancelled or postponed or BYE, check the scores are not entered
        if((self.alt_outcome == AlternativeOutcome.Cancelled or
            self.alt_outcome == AlternativeOutcome.Postponed or
            self.alt_outcome == AlternativeOutcome.BYE) and
           (self.our_score is not None or self.opp_score is not None or self.our_ht_score is not None or self.opp_ht_score is not None)):
            raise ValidationError(
                "A cancelled or postponed match should not have scores")

        if self.alt_outcome is None or self.alt_outcome == AlternativeOutcome.Abandoned:
            # You can't specify one score without the other
            if((self.our_score is not None and self.opp_score is None) or
               (self.our_score is None and self.opp_score is not None)):
                raise ValidationError("Both scores must be provided")

            # ...same goes for half time scores
            if((self.our_ht_score is not None and self.opp_ht_score is None) or
               (self.our_ht_score is None and self.opp_ht_score is not None)):
                raise ValidationError("Both half-time scores must be provided")

            # The opposition can't score more own goals than our total score
            if(self.our_score is not None and
               self.opp_own_goals > self.our_score):
                raise ValidationError("Too many opposition own goals")

            # Half-time scores must be <= the final scores
            if self.all_scores_provided():
                if(self.our_ht_score > self.our_score or
                   self.opp_ht_score > self.opp_score):
                    raise ValidationError(
                        "Half-time scores cannot be greater than final scores")

        # Automatically set the season based on the date
        try:
            self.season = Season.objects.by_date(self.date)
        except Season.DoesNotExist:
            raise ValidationError(
                "This date appears to be outside of any recognised season.")

        if self.fixture_type == FixtureType.League:
            # Automatically set the division based on the team and season
            try:
                self.division = ClubTeamSeasonParticipation.objects.get(
                    team=self.our_team, season=self.season).division
            except Division.DoesNotExist:
                raise ValidationError("{} is not participating in a division in the season {}".format(
                    self.our_team, self.season))
        else:
            self.division = None    # Clear the division field

        if self.fixture_type == FixtureType.Cup:
            # Automatically set the cup based on the team and season
            try:
                self.cup = ClubTeamSeasonParticipation.objects.get(
                    team=self.our_team, season=self.season).cup
            except Cup.DoesNotExist:
                raise ValidationError("{} is not participating in a cup in the season {}".format(
                    self.our_team, self.season))
        else:
            self.cup = None    # Clear the cup field

    def save(self, *args, **kwargs):
        """ Set a few automatic fields and then save """
        # Timestamp the report publish datetime when its first created
        if self.report_pub_timestamp is None and self.report_body.content:
            self.report_pub_timestamp = datetime.now()

        super(Match, self).save(*args, **kwargs)

    @property
    def is_home(self):
        """ Returns True if this is a home fixture"""
        return self.home_away == HomeAway.Home

    def home_away_abbrev(self):
        """ Returns an abbreviated representation of the home/away status ('H'/'A') """
        return 'H' if self.is_home else 'A'

    def kit_clash(self):
        """Returns true if there is a kit-clash for this fixture

            Note that this takes into account the override_kit_clash field.
            Home    Clash   Override    Return
            F       F       F           F
            F       F       T           T
            F       T       F           T
            F       T       T           F
            T       F       F           F
            T       F       T           T
            T       T       F           F
            T       T       T           T
        """
        if self.is_home:
            return self.override_kit_clash
        clash = self.opp_team.club.kit_clash(self.our_team.gender)
        return (clash and not self.override_kit_clash) or (not clash and self.override_kit_clash)

    def has_report(self):
        """ Returns True if this match has a match report"""
        return self.report_body and self.report_body.content

    def datetime(self):
        """ Convenience method to retrieve the date and time as one datetime object.
            Returns just the date if the time is not set.
        """
        if self.time is not None:
            return datetime.combine(self.date, self.time)
        return datetime.combine(self.date, time())

    def is_off(self):
        """ Returns True if the match is postponed or cancelled."""
        return self.alt_outcome in (AlternativeOutcome.Postponed,
                                    AlternativeOutcome.Cancelled)

    def is_in_past(self):
        """ Returns True if the match date/datetime is in the past."""
        if self.time is not None:
            return self.datetime() < datetime.now()
        return self.date < datetime.today().date()

    def commentary_is_active(self):
        """
        Returns True if commentary should be active (i.e. if its within COMMENTARY_START_MINS of the start of
        the match and COMMENTARY_END_MINS after the end of the match)
        """
        if not self.time:
            return False
        now = datetime.now()
        match_dt = self.datetime()
        commentary_start = match_dt - \
            timedelta(minutes=Match.COMMENTARY_START_MINS)
        commentary_end = match_dt + \
            timedelta(minutes=Match.COMMENTARY_END_MINS)
        return (now >= commentary_start) and (now <= commentary_end)

    def time_display(self):
        """ Gets a formatted display of the match time.

            If the match time is not known, returns '???'
            if the match is in the past or 'TBD' if the match
            is in the future.
        """
        if self.time:
            return self.time.strftime('%H:%M')
        elif self.is_in_past():
            return '???'
        return 'TBD'

    def match_title_text(self):
        """ Gets an appropriate match title regardless of the status of the match.
            Examples include:
                "Men's 1sts thrash St Neots"
                "M1 vs St Neots Men's 1sts"
                "M1 vs St Neots Men's 1sts - POSTPONED"
                "M1 vs St Neots Men's 1sts - CANCELLED"
                "M1 3-0 St Neots Men's 1sts (WALK-OVER)"
                "M1 5-1 St Neots Men's 1sts"
        """
        if self.report_title:
            return self.report_title
        return self.fixture_title()

    def fixture_title(self):
        """ Returns the title of this fixture in one of the following formats:
            Fixtures:- "M1 vs St Neots Men's 1sts"
            Results:-  "M1 3-0 St Neots Men's 1sts"
        """
        if self.alt_outcome == AlternativeOutcome.Walkover:
            return "{} {}-{} {} (WALK-OVER)".format(self.our_team, self.our_score,
                                                    self.opp_score, self.opp_team)

        elif self.alt_outcome == AlternativeOutcome.Abandoned:
            return "{} {}-{} {} (Abandoned)".format(self.our_team, self.our_score,
                                                    self.opp_score, self.opp_team)

        elif self.alt_outcome is not None:
            return "{} vs {} - {}".format(self.our_team, self.opp_team,
                                          self.get_alt_outcome_display())

        elif not self.final_scores_provided():
            return "{} vs {}".format(self.our_team, self.opp_team)

        return "{} {}-{} {}".format(self.our_team, self.our_score,
                                    self.opp_score, self.opp_team)

    @staticmethod
    def is_walkover_score(score1, score2):
        """ Checks if the given scores are valid walk-over scores.
            Valid results are 3-0, 5-0, 0-3, 0-5.
        """
        if score1 in (Match.WALKOVER_SCORE_W1, Match.WALKOVER_SCORE_W2):
            return score2 == Match.WALKOVER_SCORE_L
        elif score2 in (Match.WALKOVER_SCORE_W1, Match.WALKOVER_SCORE_W2):
            return score1 == Match.WALKOVER_SCORE_L
        return False

    def ht_scores_provided(self):
        """ Returns true if both half-time scores are not None."""
        return (self.our_ht_score is not None and
                self.opp_ht_score is not None)

    def final_scores_provided(self):
        """ Returns true if both full-time/final scores are not None."""
        return (self.our_score is not None and
                self.opp_score is not None)

    def all_scores_provided(self):
        """ Returns true if both half-time and full-time scores are provided."""
        return self.final_scores_provided() and self.ht_scores_provided()

    def was_won(self):
        """ Returns true if our team won the match. """
        return (self.final_scores_provided() and
                self.our_score > self.opp_score)

    def was_lost(self):
        """ Returns true if our team lost the match. """
        return (self.final_scores_provided() and
                self.our_score < self.opp_score)

    def was_drawn(self):
        """ Returns true if the match was drawn. """
        return (self.final_scores_provided() and
                self.our_score == self.opp_score)

    def score_display(self):
        """ Convenience method for displaying the score.
            Examples include:
            "3-2"         (normal result)
            ""            (blank - no result yet)
            "Cancelled"   (alt_outcome not None)
        """
        if self.alt_outcome is not None:
            return self.get_alt_outcome_display()
        if not self.final_scores_provided():
            return "-"
        return "{}-{}".format(self.our_score, self.opp_score)

    def result_display(self):
        """ Returns a textual representation of the result (or alternative outcome) """
        if self.final_scores_provided():
            if self.our_score > self.opp_score:
                return 'won'
            elif self.our_score < self.opp_score:
                return 'lost'
            else:
                return 'drawn'
        else:
            return self.get_alt_outcome_display()

    def simple_venue_name(self):
        """ Returns 'Away' if this is not a home match.
            Otherwise returns the short_name attribute value.
        """
        if self.venue:
            if self.is_home:
                if self.venue.short_name is not None:
                    return self.venue.short_name
                return self.venue.name
            return "Away"
        elif self.is_in_past():
            return '???'
        return 'TBD'
