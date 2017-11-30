"""
Configuration of MemberOffer models for the admin interface.
"""

from django.contrib import admin
from .models import MemberOffer


@admin.register(MemberOffer)
class MemberOfferAdmin(admin.ModelAdmin):
    """ Admin interface for the MemberOffer model. """
    list_display = ('title', 'url', 'image', 'expiry', 'modified')
    search_fields = ('title', )
