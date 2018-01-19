""" Django settings for cshc project - local development environment
"""

from cshc.settings.base import *

DEBUG = True

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# DATABASE CONFIGURATION
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(SITE_ROOT, 'db.sqlite3'),
    }
}
# END DATABASE CONFIGURATION

INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]


MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'cshc.middleware.SQLPrintingMiddleware',
]

# Used by DJANGO_DEBUG_TOOLBAR - DEV ONLY
INTERNAL_IPS = ['127.0.0.1']

DISQUS_WEBSITE_SHORTNAME = 'cshc-local'     # Need to change for prod

# ########## WEBPACK LOADER CONFIGURATION

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': join(ROOT_DIR, 'webpack-stats.json'),
    }
}

CORS_ORIGIN_ALLOW_ALL = True

# ########## END WEBPACK LOADER CONFIGURATION

# ########## Amazon S3 CONFIGURATION

if not DEBUG:
    from .common.storage import *

# ########## END Amazon S3 CONFIGURATION

# Important: This needs to be placed after the storage config so the
# correct value of STATIC_URL is used
from .common.ckeditor import get_ckeditor_config
CKEDITOR_CONFIGS = get_ckeditor_config(STATIC_URL)

if DEBUG:
    THUMBNAIL_DEBUG = True