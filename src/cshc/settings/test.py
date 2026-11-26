""" Settings for running the test suite.

    Builds the test database directly from the models instead of running the
    migrations. Some old data migrations (e.g. teams/0009_modify_values) assume
    the production data already exists and fail on an empty test database.

    Usage: python manage.py test --settings=cshc.settings.test
"""

import copy

from .local import *  # noqa: F401,F403
from .local import LOGGING


class DisableMigrations:
    """ Tells Django that no app has migrations, so tables are created from the models. """

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# Pages use {% thumbnail %} on absolute URLs (http://testserver/static/...). sorl
# tries to download them, fails (there is no such server), logs the error with a
# traceback and renders without the image. That's harmless in tests, so hide it.
LOGGING = copy.deepcopy(LOGGING)
LOGGING['loggers']['sorl.thumbnail']['level'] = 'CRITICAL'
