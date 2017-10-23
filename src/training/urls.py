"""
  URL endpoints for Training Sessions
"""
from django.conf.urls import url

from . import views

#pylint: disable=C0103
urlpatterns = [

    # E.g. '/training/'                     - Lists all upcoming training sessions
    url(r'^$',
        views.UpcomingTrainingSessionsView.as_view(),
        name="upcoming_trainingsession_list"
        ),

    # E.g. '/training/41/'                  - Details of a particular training session
    url(r'^(?P<pk>\d+)/$',
        views.TrainingSessionDetailView.as_view(),
        name="trainingsession_detail"
        ),
]
