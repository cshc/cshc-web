"""
  URL endpoints for Teams
"""
from django.conf.urls import url

from . import views, feeds

#pylint: disable=C0103
urlpatterns = [
    url(r'^$', views.ClubTeamListView.as_view(), name='clubteam_list'),
    url(r'^(?P<slug>[-\w]+)/$',
        views.ClubTeamDetailView.as_view(), name='clubteam_detail'),

    # E.g. '/teams/m1/2011-2012/'
    # Details of a particular CSHC team (including the team's playing record) for a previous season
    url(r'^(?P<slug>[-\w]+)/(?P<season_slug>[-\w]+)/$',
        views.ClubTeamDetailView.as_view(),
        name="clubteam_season_detail"
        ),

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
