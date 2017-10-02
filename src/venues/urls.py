"""
  URL endpoints for Venues
"""
from django.conf.urls import url

from . import views

#pylint: disable=C0103
urlpatterns = [
    url(r'^$', views.VenueListView.as_view(), name='venue-list'),
    url(r'^(?P<slug>[-\w]+)/$',
        views.VenueDetailsView.as_view(), name='venue-details'),
]
