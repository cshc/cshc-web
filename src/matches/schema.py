"""
GraphQL Schema for matches etc
"""

import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Prefetch
from core import schema_helper
from core.cursor import CursorPaginatedConnectionField
from competitions.schema import SeasonNode
from awards.models import MatchAwardWinner
from awards.schema import MatchAwardWinnerNode
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
    class Meta:
        model = Match
        exclude = []

    order_by = django_filters.OrderingFilter(
        fields=(
            ('our_score', 'our_score'),
        )
    )


class AppearanceNode(DjangoObjectType):
    """ GraphQL node representing a member's appearance in a match """
    class Meta:
        model = Appearance
        interfaces = (graphene.relay.Node, )
        filter_fields = {
            'goals': ['gte'],
        }

    def prefetch_member(queryset, related_queryset):
        return queryset.select_related('member')

    def prefetch_match(queryset, related_queryset):
        return queryset.select_related('match')


class AppearanceConnection(graphene.relay.Connection):
    class Meta:
        node = AppearanceNode


class MatchNode(DjangoObjectType):
    """ GraphQL node representing a match/fixture """
    model_id = graphene.String()
    has_report = graphene.Boolean()
    kit_clash = graphene.Boolean()

    appearances = CursorPaginatedConnectionField(AppearanceNode)
    award_winners = CursorPaginatedConnectionField(MatchAwardWinnerNode)

    class Meta:
        model = Match
        interfaces = (graphene.relay.Node, )
        filter_fields = ['venue__name', 'opp_team__name', 'opp_team__club__slug',
                         'our_team__slug', 'season__slug', 'appearances__member__id', 'report_author__id']

    def resolve_model_id(self, info):
        return self.id

    def resolve_has_report(self, info):
        return self.has_report()

    def resolve_kit_clash(self, info):
        return self.kit_clash()

    def prefetch_venue(queryset, related_queryset):
        print('Prefetch venue')
        return queryset.select_related('venue')

    def prefetch_our_team(queryset, related_queryset):
        print('Prefetch our_team')
        return queryset.select_related('our_team')

    def prefetch_opp_team(queryset, related_queryset):
        return queryset.select_related('opp_team__club')

    def prefetch_season(queryset, related_queryset):
        return queryset.select_related('season')

    def prefetch_division(queryset, related_queryset):
        return queryset.select_related('division')

    def prefetch_cup(queryset, related_queryset):
        return queryset.select_related('cup')

    def prefetch_report_author(queryset, related_queryset):
        return queryset.select_related('report_author')

    # def optimize_appearances(queryset, **kwargs):
    #     return queryset.prefetch_related(Prefetch('appearances', queryset=Appearance.objects.select_related('member')))

    # def optimize_award_winners(queryset, **kwargs):
    #     return queryset.prefetch_related(Prefetch('award_winners', queryset=MatchAwardWinner.objects.select_related('member', 'award')))


class MatchConnection(graphene.relay.Connection):
    class Meta:
        node = MatchNode


goalking_field_map = {
    "member": ("member", "select"),
}


class GoalKingType(DjangoObjectType):
    """ GraphQL node representing an entry in the Goal King stats """
    gender = graphene.String()

    class Meta:
        model = GoalKing
        interfaces = (graphene.Node, )
        filter_fields = ['member__gender', 'season__slug']

    def resolve_gender(self, info):
        return self.member.gender


class Query(graphene.ObjectType):
    """ GraphQL query for members etc """

    matches2 = DjangoFilterConnectionField(
        MatchNode, filterset_class=MatchFilter)

    matches = schema_helper.OptimizableFilterConnectionField(MatchNode)

    matches_cursor = CursorPaginatedConnectionField(MatchNode)

    seasons_cursor = CursorPaginatedConnectionField(SeasonNode)

    appearances = graphene.List(AppearanceNode)
    goal_king_entries = schema_helper.OptimizableFilterConnectionField(
        GoalKingType, filterset_class=GoalKingFilter)

    def resolve_matches_cursor(self, info, **kwargs):
        return Match.objects.all()

    def resolve_matches(self, info, **kwargs):
        appearances_qs = Appearance.objects.select_related('member')
        appearances_prefetch = Prefetch('appearances', queryset=appearances_qs)
        award_winners_qs = MatchAwardWinner.objects.select_related(
            'member', 'award')
        award_winner_prefetch = Prefetch(
            'award_winners', queryset=award_winners_qs)
        return Match.objects.filter(**kwargs).select_related('our_team', 'opp_team__club', 'venue').prefetch_related(appearances_prefetch, award_winner_prefetch)

    def resolve_appearances(self):
        return Appearance.objects.all()

    def resolve_goal_king_entries(self, info, **kwargs):
        order_field = '-total_goals'
        if 'team' in kwargs:
            team = kwargs.pop('team')
            order_field = '-{}_goals'.format(team)
            kwargs["{}_goals__gt".format(team)] = 0

        return schema_helper.optimize(GoalKing.objects.filter(total_goals__gt=0).filter(**kwargs).order_by(order_field, '-gpg'), info, goalking_field_map)
