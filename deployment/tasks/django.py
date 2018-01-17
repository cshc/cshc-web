
from invoke import task
from os import path
from .common import venv_activate


def django_dir(cnx):
    return path.join(cnx.config.local_root, 'src')


@task
def migrate(cnx):
    """ Calls the migrate Django admin task """
    data = {
        'venv': venv_activate(cnx),
        'django_dir': django_dir(cnx),
    }
    cnx.local(
        '{venv} && cd {django_dir} && python manage.py migrate'.format(**data))
