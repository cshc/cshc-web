"""
  URL endpoints for Venues
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.VenueListView.as_view(), name='venue-list'),
    url(r'^(?P<slug>[-\w]+)/$',
        views.VenueDetailsView.as_view(), name='venue-details'),
]
