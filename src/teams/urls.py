"""
  URL endpoints for Teams
"""
from django.conf.urls import url

from . import views, feeds

#pylint: disable=C0103
urlpatterns = [
    url(r'^$', views.ClubTeamListView.as_view(), name='clubteam_list'),

    # E.g. '/teams/southerners/'                - Statistics table comparing the performance of CSHC teams this season
    url(r'^southerners/$',
        views.SouthernersSeasonView.as_view(),
        name="southerners_league"
        ),

    # E.g. '/teams/southerners/2011-2012/'      - Statistics table comparing the performance of CSHC teams in a previous season
    url(r'^southerners/(?P<season_slug>[-\w]+)/$',
        views.SouthernersSeasonView.as_view(),
        name="southerners_league_season"
        ),

    # E.g. '/teams/playing-record/'             - The playing records through the seasons of each team
    url(r'^playing-record/$',
        views.PlayingRecordView.as_view(),
        name="playing_record"
        ),

    url(r'^(?P<slug>[-\w]+)/$',
        views.ClubTeamDetailView.as_view(), name='clubteam_detail'),

    # E.g. '/teams/m1/2011-2012/'
    # Details of a particular CSHC team (including the team's playing record) for a previous season
    url(r'^(?P<slug>[-\w]+)/(?P<season_slug>[-\w]+)/$',
        views.ClubTeamDetailView.as_view(),
        name="clubteam_season_detail"
        ),

    # Feeds
    # E.g. /teams/m1.ics'                       - Calendar feed of a particular team's matches
    url(r'^(?P<slug>[-\w]+).ics$',
        feeds.ClubTeamMatchICalFeed(),
        name="clubteam_ical_feed"
        ),

    # E.g. /teams/m1.rss'                       - RSS feed of a particular team's match reports
    url(r'^(?P<slug>[-\w]+).rss$',
        feeds.RssClubTeamMatchReportsFeed(),
        name="clubteam_match_rss_feed"
        ),
]
