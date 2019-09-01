import os
from invoke import Collection

from tasks import database, django, common

ns = Collection(database, django, common)
ns.configure({
    'user': os.environ['CSHC_AWS_SSH_USER'],
    'connect_kwargs': {
        'key_filename': os.environment['CSHC_WEB_KEY_PAIR_FILENAME'],
    },
})
