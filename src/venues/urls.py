"""
  URL endpoints for Venues
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='venues-index'),
]
