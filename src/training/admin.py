""" Configuration of training models for the Django admin interface.
"""

from django.contrib import admin
from .models import TrainingSession


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    """Admin interface for a training session"""
    search_fields = ('venue__name', 'description')
    list_filter = ('venue',)
    list_display = ('__str__', 'description', 'venue',
                    'datetime', 'duration_mins')
