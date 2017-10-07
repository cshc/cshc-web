""" Configuration of Award models for the Django admin interface.
"""

from django.contrib import admin
from .models import MatchAward, EndOfSeasonAward, MatchAwardWinner, EndOfSeasonAwardWinner


@admin.register(MatchAward)
class MatchAwardAdmin(admin.ModelAdmin):
    """ Admin interface definition for the MatchAward model. """
    pass


@admin.register(EndOfSeasonAward)
class EndOfSeasonAwardAdmin(admin.ModelAdmin):
    """ Admin interface definition for the EndOfSeasonAward model. """
    pass


@admin.register(MatchAwardWinner)
class MatchAwardWinnerAdmin(admin.ModelAdmin):
    """ Admin interface definition for the MatchAwardWinner model."""
    model = MatchAwardWinner
    search_fields = ('member__first_name', 'member__last_name')
    list_display = ('__str__', 'member', 'awardee', 'award', 'match')
    list_filter = ('award',)


@admin.register(EndOfSeasonAwardWinner)
class EndOfSeasonAwardWinnerAdmin(admin.ModelAdmin):
    """ Admin interface definition for the EndOfSeasonAwardWinner model."""
    model = EndOfSeasonAwardWinner
    search_fields = ('member__first_name', 'member__last_name')
    list_display = ('__str__', 'member', 'awardee', 'award', 'season')
    list_filter = ('award', 'season')
