"""
GraphQL Schema for Members etc
"""

import graphene
import django_filters
from graphene_django_extras import DjangoListObjectType, DjangoObjectType
from graphene_django_optimizedextras import OptimizedDjangoListObjectField, get_paginator
from django.db.models import (Count, Sum, Q)
from matches.models import Appearance
from awards.models import MatchAwardWinner
from teams.models import TeamCaptaincy
from teams.schema import ClubTeamType
from core.filters import AndFilter
from core.utils import get_thumbnail_url
from competitions.schema import SeasonType
from .stats import SquadPlayingStats, AllSeasonsPlayingStats
from .models import CommitteePosition, Member, CommitteeMembership, SquadMembership


class NumberInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class MemberFilter(AndFilter):
    # Do 'in' lookups on 'pref_position'
    pref_position__in = NumberInFilter(name='pref_position', lookup_expr='in')
    name = django_filters.CharFilter(name='first_name', method="filter_name")

    def filter_name(self, queryset, name, value):
        # filter by first name or last name
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )

    class Meta:
        model = Member
        fields = ['is_current', 'gender', 'pref_position', 'first_name', 'known_as', 'last_name',
                  'appearances__match__season__slug', 'appearances__match__our_team__slug',
                  'teamcaptaincy__season__slug', 'squadmembership__season__slug', 'squadmembership__team__slug',
                  'is_umpire', 'is_coach']


class CommitteePositionType(DjangoObjectType):
    """ GraphQL node representing a committee position """
    class Meta:
        model = CommitteePosition


class CommitteePositionList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of committee positions"
        model = CommitteePosition
        pagination = get_paginator()


class CommitteeMembershipType(DjangoObjectType):
    """ GraphQL node representing a committee membership """
    class Meta:
        model = CommitteeMembership
        filter_fields = {
            'member_id': ['exact'],
            'position__name': ['exact', 'icontains', 'istartswith'],
        }


class CommitteeMembershipList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of committee memberships"
        model = CommitteeMembership
        pagination = get_paginator()


class SquadMembershipType(DjangoObjectType):
    """ GraphQL node representing a member's squad membership """
    class Meta:
        model = SquadMembership


class SquadMembershipList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of squad memberships"
        model = SquadMembership
        pagination = get_paginator()


class MemberType(DjangoObjectType):
    """ GraphQL node representing a club member """
    thumb_url = graphene.String(size=graphene.String(), crop=graphene.String())
    pref_position = graphene.String()
    num_appearances = graphene.Int()
    goals = graphene.Int()
    full_name = graphene.String()

    class Meta:
        model = Member
        filter_fields = {
            'first_name': ['exact', 'icontains', 'istartswith'],
            'known_as': ['exact', 'icontains', 'istartswith'],
            'last_name': ['exact', 'icontains', 'istartswith'],
            'is_current': ['exact'],
            'pref_position': ['in'],
            'gender': ['exact'],
            'appearances__match__season__slug': ['exact'],
            'appearances__match__our_team__slug': ['exact'],
            'teamcaptaincy__season__slug': ['exact'],
        }

    def resolve_address_known(self, info):
        return self.address_known()

    def resolve_full_address(self, info):
        return self.full_address()

    def resolve_first_name(self, info):
        return self.pref_first_name()

    def resolve_num_appearances(self, info):
        return self.num_appearances

    def resolve_goals(self, info):
        return self.goals

    def resolve_thumb_url(self, info, size='50x50', crop=None):
        return get_thumbnail_url(self.profile_pic, size, crop, self.profile_pic_cropping)

    def resolve_pref_position(self, info):
        return self.get_pref_position_display()

    def resolve_full_name(self, info):
        return self.full_name()


class MemberList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of members"
        model = Member
        pagination = get_paginator()


class TeamRepresentationType(graphene.ObjectType):
    team = graphene.Field(ClubTeamType)
    appearance_count = graphene.Int()


class MemberStatsType(graphene.ObjectType):
    member = graphene.Field(MemberType)
    played = graphene.Int()
    won = graphene.Int()
    drawn = graphene.Int()
    lost = graphene.Int()
    goals = graphene.Int()
    goals_for = graphene.Int()
    goals_against = graphene.Int()
    total_points = graphene.Int()
    clean_sheets = graphene.Int()
    lom = graphene.Int()
    mom = graphene.Int()
    is_captain = graphene.Boolean()
    is_vice_captain = graphene.Boolean()
    team_representations = graphene.List(TeamRepresentationType)

    def resolve_member(self, info):
        return self.member

    def resolve_total_points(self, info):
        return self.total_points()

    def resolve_team_representations(self, info):
        return sorted(self.team_representations.values(), key=lambda tr: tr.team.position)


class SeasonRepresentationType(graphene.ObjectType):
    season = graphene.Field(SeasonType)
    member_stats = graphene.Field(MemberStatsType)


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


class AddNewMemberInput(graphene.InputObjectType):
    """ Input Type for adding a new member """
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    gender = graphene.String(required=True)


class AddMember(graphene.relay.ClientIDMutation):

    class Input:
        member = graphene.Argument(AddNewMemberInput)

    errors = graphene.List(graphene.String)
    new_member = graphene.Field(MemberType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        member_data = input['member']
        member, created = Member.objects.get_or_create(
            first_name=member_data.first_name,
            last_name=member_data.last_name,
            gender=member_data.gender,
            defaults={'is_current': True},
        )
        errors = ['This member already exists'] if not created else None

        return cls(new_member=member, errors=errors)


def post_optimize_members(queryset, **kwargs):
    # Slight hack to manually convert a comma-separated list of pref_position ints to an array of ints
    if 'pref_position__in' in kwargs:
        pref_positions = [
            int(x) for x in kwargs['pref_position__in'].split(",")]
        queryset = queryset.filter(pref_position__in=pref_positions)

    # Manually create text search by first name OR last name
    text_query = None
    if 'name' in kwargs:
        text_search = kwargs.pop('name')
        text_query = Q(first_name__istartswith=text_search) | Q(
            last_name__istartswith=text_search) | Q(known_as__istartswith=text_search)
        queryset = queryset.filter(text_query)

    queryset = queryset.annotate(num_appearances=Count(
        'appearances'), goals=Sum('appearances__goals'))

    return queryset


class Query(graphene.ObjectType):
    """ GraphQL query for members etc """
    committee_positions = OptimizedDjangoListObjectField(CommitteePositionList)

    committee_memberships = OptimizedDjangoListObjectField(
        CommitteeMembershipList)

    squad_memberships = OptimizedDjangoListObjectField(SquadMembershipList)

    members = OptimizedDjangoListObjectField(
        MemberList, filterset_class=MemberFilter, post_optimize=post_optimize_members)

    squad_stats = graphene.Field(
        SquadStatsType, season=graphene.Int(), team=graphene.Int(), fixture_Type=graphene.String())

    member_stats = graphene.List(
        SeasonRepresentationType, member_Id=graphene.Int(), fixture_Type=graphene.String())

    def resolve_squad_stats(self, info, **kwargs):
        # Get playing stats for the team, including squad members
        app_qs = Appearance.objects.select_related('member', 'match__our_team')
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

    def resolve_member_stats(self, info, **kwargs):
        # Get playing stats for the specified member
        app_qs = Appearance.objects.filter(member=kwargs['member_Id']).select_related(
            'member', 'match__our_team', 'match__season')
        award_winners_qs = MatchAwardWinner.objects.filter(
            member=kwargs['member_Id']).select_related('award', 'match__season', 'member')

        if 'fixture_Type' in kwargs:
            app_qs = app_qs.filter(match__fixture_type=kwargs['fixture_Type'])
            award_winners_qs = award_winners_qs.filter(
                match__fixture_type=kwargs['fixture_Type'])

        season_stats = AllSeasonsPlayingStats()

        for app in app_qs:
            season_stats.add_appearance(app)

        for award_winner in award_winners_qs:
            season_stats.add_award_winner(award_winner)

        return season_stats.seasons.values()


class Mutation(graphene.ObjectType):
    add_member = AddMember.Field()
