"""
GraphQL Schema for opposition clubs and teams etc
"""

import graphene
from graphene_django_extras import DjangoListObjectType, DjangoObjectType
from graphene_django_optimizedextras import OptimizedDjangoListObjectField, get_paginator
from .models import Club, Team, ClubStats


class ClubType(DjangoObjectType):
    """ GraphQL node representing an opposition club """
    class Meta:
        model = Club


class ClubList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of oppositions clubs"
        model = Club
        pagination = get_paginator()


class TeamType(DjangoObjectType):
    """ GraphQL node representing an opposition team """
    class Meta:
        model = Team


class TeamList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of opposition teams"
        model = Team
        pagination = get_paginator()


class ClubStatsType(DjangoObjectType):
    """ GraphQL node representing a club stats record """
    home_played = graphene.Int()
    away_played = graphene.Int()
    total_played = graphene.Int()
    total_won = graphene.Int()
    total_drawn = graphene.Int()
    total_lost = graphene.Int()
    total_gf = graphene.Int()
    total_ga = graphene.Int()
    avg_gf = graphene.Float()
    avg_ga = graphene.Float()
    avg_gd = graphene.Float()
    avg_points = graphene.Float()
    is_club_total = graphene.Boolean()

    class Meta:
        model = ClubStats
        filter_fields = ['club__slug']

    def resolve_home_played(self, info):
        return self.home_played

    def resolve_away_played(self, info):
        return self.away_played

    def resolve_total_played(self, info):
        return self.total_played

    def resolve_total_won(self, info):
        return self.total_won

    def resolve_total_drawn(self, info):
        return self.total_drawn

    def resolve_total_lost(self, info):
        return self.total_lost

    def resolve_total_gf(self, info):
        return self.total_gf

    def resolve_total_ga(self, info):
        return self.total_ga

    def resolve_avg_gf(self, info):
        return self.avg_gf

    def resolve_avg_ga(self, info):
        return self.avg_ga

    def resolve_avg_gd(self, info):
        return self.avg_gd

    def resolve_avg_points(self, info):
        return self.avg_points

    def resolve_is_club_total(self, info):
        return self.is_club_total


class ClubStatsList(DjangoListObjectType):
    class Meta:
        description = "Type definition for a list of club stats"
        model = ClubStats
        pagination = get_paginator()


class Query(graphene.ObjectType):
    """ GraphQL query for members etc """
    opposition_clubs = OptimizedDjangoListObjectField(ClubList)
    opposition_teams = OptimizedDjangoListObjectField(TeamList)
    opposition_club_stats = OptimizedDjangoListObjectField(ClubStatsList)

    def resolve_opposition_club_stats(self, info, **kwargs):
        if 'club__slug' in kwargs:
            return ClubStats.objects.select_related('team').filter(club__slug=kwargs['club__slug']).order_by('team__position')
        return ClubStats.objects.totals()
