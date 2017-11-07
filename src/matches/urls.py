""" URL routing for views relating to matches.

    This includes all the RSS and ical feeds.
"""

from django.conf.urls import url
from . import views, feeds

urlpatterns = [

    # E.g. '/matches/'                      - Searchable/filterable list of all matches
    url(r'^$',
        views.MatchListView.as_view(),
        name="match_list"
        ),

    # E.g. '/matches/23/'                   - Details of a specific match
    url(r'^(?P<pk>\d+)/$',
        views.MatchDetailView.as_view(),
        name="match_detail"
        ),

    # # E.g. '/matches/23-Apr-13/'            - List of matches on a particular date
    # url(r'^(?P<date>\d{2}-[a-zA-Z]{3}-\d{2})/$',
    #     views.MatchesByDateView.as_view(),
    #     name="matches_by_date"
    # ),

    # # E.g. '/matches/by-season/'            - Calendar view of matches in the current season
    # url(r'^by-season/$',
    #     views.MatchesBySeasonView.as_view(),
    #     name="matches_by_season_default"
    # ),

    # # E.g. '/matches/by-season/2011-2012/'  - Calendar view of matches in a previous season
    # url(r'^by-season/(?P<season_slug>[-\w]+)/$',
    #     views.MatchesBySeasonView.as_view(),
    #     name="matches_by_season"
    # ),

    # E.g. '/matches/goal-king/'            - Goal King table
    url(r'^goal-king/$',
        views.GoalKingView.as_view(),
        name="goal_king"
        ),

    # E.g. '/matches/accidental-tourist/'   - Accidental Tourist table for the current season
    url(r'^accidental-tourist/$',
        views.AccidentalTouristSeasonView.as_view(),
        name="accidental_tourist"
        ),

    # E.g. '/matches/accidental-tourist/2011-2012/'     - Accidental Tourist table for previous seasons
    url(r'^accidental-tourist/(?P<season_slug>[-\w]+)/$',
        views.AccidentalTouristSeasonView.as_view(),
        name="accidental_tourist_season"
        ),

    # # E.g. '/matches/accidental-tourist/2011-2012/ajax/'    - AJAX-only: Updates and refreshes Accidental Tourist stats
    # url(r'^accidental-tourist/(?P<season_slug>[-\w]+)/ajax/$',
    #     views.AccidentalTouristSeasonUpdateView.as_view(),
    #     name="accidental_tourist_season_update"
    # ),

    # E.g. '/matches/naughty-step/'         - Statistics on the number of cards (red/yellow/green) received by members
    url(r'^naughty-step/$',
        views.NaughtyStepSeasonView.as_view(),
        name="naughty_step"
        ),

    # E.g. '/matches/naughty-step/2011-2012/'     - Statistics on the number of cards (red/yellow/green) received by members for particular seasons
    url(r'^naughty-step/(?P<season_slug>[-\w]+)/$',
        views.NaughtyStepSeasonView.as_view(),
        name="naughty_step_season"
        ),

    # Feeds
    url(r'^feed/rss/$',                          # RSS feed of match reports
        feeds.RssMatchReportsFeed(),
        name="match_report_rss_feed"
        ),
    url(r'feed/atom/$',                         # Atom feed of match reports
        feeds.AtomMatchReportsFeed(),
        name="match_report_atom_feed"
        ),
    # E.g. '/matches/cshc_matches.ics'
    url(r'^cshc_matches.ics$',                  # Calendar feed of this season's matches
        feeds.MatchICalFeed(),
        name="match_ical_feed"
        ),
]
