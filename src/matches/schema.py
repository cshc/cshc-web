"""
GraphQL Schema for matches etc
"""

import graphene
import django_filters
from graphene_django_extras import DjangoListObjectType, DjangoObjectType
from graphene_django_optimizedextras import OptimizedDjangoListObjectField, get_paginator
from awards.schema import MatchAwardWinnerList
from awards.models import MatchAward
from .models import Match, Appearance, GoalKing


class GoalKingFilter(django_filters.FilterSet):
    """ Goal King Filters """
    team = django_filters.CharFilter(name='team', method='filter_team')

    def filter_team(self, queryset, name, value):
        # filter for entries where the player has scored for the corresponding team.
        filter_name = "{}_goals__gt".format(value)
        kwargs = {
            filter_name: 0
        }
        return queryset.filter(**kwargs).order_by("-{}_goals".format(value))

    class Meta:
        model = GoalKing
        fields = ['team', 'member__gender', 'season__slug']


class MatchFilter(django_filters.FilterSet):
    mom = django_filters.CharFilter(name='mom', method='filter_mom')
    lom = django_filters.CharFilter(name='lom', method='filter_lom')

    def filter_mom(self, queryset, name, value):
        # filter for matches where the given member won the Man of the Match award.
        kwargs = {
            'award_winners__member_id': value,
            'award_winners__award__name': MatchAward.MOM,
        }
        return queryset.filter(**kwargs)

    def filter_lom(self, queryset, name, value):
        # filter for matches where the given member won the Lemon of the Match award.
        kwargs = {
            'award_winners__member_id': value,
            'award_winners__award__name': MatchAward.LOM,
        }
        return queryset.filter(**kwargs)

    class Meta:
        model = Match
        fields = {
            'mom': ['exact'],
            'lom': ['exact'],
            'venue__slug': ['exact'],
            'venue_id': ['exact'],
            'opp_team__name': ['exact'],
            'opp_team__club__slug': ['exact'],
            'fixture_type': ['exact'],
            'date': ['exact', 'gte', 'lte'],
            'our_team__slug': ['exact'],
            'our_team__gender': ['exact'],
            'season__slug': ['exact'],
            'report_author_id': ['exact'],
            'appearances__member_id': ['in', 'exact'],
        }

    order_by = django_filters.OrderingFilter(
        fields=(
            ('our_score', 'score'),
            ('date', 'date'),
            ('fixtureType', 'fixtureType'),
            ('our_team__short_name', 'ourTeam'),
            ('opp_team__name', 'oppTeam'),
            ('venue__short_name', 'venue'),
        )
    )


class AppearanceType(DjangoObjectType):
    """ GraphQL node representing a member's appearance in a match """
    class Meta:
        model = Appearance
        filter_fields = {
            'goals': ['gte'],
        }


class AppearanceList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of appearances"
        model = Appearance
        pagination = get_paginator()


class MatchType(DjangoObjectType):
    """ GraphQL node representing a match/fixture """
    has_report = graphene.Boolean()
    kit_clash = graphene.Boolean()
    match_title_text = graphene.String()

    appearances = OptimizedDjangoListObjectField(AppearanceList)
    award_winners = OptimizedDjangoListObjectField(MatchAwardWinnerList)

    class Meta:
        model = Match

    def resolve_has_report(self, info):
        return self.has_report()

    def resolve_kit_clash(self, info):
        return self.kit_clash()

    def resolve_match_title_text(self, info):
        return self.match_title_text()


class MatchList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of matches"
        model = Match
        pagination = get_paginator()


class GoalKingType(DjangoObjectType):
    """ GraphQL node representing an entry in the Goal King stats """
    gender = graphene.String()

    class Meta:
        model = GoalKing
        filter_fields = ['member__gender', 'season__slug']

    def resolve_gender(self, info):
        return self.member.gender


class GoalKingList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of goal king entries"
        model = GoalKing
        pagination = get_paginator()


class Query(graphene.ObjectType):
    """ GraphQL query for members etc """

    matches = OptimizedDjangoListObjectField(
        MatchList, filterset_class=MatchFilter)

    appearances = OptimizedDjangoListObjectField(AppearanceList)

    goal_king_entries = OptimizedDjangoListObjectField(
        GoalKingList, filterset_class=GoalKingFilter)

    def resolve_goal_king_entries(self, info, **kwargs):
        order_field = '-total_goals'
        if 'team' in kwargs:
            team = kwargs.pop('team')
            order_field = '-{}_goals'.format(team)
            kwargs["{}_goals__gt".format(team)] = 0

        return GoalKing.objects.filter(total_goals__gt=0).filter(**kwargs).order_by(order_field, '-gpg')
