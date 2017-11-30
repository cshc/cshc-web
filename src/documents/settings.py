""" Settings for the Documents app """

from django.conf import settings

DOCUMENTS_DIR = getattr(settings, 'DOCUMENTS_DIR', 'uploads/documents')
""" The directory where uploaded documents should be stored (within MEDIA_URL) """
