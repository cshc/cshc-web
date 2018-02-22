"""
  URL endpoints for Award Winners
"""
from django.conf.urls import url

from . import views

#pylint: disable=C0103
urlpatterns = [

    # E.g. '/awards/end-of-season'                    - Lists all end of season award winners
    url(r'^end-of-season/$',
        views.EndOfSeasonAwardWinnersView.as_view(),
        name="end_of_season_award_winners_list"
        ),
]
