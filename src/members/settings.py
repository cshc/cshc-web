""" Settings for the Members app """

from django.conf import settings

MEMBERS_PHOTO_DIR = getattr(
    settings, 'MEMBERS_PHOTO_DIR', 'uploads/profile_pics')
""" The directory where uploaded profile pictures should be stored (within MEDIA_URL) """

MEMBERS_SHIRT_NUMBER_MAX = getattr(
    settings, 'MEMBERS_SHIRT_NUMBER_MAX', 299)
""" The maximum permitted shirt number """

MEMBERS_SHIRT_NUMBER_LIMIT = getattr(
    settings, 'MEMBERS_SHIRT_NUMBER_LIMIT', 24)
""" The number of available shirt numbers to return """

MEMBERS_SHIRT_NUMBER_INCLUDE_NOT_CURRENT = getattr(
    settings, 'MEMBERS_SHIRT_NUMBER_INCLUDE_NOT_CURRENT', True)
""" Whether to include non-current members when looking for available shirt numbers """

MEMBERS_SHIRT_NUMBER_GRACE_PERIOD = getattr(
    settings, 'MEMBERS_SHIRT_NUMBER_GRACE_PERIOD', 2)
""" Number of seasons after which non-current members' assigned shirt numbers are considered for reuse """
