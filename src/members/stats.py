"""
Utilities for processing stats related to members
"""

from awards.models import MatchAward


class MemberPlayingStats(object):
    """ Container class for statistics about a member's playing record. """

    def __init__(self, member):
        self.member = member
        self.played = 0
        self.won = 0
        self.drawn = 0
        self.lost = 0
        self.goals = 0
        self.clean_sheets = 0
        self.mom = 0
        self.lom = 0

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
        if appearance.match.opp_score == 0:
            self.clean_sheets += 1

    def add_award(self, award):
        """ Add the specified award to the member's stats"""
        if award.name == MatchAward.MOM:
            self.mom += 1
        elif award.name == MatchAward.LOM:
            self.lom += 1


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
        return sorted(self.squad_lookup.values(), key=lambda playerstats: -playerstats.played)

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
