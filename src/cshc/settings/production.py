""" Django settings for cshc project - production environment
"""
import sys
import os
from cshc.settings.base import *

DEBUG = False

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = ['*']

# DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}

# Only specify this option for syncdb or migrate calls (for efficiency)
# Ref: Comment on http://stackoverflow.com/a/5270072
if 'migrate' in sys.argv or 'syncdb' in sys.argv:
    DATABASES['default']['OPTIONS'] = {
        'init_command': 'SET storage_engine=MyISAM', }

# END DATABASE CONFIGURATION

# EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = 'smtp.sendgrid.net'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = get_env_setting('EMAIL_HOST_PASSWORD')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = get_env_setting('EMAIL_HOST_USER')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 587

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# END EMAIL CONFIGURATION

# ########## WEBPACK LOADER CONFIGURATION

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'dist/',
        'STATS_FILE': join(ROOT_DIR, 'webpack-stats-prod.json'),
    }
}

CORS_ORIGIN_ALLOW_ALL = True

# ########## END WEBPACK LOADER CONFIGURATION

# ########## Amazon S3 CONFIGURATION

from .common.storage import *

# ########## END Amazon S3 CONFIGURATION

# Important: This needs to be placed after the storage config so the
# correct value of STATIC_URL is used
from .common.ckeditor import get_ckeditor_config
CKEDITOR_CONFIGS = get_ckeditor_config(STATIC_URL)
