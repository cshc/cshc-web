""" Views for the Availability app.
"""
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from core.models import Gender, TeamGender
from core.views import MemberSelectionMixin
from teams.models import ClubTeam, TeamCaptaincy
from members.models import Member
from competitions.models import Season


class ManageAvailabilityView(MemberSelectionMixin, TemplateView):
    """ Base class for availability management views """
    template_name = 'availability/manage_availability.html'

    def get_context_data(self, **kwargs):
        context = super(ManageAvailabilityView,
                        self).get_context_data(**kwargs)

        context['props'] = {}
        return context


class ManageTeamPlayingAvailabilityView(UserPassesTestMixin, ManageAvailabilityView):
    """ React view that allows the user to manage the playing availabilities 
        for upcoming matches for a specific team.
    """
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return (user.is_authenticated and
                user.member is not None and
                user.member.id in list(TeamCaptaincy.objects.current().filter(team__slug=self.kwargs['slug']).values_list('member_id', flat=True)))

    def get_context_data(self, **kwargs):
        context = super(ManageTeamPlayingAvailabilityView,
                        self).get_context_data(**kwargs)

        team = ClubTeam.objects.get(slug=kwargs['slug'])

        member_fields = ['id', 'first_name', 'last_name', 'gender']
        player_suggestions = []
        current_season = Season.current()

        # 1. Get all possible members
        member_qs = Member.objects.filter(is_current=True)
        if team.gender == TeamGender.Mens:
            member_qs = member_qs.filter(gender=Gender.Male)
        elif team.gender == TeamGender.Ladies:
            member_qs = member_qs.filter(gender=Gender.Female)
        else:
            member_qs = member_qs.order_by('gender')

        player_suggestions = self.to_player_list(
            member_qs.only(*member_fields))

        # 2. Get members who have played in this team before this season
        played_this_season_qs = Member.objects.filter(
            appearances__match__season=current_season,
            appearances__match__our_team=team).order_by(
                '-first_name', '-last_name').only(*member_fields)

        played_this_season = self.to_player_list(played_this_season_qs)

        for player in played_this_season:
            self.prioritize(player_suggestions, player)

        # 3. Get members who are in the squad
        squad_members_qs = Member.objects.filter(squadmembership__team=team,
                                                 squadmembership__season=current_season).order_by('-first_name', '-last_name').only(*member_fields)

        squad_members = self.to_player_list(squad_members_qs)

        for player in squad_members:
            self.prioritize(player_suggestions, player)

        context['title'] = 'Manage {} Playing Availability'.format(
            team.short_name)
        context['team'] = team
        context['props']['teamId'] = team.id
        context['props']['availabilityType'] = 'playing'
        context['props']['playerOptions'] = player_suggestions
        return context


class ManageUmpiringAvailabilityView(PermissionRequiredMixin, ManageAvailabilityView):
    """ React view that allows the user to manage the umpiring availabilities 
        for upcoming matches for all teams.
    """
    permission_required = 'availability.manage_umpiring_matchavailability'

    def get_context_data(self, **kwargs):
        context = super(ManageUmpiringAvailabilityView,
                        self).get_context_data(**kwargs)

        context['title'] = 'Manage Umpiring Availability'
        context['props']['availabilityType'] = 'umpiring'
        return context
