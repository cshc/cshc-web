""" 
Configuration of Availability models for the Django admin interface.
"""
from django.contrib import admin
from .models import MatchAvailability


@admin.register(MatchAvailability)
class MatchAvailabilityAdmin(admin.ModelAdmin):
    """ Admin interface definition for the MatchAvailability model. """
    exclude = ('playing_availability_changed', 'umpiring_availability_changed')
