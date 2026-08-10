# -*- mode: python; coding: utf-8; -*-
"""Development and testing URLs."""

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt


from . import views


#pylint: disable=C0103
urlpatterns = [
    url(r'^unreadable_post_error$', csrf_exempt(views.unreadable_post_error)),
]
