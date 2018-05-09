"""
  URL endpoints for Match Availabilities
"""
from django.conf.urls import url

from . import views

#pylint: disable=C0103
urlpatterns = [

    # E.g. '/availability/playing/m1/'                    - Manage playing availabilities for a particular team
    url(r'^playing/(?P<slug>[-\w]+)/$',
        views.ManageTeamPlayingAvailabilityView.as_view(),
        name="manage_team_playing_availability"
        ),

    # E.g. '/availability/umpiring/'                    - Manage umpiring availabilities for all teams
    url(r'^umpiring/$',
        views.ManageUmpiringAvailabilityView.as_view(),
        name="manage_umpiring_availability"
        ),
]
