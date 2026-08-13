# -*- mode: python; coding: utf-8; -*-
"""Useful development and testing views."""

from django.http import UnreadablePostError


def unreadable_post_error(request):
    raise UnreadablePostError("simulated unreadable post error")
