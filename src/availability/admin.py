""" 
Configuration of Availability models for the Django admin interface.
"""
from django.contrib import admin
from django.conf import settings
from .models import MatchAvailability


class MatchAvailabilityAdmin(admin.ModelAdmin):
    """ Admin interface definition for the MatchAvailability model. """
    exclude = ('playing_availability_changed', 'umpiring_availability_changed')


if settings.AVAILABILITY_ENABLED:
    admin.site.register(MatchAvailability, MatchAvailabilityAdmin)
