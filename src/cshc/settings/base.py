import os
from os.path import abspath, dirname, join, normpath
from easy_thumbnails.conf import Settings as thumbnail_settings

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)


# ########## PATH CONFIGURATION
# 'src' folder
SITE_ROOT = dirname(dirname(dirname(abspath(__file__))))

# Repo root
ROOT_DIR = dirname(SITE_ROOT)

SITE_NAME = 'CSHC'

FIXTURE_DIRS = join(SITE_ROOT, 'fixtures')

# ########## END PATH CONFIGURATION

# ########## MANAGER CONFIGURATION

ADMINS = (
    ('Graham McCulloch', 'website@cambridgesouthhockeyclub.co.uk'),
)

MANAGERS = ADMINS

SERVER_EMAIL = 'website@cambridgesouthhockeyclub.co.uk'
DEFAULT_FROM_EMAIL = 'website@cambridgesouthhockeyclub.co.uk'

# ########## END MANAGER CONFIGURATION

# ########## AUTHENTICATION CONFIGURATION
AUTH_USER_MODEL = 'core.CshcUser'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_setting('CSHC_SECRET_KEY')

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Django-AllAuth
# Ref: http://django-allauth.readthedocs.io/en/latest
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_SIGNUP_FORM_CLASS = 'core.forms.SignupForm'

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'js_sdk',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.10',
    },
    'linkedin': {
        'SCOPE': [
            'r_emailaddress',
        ],
        'PROFILE_FIELDS': [
            'id',
            'first-name',
            'last-name',
            'email-address',
            'picture-url',
            'public-profile-url',
        ]
    }
}

# ########## END AUTHENTICATION CONFIGURATION

# ########## GENERAL CONFIGURATION

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
SESSION_COOKIE_AGE = 30 * 24 * 60 * 60   # 30 days in seconds
ROOT_URLCONF = 'cshc.urls'
SITE_ID = 1
WSGI_APPLICATION = 'cshc.wsgi.application'

# ########## END GENERAL CONFIGURATION

# ########## VERSION CONFIGURATION

VERSION_FILE = normpath(join(ROOT_DIR, 'version.txt'))
VERSION = open(VERSION_FILE).read().lstrip('v').rstrip()

# ########## END VERSION CONFIGURATION

# ########## APPLICATION DEFINITION
DJANGO_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django_comments',
]

THIRD_PARTY_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'ckeditor',
    'ckeditor_uploader',
    'dbbackup',
    'disqus',
    'django_bootstrap_breadcrumbs',
    'django_filters',
    'django_user_agents',
    'easy_thumbnails',
    'geoposition',
    'graphene_django',
    'image_cropping',
    'mptt',
    's3_folder_storage',
    'tagging',
    'taggit',
    'raven.contrib.django.raven_compat',
    'webpack_loader',
    'zinnia',
]

LOCAL_APPS = [
    'core.apps.CoreConfig',
    'venues.apps.VenuesConfig',
    'competitions.apps.CompetitionsConfig',
    'opposition.apps.OppositionConfig',
    'teams.apps.TeamsConfig',
    'members.apps.MembersConfig',
    'training.apps.TrainingConfig',
    'matches.apps.MatchesConfig',
    'awards.apps.AwardsConfig',
    'documents.apps.DocumentsConfig',
    'offers.apps.OffersConfig',
    'unify.apps.UnifyConfig',
]

# Note: LOCAL_APPS should be added before THIRD_PARTY_APPS as
#       zinnia looks for AUTH_USER_MODEL when loaded
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

# ########## END APPLICATION DEFINITION

# ########## MIDDLEWARE CONFIGURATION

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

# ########## END MIDDLEWARE CONFIGURATION

# ########## TEMPLATE CONFIGURATION

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [join(SITE_ROOT, 'cshc', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                'cshc.context_processors.utils',
            ],
        },
    },
]

# ########## END TEMPLATE CONFIGURATION

# ########## MEDIA CONFIGURATION

MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))
MEDIA_URL = '/media/'

# ########## END MEDIA CONFIGURATION

# ########## STATIC FILE CONFIGURATION

STATIC_ROOT = join(SITE_ROOT, 'assets')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # We do this so that django's collectstatic copies our bundles to the
    # STATIC_ROOT or syncs them to whatever storage we use.
    # join(SITE_ROOT, 'frontend'),
    join(SITE_ROOT, 'static'),
)

# ########## END STATIC FILE CONFIGURATION

# ########## LOGGING CONFIGURATION

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            # To capture more than ERROR, change to WARNING, INFO, etc.
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# ########## END LOGGING CONFIGURATION

# ########## django-user-agents CONFIGURATION

# https://github.com/selwin/django-user_agents

# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = 'default'

# ########## END django-user-agents CONFIGURATION

# ########## django-geoposition / GOOGLE MAPS CONFIGURATION

GMAPS_API_KEY = get_env_setting('GMAPS_API_KEY')
GEOPOSITION_GOOGLE_MAPS_API_KEY = GMAPS_API_KEY
GEOPOSITION_MAP_OPTIONS = {
    'minZoom': 3,
    'maxZoom': 15,
    'scrollwheel': True,
    'lat': 52.206133926014665,      # Cambridge
    'lng': 0.12531280517578125,
}

# ########## END django-geoposition / GOOGLE MAPS CONFIGURATION

# ########## django-bootstrap-breadcrumbs CONFIGURATION

# Ref: http://django-bootstrap-breadcrumbs.readthedocs.io/en/latest/
BREADCRUMBS_TEMPLATE = "core/_breadcrumbs.html"

# ########## END django-bootstrap-breadcrumbs CONFIGURATION

# ########## django-image-cropping CONFIGURATION

# Ref: https://github.com/jonasundderwolf/django-image-cropping
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS
IMAGE_CROPPING_BACKEND = 'core.backends.image_backend.ResizedImageEasyThumbnailsBackend'

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True},
        'member-link': {'size': (30, 30), 'crop': True},
        'squad-list': {'size': (255, 255), 'crop': True},
        'news-list': {'size': (350, 233), 'crop': True},
        'member_detail': {'size': (255, 255), 'crop': True},
    },
}

IMAGE_CROPPING_JQUERY_URL = "None"

# ########## END django-image-cropping CONFIGURATION

# ########## django-ckeditor CONFIGURATION

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_FILENAME_GENERATOR = 'core.models.make_unique_filename'

# Note: Additional CKEDITOR config specified after STATIC_URL is set

# ########## END django-ckeditor CONFIGURATION

# ########## graphene CONFIGURATION

GRAPHENE = {
    'SCHEMA': 'cshc.schema.schema',  # Where your Graphene schema lives
    'SCHEMA_INDENT': 2,
    'MIDDLEWARE': [
        'graphene_django.debug.DjangoDebugMiddleware',
    ]
}

# ########## END graphene CONFIGURATION

# ########## django-templated-email CONFIGURATION

# Ref: https://github.com/vintasoftware/django-templated-email
TEMPLATED_EMAIL_TEMPLATE_DIR = 'emails/'
TEMPLATED_EMAIL_FILE_EXTENSION = 'html'

# ########## END django-templated-email CONFIGURATION

# ########## raven CONFIGURATION

# Ref: https://sentry.io/onboarding/cambridge-south-hockey-club/cshc-django/configure/python-django
RAVEN_CONFIG = {
    'dsn': get_env_setting('SENTRY_DNS'),
    'release': VERSION,
}

# ########## END raven CONFIGURATION

# ########## django-disqus CONFIGURATION

# Ref: https://django-disqus.readthedocs.io/en/latest

DISQUS_API_KEY = get_env_setting('DISQUS_API_KEY')

# ########## END django-disqus CONFIGURATION

# ########## Zinnia CONFIGURATION

# Ref: http://docs.django-blog-zinnia.com/en/latest/getting-started/configuration.html
ZINNIA_PING_EXTERNAL_URLS = False
ZINNIA_SAVE_PING_DIRECTORIES = False
# disable comments, pingbacks and trackbacks completely (we'll use disqus)
ZINNIA_AUTO_CLOSE_COMMENTS_AFTER = 0
ZINNIA_AUTO_CLOSE_PINGBACKS_AFTER = 0
ZINNIA_AUTO_CLOSE_TRACKBACKS_AFTER = 0

# ########## END Zinnia CONFIGURATION


# ########## MODEL-UTILS CONFIGURATION

# See: https://github.com/carljm/django-model-utils
SPLIT_MARKER = '<!-- split -->'
SPLIT_DEFAULT_PARAGRAPHS = 1

# ########## END MODEL-UTILS CONFIGURATION


# ########## django-dbbackup CONFIGURATION

# Ref: https://github.com/django-dbbackup/django-dbbackup
DBBACKUP_STORAGE = 'dbbackup.storage.s3_storage'
DBBACKUP_S3_BUCKET = get_env_setting('AWS_STORAGE_BUCKET_NAME')
DBBACKUP_S3_ACCESS_KEY = get_env_setting('AWS_ACCESS_KEY_ID')
DBBACKUP_S3_SECRET_KEY = get_env_setting('AWS_SECRET_ACCESS_KEY')
DBBACKUP_S3_DIRECTORY = 'django-dbbackups/'

# ########## END django-dbbackup CONFIGURATION
