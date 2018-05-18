"""
  URL endpoints for Training Sessions
"""
from django.conf.urls import url

from . import views, feeds

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

    # E.g. '/training/add/'                 - Form for adding new training sessions
    url(r'^add/$',
        views.TrainingSessionFormView.as_view(),
        name="trainingsession_create"
        ),

    # E.g. '/training/cshc_training.ics'    - Automatically generated ical calendar feed of training sessions
    url(r'^cshc_training.ics$',
        feeds.TrainingSessionICalFeed(),
        name="trainingsession_ical_feed"
        ),
]
