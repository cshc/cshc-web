from os.path import join, normpath
from cshc.settings.base import get_env_setting, SITE_ROOT

# ########## django-s3-folder-storage CONFIGURATION

# Ref: https://github.com/jamstooks/django-s3-folder-storage
# Creds
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = get_env_setting('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_setting('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_setting('AWS_STORAGE_BUCKET_NAME')

# Uploaded Media Folder
# DEFAULT_FILE_STORAGE = 'cshc.util.FixedDefaultStorage'
DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
DEFAULT_S3_PATH = "media"
MEDIA_ROOT = normpath(join(SITE_ROOT, DEFAULT_S3_PATH))
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME

# Static media folder
# STATICFILES_STORAGE = 'cshc.util.FixedStaticStorage'
STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
STATIC_S3_PATH = "static"
STATIC_ROOT = normpath(join(SITE_ROOT, STATIC_S3_PATH))
STATIC_URL = '//%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME

# ########## END django-s3-folder-storage CONFIGURATION
