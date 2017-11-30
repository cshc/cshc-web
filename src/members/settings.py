""" Settings for the Members app """

from django.conf import settings

MEMBERS_PHOTO_DIR = getattr(
    settings, 'MEMBERS_PHOTO_DIR', 'uploads/profile_pics')
""" The directory where uploaded profile pictures should be stored (within MEDIA_URL) """
