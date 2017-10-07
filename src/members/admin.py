""" Configuration of Members models for the admin interface.
"""

from django.contrib import admin
from image_cropping import ImageCroppingMixin
from members.models import Member, CommitteeMembership, CommitteePosition, SquadMembership


class SquadMembershipInline(admin.TabularInline):
    """ Allows squad membership to be edited from the admin page of the member model."""
    model = SquadMembership
    extra = 0


@admin.register(Member)
class MemberAdmin(ImageCroppingMixin, admin.ModelAdmin):
    """ Admin interface definition for the Member model."""
    model = Member
    inlines = (SquadMembershipInline,)
    search_fields = ('first_name', 'last_name')
    list_filter = ('is_current', 'gender', 'pref_position')
    list_display = ('__str__', 'user', 'gender',
                    'pref_position', 'is_current')


@admin.register(SquadMembership)
class SquadMembershipAdmin(admin.ModelAdmin):
    """ Admin interface definition for the SquadMembership model."""
    model = SquadMembership
    search_fields = ('member__first_name', 'member__last_name')
    list_filter = ('member', 'team', 'season')
    list_display = ('__str__', 'member', 'team', 'season')


@admin.register(CommitteePosition)
class CommitteePositionAdmin(admin.ModelAdmin):
    """ Admin interface definition for the CommitteePosition model."""
    model = CommitteePosition
    search_fields = ('name',)
    list_filter = ('name', 'gender')
    list_display = ('__str__', 'name', 'gender')


@admin.register(CommitteeMembership)
class CommitteeMembershipAdmin(admin.ModelAdmin):
    """ Admin interface definition for the CommitteeMembership model."""
    model = CommitteeMembership
    search_fields = ('member__first_name', 'member__last_name')
    list_filter = ('member', 'position', 'season')
    list_display = ('__str__', 'member', 'position', 'season')
