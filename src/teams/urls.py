"""
  URL endpoints for Teams
"""
from django.conf.urls import url

from . import views

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
]
