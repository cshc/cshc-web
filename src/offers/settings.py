""" Settings for the Offers app """

from django.conf import settings

OFFERS_IMAGE_DIR = getattr(settings, 'OFFERS_IMAGE_DIR', 'uploads/offers')
""" The directory where uploaded member offer images should be stored (within MEDIA_URL) """
