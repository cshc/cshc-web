""" Settings for the Teams app """

from django.conf import settings

TEAMS_PHOTO_DIR = getattr(settings, 'TEAMS_PHOTO_DIR', 'uploads/team_photos')
""" The directory where uploaded team photos should be stored (within MEDIA_URL) """
