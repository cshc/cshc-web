"""
  URL endpoints for Teams
"""
from django.conf.urls import url

from . import views

#pylint: disable=C0103
urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$',
        views.ClubTeamDetailsView.as_view(), name='team_detail'),
]
