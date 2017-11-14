"""
GraphQL Schema for Members etc
"""

import graphene
import django_filters
from django.db.models import (Count, Sum)
from easy_thumbnails.files import get_thumbnailer
from graphene_django import DjangoObjectType
from matches.models import Appearance
from awards.models import MatchAwardWinner
from teams.models import TeamCaptaincy
from core import schema_helper
from .stats import SquadPlayingStats
from .models import CommitteePosition, Member, CommitteeMembership, SquadMembership


member_field_map = {
    "squadmembership_set": ("squadmembership_set", "prefetch"),
    "teamcaptaincy_set": ("teamcaptaincy_set", "prefetch"),
}


class NumberInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class MemberFilter(django_filters.FilterSet):
    # Do 'in' lookups on 'pref_position'
    pref_position__in = NumberInFilter(name='pref_position', lookup_expr='in')

    class Meta:
        model = Member
        fields = ['is_current', 'gender', 'pref_position',
                  'appearances__match__season__slug', 'appearances__match__our_team__slug']


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
    num_appearances = graphene.Int()
    goals = graphene.Int()

    class Meta:
        model = Member
        interfaces = (graphene.Node, )
        filter_fields = {
            'first_name': ['exact', 'icontains', 'istartswith'],
            'last_name': ['exact', 'icontains', 'istartswith'],
            'is_current': ['exact'],
            'pref_position': ['in'],
            'gender': ['exact'],
            'appearances__match__season__slug': ['exact'],
            'appearances__match__our_team__slug': ['exact'],
        }

    def resolve_model_id(self, info):
        return self.id

    def resolve_num_appearances(self, info):
        return self.num_appearances

    def resolve_goals(self, info):
        return self.goals

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
    is_captain = graphene.Boolean()
    is_vice_captain = graphene.Boolean()

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
    members = schema_helper.OptimizableFilterConnectionField(
        MemberType, filterset_class=MemberFilter)
    squad_stats = graphene.Field(
        SquadStatsType, season=graphene.Int(), team=graphene.Int(), fixture_Type=graphene.String())

    def resolve_members(self, info, **kwargs):
        # Slight hack to manually convert a comma-separated list of pref_position ints to an array of ints
        if 'pref_position__in' in kwargs:
            kwargs['pref_position__in'] = [
                int(x) for x in kwargs['pref_position__in'].split(",")]
        return schema_helper.optimize(Member.objects.annotate(num_appearances=Count('appearances'), goals=Sum('appearances__goals')).filter(**kwargs),
                                      info,
                                      member_field_map).distinct()

    def resolve_squad_stats(self, info, **kwargs):
        # Get playing stats for the team, including squad members
        app_qs = Appearance.objects.select_related('member', 'match')
        award_winners_qs = MatchAwardWinner.objects.select_related('award')
        qs_captains = TeamCaptaincy.objects

        if 'team' in kwargs:
            app_qs = app_qs.filter(match__our_team_id=kwargs['team'])
            award_winners_qs = award_winners_qs.filter(
                match__our_team_id=kwargs['team'])
            qs_captains = qs_captains.filter(team_id=kwargs['team'])
        else:
            app_qs = app_qs.select_related('match__our_team')
            award_winners_qs = award_winners_qs.select_related(
                'match__our_team')

        if 'season' in kwargs:
            app_qs = app_qs.filter(match__season_id=kwargs['season'])
            award_winners_qs = award_winners_qs.filter(
                match__season_id=kwargs['season'])
            qs_captains = qs_captains.filter(season_id=kwargs['season'])
        else:
            app_qs = app_qs.select_related('match__season')
            award_winners_qs = award_winners_qs.select_related('match__season')

        if 'fixture_Type' in kwargs:
            app_qs = app_qs.filter(match__fixture_type=kwargs['fixture_Type'])
            award_winners_qs = award_winners_qs.filter(
                match__fixture_type=kwargs['fixture_Type'])

        squad_stats = SquadPlayingStats()

        for app in app_qs:
            squad_stats.add_appearance(app)

        for award_winner in award_winners_qs:
            squad_stats.add_award_winner(award_winner)

        squad_stats.add_captains(qs_captains)

        return SquadStatsType(totals=squad_stats.totals, squad=squad_stats.squad())

    def resolve_committee_positions(self):
        return CommitteePosition.objects.all()

    def resolve_committee_memberships(self):
        return CommitteeMembership.objects.all()

    def resolve_squad_memberships(self):
        return SquadMembership.objects.all()
