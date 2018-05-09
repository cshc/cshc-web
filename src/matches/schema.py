"""
GraphQL Schema for matches etc
"""

import logging
import traceback
import graphene
import django_filters
from django.db.models import F, Q
from graphene_django_extras import DjangoListObjectType, DjangoObjectType
from graphene_django_optimizedextras import OptimizedDjangoListObjectField, get_paginator
from core.filters import AndFilter
from availability.schema import MatchAvailabilityList, MatchAvailabilityFilter
from awards.schema import MatchAwardWinnerList, MatchAwardWinnerInput
from awards.models import MatchAward, MatchAwardWinner
from .models import Match, Appearance, GoalKing

LOG = logging.getLogger(__name__)


class GoalKingFilter(AndFilter):
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


class MatchFilter(AndFilter):
    mom = django_filters.CharFilter(name='mom', method='filter_mom')
    lom = django_filters.CharFilter(name='lom', method='filter_lom')
    result = django_filters.CharFilter(name='result', method='filter_result')

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

    def filter_result(self, queryset, name, value):
        # Filter for a particular result
        final_scores_provided = Q(our_score__isnull=False) and Q(
            opp_score__isnull=False)
        queryset = queryset.filter(final_scores_provided)
        if value.lower() == 'won':
            return queryset.filter(our_score__gt=F('opp_score'))
        elif value.lower() == 'lost':
            return queryset.filter(our_score__lt=F('opp_score'))
        elif value.lower() == 'drawn':
            return queryset.filter(our_score=F('opp_score'))
        else:
            raise Exception('Invalid result specified: ' + value)

    class Meta:
        model = Match
        fields = {
            'mom': ['exact'],
            'lom': ['exact'],
            'result': ['result'],
            'venue__slug': ['exact'],
            'venue_id': ['exact'],
            'opp_team__name': ['exact'],
            'opp_team_id': ['exact'],
            'opp_team__club__slug': ['exact'],
            'fixture_type': ['exact'],
            'date': ['exact', 'gte', 'lte', 'lt', 'gt'],
            'our_team_id': ['exact'],
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
            ('fixture_type', 'fixtureType'),
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
    result = graphene.String()
    is_home = graphene.Boolean()

    appearances = OptimizedDjangoListObjectField(AppearanceList)
    award_winners = OptimizedDjangoListObjectField(MatchAwardWinnerList)
    availabilities = OptimizedDjangoListObjectField(
        MatchAvailabilityList, filterset_class=MatchAvailabilityFilter)

    class Meta:
        model = Match

    def resolve_is_home(self, info):
        return self.is_home

    def resolve_has_report(self, info):
        return self.has_report()

    def resolve_kit_clash(self, info):
        return self.kit_clash()

    def resolve_match_title_text(self, info):
        return self.match_title_text()

    def resolve_result(self, info):
        return self.result_display()


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


class AppearanceInput(graphene.InputObjectType):
    member_id = graphene.Int()
    match_id = graphene.Int(required=False)
    greenCard = graphene.Boolean(required=False)
    yellowCard = graphene.Boolean(required=False)
    redCard = graphene.Boolean(required=False)
    goals = graphene.Int(required=False)


class EditMatchInput(graphene.InputObjectType):
    """ Input Type for updating a match """
    match_id = graphene.Int()
    our_score = graphene.Int(required=False)
    opp_score = graphene.Int(required=False)
    our_ht_score = graphene.Int(required=False)
    opp_ht_score = graphene.Int(required=False)
    alt_outcome = graphene.String(required=False)
    report_author_id = graphene.Int(required=False)
    report_title = graphene.String(required=False)
    report_content = graphene.String(required=False)

    appearances = graphene.List(AppearanceInput)
    awardWinners = graphene.List(MatchAwardWinnerInput)


class UpdateMatch(graphene.relay.ClientIDMutation):

    class Input:
        match = graphene.Argument(EditMatchInput)

    errors = graphene.List(graphene.String)
    match = graphene.Field(MatchType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        match_data = input['match']
        errors = []
        try:
            match = Match.objects.get(id=match_data.match_id)
            match.our_score = match_data.our_score
            match.opp_score = match_data.opp_score
            match.our_ht_score = match_data.our_ht_score
            match.opp_ht_score = match_data.opp_ht_score
            match.alt_outcome = match_data.alt_outcome
            match.report_author_id = match_data.report_author_id
            match.report_title = match_data.report_title
            # SplitField has issues with being set to None (so default to an empty string)
            match.report_body = match_data.report_content if match_data.report_content else ''
            match.clean()
            match.save()

            # UPDATE ALL APPEARANCES
            # 1. Delete appearances not listed in the mutation input
            member_ids = [a.member_id for a in match_data.appearances]
            deleted, _ = Appearance.objects.filter(
                match_id=match_data.match_id).exclude(member_id__in=member_ids).delete()
            LOG.info('Deleted {} appearances'.format(deleted))

            # 2. Add/update all appearances from the mutation input
            for app_data in match_data.appearances:
                app, created = Appearance.objects.get_or_create(
                    member_id=app_data.member_id, match_id=match_data.match_id)
                app.goals = app_data.goals if app_data.goals else 0
                app.greenCard = app_data.greenCard if app_data.greenCard else False
                app.yellowCard = app_data.yellowCard if app_data.yellowCard else False
                app.redCard = app_data.redCard if app_data.redCard else False
                app.clean()
                app.save()
                if created:
                    LOG.info(
                        'Added appearance for member {}'.format(app.member_id))
                else:
                    LOG.info(
                        'Updated appearance for member {}'.format(app.member_id))

            LOG.info('{} appearances for match {}'.format(
                len(match_data.appearances), match_data.match_id))

            # UPDATE ALL AWARD WINNERS
            mom = MatchAward.objects.mom()
            lom = MatchAward.objects.lom()

            # 1. Delete award winners not listed in the mutation input
            award_winners_delete_qs = MatchAwardWinner.objects.filter(
                match_id=match_data.match_id)
            for award_winner_data in match_data.awardWinners:
                if award_winner_data.member_id:
                    award_winners_delete_qs = award_winners_delete_qs.exclude(
                        member_id=award_winner_data.member_id, award__name=award_winner_data.award)
                else:
                    award_winners_delete_qs = award_winners_delete_qs.exclude(
                        awardee=award_winner_data.awardee, award__name=award_winner_data.award)

            award_winners_deleted, _ = award_winners_delete_qs.delete()
            LOG.info('Deleted {} award winners'.format(award_winners_deleted))

            # 2. Add/update all award winners from the mutation input
            for award_winner_data in match_data.awardWinners:
                query_kwargs = {
                    'match_id': match_data.match_id,
                    'award_id': mom.id if award_winner_data.award == MatchAward.MOM else lom.id,
                }
                if award_winner_data.member_id:
                    query_kwargs['member_id'] = award_winner_data.member_id
                else:
                    query_kwargs['awardee'] = award_winner_data.awardee
                award_winner, created = MatchAwardWinner.objects.get_or_create(defaults={'comment': award_winner_data.comment},
                                                                               **query_kwargs)
                award_winner.comment = award_winner_data.comment
                award_winner.clean()
                award_winner.save()
                if created:
                    LOG.info('Added award winner: {}'.format(award_winner))
                else:
                    LOG.info('Updated award winner: {}'.format(award_winner))

        except Match.DoesNotExist:
            errors.append('Can\'t find match with ID {}'.format(
                match_data.match_id))
            match = None
        except Exception as e:
            traceback.print_exc()
            match = None
            errors.append("{}".format(e))

        return cls(match=match, errors=errors)


def post_optimize_goal_king_entries(queryset, **kwargs):
    order_field = '-total_goals'
    if 'team' in kwargs:
        team = kwargs.pop('team')
        order_field = '-{}_goals'.format(team)
        team_kwargs = {}
        team_kwargs["{}_goals__gt".format(team)] = 0
        queryset = queryset.filter(**team_kwargs)

    return queryset.filter(total_goals__gt=0).order_by(order_field, '-gpg')


class Query(graphene.ObjectType):
    """ GraphQL query for members etc """

    matches = OptimizedDjangoListObjectField(
        MatchList, filterset_class=MatchFilter)

    appearances = OptimizedDjangoListObjectField(AppearanceList)

    goal_king_entries = OptimizedDjangoListObjectField(
        GoalKingList, filterset_class=GoalKingFilter, post_optimize=post_optimize_goal_king_entries)


class Mutation(graphene.ObjectType):
    update_match = UpdateMatch.Field()
