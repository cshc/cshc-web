"""
Configuration of Announcement models for the admin interface.
"""

from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """ Admin interface for the Announcement model. """
    list_display = ('title', 'content', 'start_date', 'end_date', 'modified')
    search_fields = ('title', 'content')
