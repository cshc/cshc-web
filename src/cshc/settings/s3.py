from .local import *

# ########## Amazon S3 CONFIGURATION

from .common.storage import *

# collectfast must be installed before 'django.contrib.staticfiles'
# Ref: https://github.com/antonagestam/collectfast
INSTALLED_APPS = ['collectfast'] + INSTALLED_APPS

# ########## END Amazon S3 CONFIGURATION
