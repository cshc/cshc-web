""" Settings for the Members app """

from django.conf import settings

MEMBERS_PHOTO_DIR = getattr(
    settings, 'MEMBERS_PHOTO_DIR', 'uploads/profile_pics')
""" The directory where uploaded profile pictures should be stored (within MEDIA_URL) """

MEMBERS_MAX_SHIRT_NUMBER = getattr(
    settings, 'MEMBERS_MAX_SHIRT_NUMBER', 299)
""" The maximum permitted shirt number """

MEMBERS_FREE_SHIRT_NUMBER_LIMIT = getattr(
    settings, 'MEMBERS_FREE_SHIRT_NUMBER_LIMIT', 12)
""" The number of available shirt numbers to return """

MEMBERS_FREE_SHIRT_CURRENT_ONLY = getattr(
    settings, 'MEMBERS_FREE_SHIRT_CURRENT_ONLY', False)
""" Whether to check current playing member shirt numbers only """