"""
Utilities for processing stats related to members
"""

from collections import defaultdict
from awards.models import MatchAward
from matches.models import Match


class TeamRepresentation(object):
    """ A record of how many appearances a member has made for the specified team """

    def __init__(self, team):
        self.team = team
        self.appearance_count = 0


class MemberPlayingStats(object):
    """ Container class for statistics about a member's playing record. """

    def __init__(self, member):
        self.member = member
        self.played = 0
        self.won = 0
        self.drawn = 0
        self.lost = 0
        self.goals = 0
        self.goals_for = 0
        self.goals_against = 0
        self.clean_sheets = 0
        self.mom = 0
        self.lom = 0
        self.is_captain = False
        self.is_vice_captain = False
        self.team_representations = {}

    def add_appearance(self, appearance):
        """ Add the specified appearance to the member's stats"""
        self.played += 1
        if appearance.match.was_won():
            self.won += 1
        elif appearance.match.was_lost():
            self.lost += 1
        elif appearance.match.was_drawn():
            self.drawn += 1
        self.goals += appearance.goals
        self.goals_for += appearance.match.our_score
        self.goals_against += appearance.match.opp_score
        if appearance.match.opp_score == 0:
            self.clean_sheets += 1
        if appearance.match.our_team.slug not in self.team_representations:
            self.team_representations[appearance.match.our_team.slug] = TeamRepresentation(
                appearance.match.our_team)
        self.team_representations[appearance.match.our_team.slug].appearance_count += 1

    def add_award(self, award):
        """ Add the specified award to the member's stats"""
        if award.name == MatchAward.MOM:
            self.mom += 1
        elif award.name == MatchAward.LOM:
            self.lom += 1

    def avg_goals_for(self):
        """ Returns the average number of goals scored by our team in matches this player made an appearance in """
        if self.played == 0:
            return 0.0

        return float(self.goals_for) / float(self.played)

    def avg_goals_against(self):
        """ Returns the average number of goals scored by the opposition team in matches this player made an appearance in """
        if self.played == 0:
            return 0.0

        return float(self.goals_against) / float(self.played)

    def avg_points(self):
        """ Returns the average number of points per game in matches this player made an appearance in """
        if self.played == 0:
            return 0.0

        return float(self.total_points()) / float(self.played)

    def total_points(self):
        """ Returns the total number of points gained in matches this player made an appearance in """
        return ((Match.POINTS_FOR_WIN * self.won) +
                (Match.POINTS_FOR_DRAW * self.drawn) +
                (Match.POINTS_FOR_LOSS * self.lost))


class TeamPlayingStats(object):
    """ Container class for statistics about a team's playing record """

    def __init__(self):
        self.played = 0
        self.won = 0
        self.drawn = 0
        self.lost = 0
        self.goals = 0
        self.clean_sheets = 0

    def add_match(self, match):
        self.played += 1
        if match.was_won():
            self.won += 1
        elif match.was_lost():
            self.lost += 1
        elif match.was_drawn():
            self.drawn += 1
        self.goals += match.our_score
        if match.opp_score == 0:
            self.clean_sheets += 1


class SquadPlayingStats(object):
    """ Container class for statistics about a team's playing record """

    def __init__(self):
        self.match_ids = {}
        self.squad_lookup = {}
        self.totals = TeamPlayingStats()

    def squad(self):
        return sorted(self.squad_lookup.values(), key=lambda playerstats: (-playerstats.is_captain, -playerstats.is_vice_captain, playerstats.member.first_name, playerstats.member.last_name))

    def add_appearance(self, appearance):
        """ Add the specified appearance to the team playing stats """
        if appearance.match_id not in self.match_ids:
            self.match_ids[appearance.match_id] = {}
            self.totals.add_match(appearance.match)

        if appearance.member_id not in self.squad_lookup:
            self.squad_lookup[appearance.member_id] = MemberPlayingStats(
                appearance.member)
        self.squad_lookup[appearance.member_id].add_appearance(appearance)

    def add_award_winner(self, award_winner):
        """ Adds the specified award winner to the corresponding member's playing stats """
        if award_winner.member_id in self.squad_lookup:
            self.squad_lookup[award_winner.member_id].add_award(
                award_winner.award)

    def add_captains(self, captains):
        """ Updates the relevant squad members with whether they are a captain/vice-captain or not """
        for captain in captains:
            if captain.member_id in self.squad_lookup:
                if captain.is_vice:
                    self.squad_lookup[captain.member_id].is_vice_captain = True
                else:
                    self.squad_lookup[captain.member_id].is_captain = True


class SeasonPlayingStats(object):
    """ Member playing stats for a particular season """

    def __init__(self, season, member):
        self.season = season
        self.member_stats = MemberPlayingStats(member)


class AllSeasonsPlayingStats(object):
    """ Container class for statistics about a member's playing record over all seasons """

    def __init__(self):
        # A dictionary of SeasonPlayingStats keyed by season slug
        self.seasons = {}

    def add_appearance(self, appearance):
        """ Add an appearance to the relevant season's stats """
        if appearance.match.season.slug not in self.seasons:
            self.seasons[appearance.match.season.slug] = SeasonPlayingStats(
                appearance.match.season, appearance.member)
        self.seasons[appearance.match.season.slug].member_stats.add_appearance(
            appearance)

    def add_award_winner(self, award_winner):
        """ Add award winner details to the relevant season's stats """
        if award_winner.match.season.slug not in self.seasons:
            self.seasons[award_winner.match.season.slug] = SeasonPlayingStats(
                award_winner.match.season, award_winner.member)
        self.seasons[award_winner.match.season.slug].member_stats.add_award(
            award_winner.award)
