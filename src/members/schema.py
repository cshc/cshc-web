"""
GraphQL Schema for Members etc
"""

import graphene
from easy_thumbnails.files import get_thumbnailer
from graphene_django import DjangoObjectType
from matches.models import Appearance
from awards.models import MatchAwardWinner
from .stats import SquadPlayingStats
from .models import CommitteePosition, Member, CommitteeMembership, SquadMembership


class CommitteePositionType(DjangoObjectType):
    """ GraphQL node representing a committee position """
    class Meta:
        model = CommitteePosition


class CommitteeMembershipType(DjangoObjectType):
    """ GraphQL node representing a committee membership """
    class Meta:
        model = CommitteeMembership


class SquadMembershipType(DjangoObjectType):
    """ GraphQL node representing a member's squad membership """
    class Meta:
        model = SquadMembership


class MemberType(DjangoObjectType):
    """ GraphQL node representing a club member """
    model_id = graphene.String()
    thumb_url = graphene.String(profile=graphene.String())
    pref_position = graphene.String()

    class Meta:
        model = Member

    def resolve_model_id(self, info):
        return self.id

    def resolve_thumb_url(self, info, profile='avatar'):
        if not self.profile_pic:
            return None
        try:
            return get_thumbnailer(self.profile_pic)[profile].url
        except:
            return None

    def resolve_pref_position(self, info):
        return self.get_pref_position_display()


class MemberStatsType(graphene.ObjectType):
    member = graphene.Field(MemberType)
    played = graphene.Int()
    won = graphene.Int()
    drawn = graphene.Int()
    lost = graphene.Int()
    goals = graphene.Int()
    clean_sheets = graphene.Int()
    lom = graphene.Int()
    mom = graphene.Int()

    def resolve_member(self, info):
        return self.member


class TeamStatsType(graphene.ObjectType):
    played = graphene.Int()
    won = graphene.Int()
    drawn = graphene.Int()
    lost = graphene.Int()
    goals = graphene.Int()
    clean_sheets = graphene.Int()


class SquadStatsType(graphene.ObjectType):
    totals = graphene.Field(TeamStatsType)
    squad = graphene.List(MemberStatsType)


class Query(graphene.ObjectType):
    """ GraphQL query for members etc """
    committee_positions = graphene.List(CommitteePositionType)
    committee_memberships = graphene.List(CommitteeMembershipType)
    squad_memberships = graphene.List(SquadMembershipType)
    members = graphene.List(MemberType)
    squad_stats = graphene.Field(
        SquadStatsType, season=graphene.Int(), team=graphene.Int())

    def resolve_squad_stats(self, info, **kwargs):
        # Get playing stats for the team, including squad members
        app_qs = Appearance.objects.select_related('member', 'match')
        award_winners_qs = MatchAwardWinner.objects.select_related('award')

        if 'team' in kwargs:
            app_qs = app_qs.filter(match__our_team_id=kwargs['team'])
            award_winners_qs = award_winners_qs.filter(
                match__our_team_id=kwargs['team'])
        else:
            app_qs = app_qs.select_related('match__our_team')
            award_winners_qs = award_winners_qs.select_related(
                'match__our_team')

        if 'season' in kwargs:
            app_qs = app_qs.filter(match__season_id=kwargs['season'])
            award_winners_qs = award_winners_qs.filter(
                match__season_id=kwargs['season'])
        else:
            app_qs = app_qs.select_related('match__season')
            award_winners_qs = award_winners_qs.select_related('match__season')

        squad_stats = SquadPlayingStats()

        for app in app_qs:
            squad_stats.add_appearance(app)

        for award_winner in award_winners_qs:
            squad_stats.add_award_winner(award_winner)

        return SquadStatsType(totals=squad_stats.totals, squad=squad_stats.squad())

    def resolve_committee_positions(self):
        return CommitteePosition.objects.all()

    def resolve_committee_memberships(self):
        return CommitteeMembership.objects.all()

    def resolve_squad_memberships(self):
        return SquadMembership.objects.all()

    def resolve_members(self):
        return Member.objects.all()
