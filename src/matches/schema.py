"""
GraphQL Schema for matches etc
"""

import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Prefetch
from core import schema_helper
from awards.models import MatchAwardWinner
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


class MatchNode(DjangoObjectType):
    """ GraphQL node representing a match/fixture """
    model_id = graphene.String()
    has_report = graphene.Boolean()
    kit_clash = graphene.Boolean()

    class Meta:
        model = Match
        interfaces = (graphene.relay.Node, )
        filter_fields = ['venue__name', 'opp_team__name', 'opp_team__club__slug',
                         'our_team__slug', 'season__slug']

    def resolve_model_id(self, info):
        return self.id

    def resolve_has_report(self, info):
        return self.has_report()

    def resolve_kit_clash(self, info):
        return self.kit_clash()


class AppearanceNode(DjangoObjectType):
    """ GraphQL node representing a member's appearance in a match """
    class Meta:
        model = Appearance
        # interfaces = (graphene.relay.Node, )
        # filter_fields = {
        #     'goals': ['gte'],
        # }


goalking_field_map = {
    "member": ("member", "select"),
}


class GoalKingType(DjangoObjectType):
    """ GraphQL node representing an entry in the Goal King stats """
    gender = graphene.String()
    goals_per_game = graphene.Float()
    miles_per_game = graphene.Float()

    class Meta:
        model = GoalKing
        interfaces = (graphene.Node, )
        filter_fields = ['member__gender', 'season__slug']

    def resolve_gender(self, info):
        return self.member.gender

    def resolve_goals_per_game(self, info):
        return self.goals_per_game()

    def resolve_miles_per_game(self, info):
        return self.miles_per_game()


class Query(graphene.ObjectType):
    """ GraphQL query for members etc """
    matches = schema_helper.OptimizableFilterConnectionField(MatchNode)
    appearances = graphene.List(AppearanceNode)
    goal_king_entries = schema_helper.OptimizableFilterConnectionField(
        GoalKingType, filterset_class=GoalKingFilter)

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
            order_field = '-{}_goals'.format(kwargs['team'])
            kwargs["{}_goals__gt".format(kwargs['team'])] = 0
            del kwargs['team']

        return schema_helper.optimize(GoalKing.objects.filter(total_goals__gt=0).filter(**kwargs).order_by(order_field), info, goalking_field_map)
