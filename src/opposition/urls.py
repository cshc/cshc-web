""" URL routing related to the opposition.
"""

from django.conf.urls import url
from .views import ClubListView, ClubDetailView


urlpatterns = [

    # E.g. 'opposition/clubs/'                  - List of all oppostion clubs (including statistics)
    url(r'^clubs/$',
        ClubListView.as_view(),
        name="opposition_club_list"
        ),

    # E.g. 'opposition/clubs/cambridge-city/'   - Details of a particular opposition club
    url(r'^clubs/(?P<slug>[-\w]+)/$',
        ClubDetailView.as_view(),
        name="opposition_club_detail"
        ),
]
