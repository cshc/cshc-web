# -*- mode: python; coding: utf-8; -*-
"""Logging handlers."""

from django.http import UnreadablePostError
from django.utils.log import AdminEmailHandler


class FilteredAdminEmailHandler(AdminEmailHandler):
    """Filter log records prior to sending emails.

    The default `AdminEmailHandler` sends emails that we don't really
    care about, e.g. stalled connections can elicit many
    `UnreadablePostError` emails.

    `FilteredAdminEmailHandler` is a small adaptor class that adds
    filtering to the log stream.  It should be attached to
    `django.request` with `propagate` set to `False`.

    """

    def emit(self, record):
        # filter -- ignore UnreadablePostError exceptions
        if (
                record.exc_info is not None and
                record.exc_info[0] is UnreadablePostError
        ):
            return

        # pass to super class
        super().emit(record)
