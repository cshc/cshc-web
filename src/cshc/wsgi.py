"""
WSGI config for cshc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cshc.settings")

for path in '../env.py', '../../env.py':
    try:
        with open(path) as envpy:
            exec(envpy.read())
    except FileNotFoundError:
        pass

#pylint: disable=C0103
application = Sentry(get_wsgi_application())
