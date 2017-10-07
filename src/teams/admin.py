""" 
Configuration of Teams models for the admin interface.
"""

from django.contrib import admin
from teams.models import ClubTeam


@admin.register(ClubTeam)
class ClubTeamAdmin(admin.ModelAdmin):
    """ Admin interface for the ClubTeam model. """
    readonly_fields = ('slug',)
    # inlines = (TeamCaptaincyInline, )
    list_display = ('short_name', 'long_name', 'slug', 'active', 'southerners',
                    'rivals', 'fill_blanks', 'personal_stats')
