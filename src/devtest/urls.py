# -*- mode: python; coding: utf-8; -*-
"""Development and testing URLs."""

from django.conf.urls import url

from . import views


#pylint: disable=C0103
urlpatterns = [
    url(r'^unreadable_post_error$', views.unreadable_post_error),
]
