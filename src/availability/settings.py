""" Settings for the Availability app """

from django.conf import settings

AVAILABILITY_ENABLED = getattr(settings, 'AVAILABILITY_ENABLED', False)
""" Set to True to enable Availability Functionality """
