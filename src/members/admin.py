""" Configuration of Members models for the admin interface.
"""

from django.contrib import admin
from image_cropping import ImageCroppingMixin
from members.models import Member


@admin.register(Member)
class MemberAdmin(ImageCroppingMixin, admin.ModelAdmin):
    """ Admin interface definition for the Member model."""
    model = Member
    # inlines = (SquadMembershipInline,)
    search_fields = ('first_name', 'last_name')
    list_filter = ('is_current', 'gender', 'pref_position')
    list_display = ('__str__', 'user', 'gender',
                    'pref_position', 'is_current')
