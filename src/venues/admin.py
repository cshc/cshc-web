"""
Django Admin configuration for Venues
"""
from django.contrib import admin
from venues.models import Venue


class VenueAdmin(admin.ModelAdmin):
    """
    ModelAdmin for the Venue model 
    """
    readonly_fields = ('slug',)
    search_fields = ('name',)
    list_filter = ('is_home',)
    list_display = ('name', 'short_name',
                    'approx_round_trip_distance', 'url', 'is_home')


admin.site.register(Venue, VenueAdmin)
