from .local import *

# ########## Amazon S3 CONFIGURATION

from .common.storage import *

# Need to re-set the CK Editor config after the previous two imports
from .common.ckeditor import get_ckeditor_config
CKEDITOR_CONFIGS = get_ckeditor_config(STATIC_URL)

# collectfast must be installed before 'django.contrib.staticfiles'
# Ref: https://github.com/antonagestam/collectfast
INSTALLED_APPS = ['collectfast'] + INSTALLED_APPS

# ########## END Amazon S3 CONFIGURATION
