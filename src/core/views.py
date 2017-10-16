from django.shortcuts import render
from competitions.models import Season


def valid_kwarg(key, **dict):
    """ Given a key and a dictionary, returns True if the given key is in
        the dictionary and its value is not None or an empty string.
    """
    return key in dict and dict[key] is not None and dict[key] != ""


def kwargs_or_none(key, **dict):
    """ Given a key and a dictionary, returns the key's value, or None
        if the key is not valid.
    """
    if valid_kwarg(key, **dict):
        return dict[key]
    else:
        return None


def add_season_selector(context, season, season_list):
    """ Adds season information to the given context, facilitating
        the use of the core/_season_selector.html template.

        Returns the updated context.
    """
    context['season'] = season
    context['season_list'] = season_list
    context['is_current_season'] = Season.is_current_season(season.id)
    return context
