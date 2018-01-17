import os
from invoke import Collection

from tasks import database, django, common

ns = Collection(database, django, common)
ns.configure({
    'user': os.environ['MYTHIC_BEASTS_SSH_USER'],
    'connect_kwargs': {
        'password': os.environ['MYTHIC_BEASTS_SSH_PASSWORD'],
    },
})
