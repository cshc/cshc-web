
from invoke import task
from os import path


def venv_activate(cnx):
    return path.join(cnx.config.local_root, 'venv', 'Scripts', 'activate.bat')


@task
def init_remote(cnx):
    cnx.run('mkdir -p {remote_root}'.format(**cnx.config))
