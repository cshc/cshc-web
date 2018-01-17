"""
    Database deployment tasks
"""
import sqlite3
from os import path
from invoke import task
from .common import init_remote

# third_party_tables_to_flush = [
#     'account_emailaddress',
#     'account_emailconfirmation',
#     'socialaccount_socialaccount',
#     'easy_thumbnails_thumbnail',
#     'easy_thumbnails_source',
# ]

extra_tables_to_flush = [
    'zinnia_entry',
]

tables_to_dump = [
    'core_clubinfo',
    'awards_matchaward',
    'awards_endofseasonaward',
    'members_committeeposition',
    'competitions_season',
    'teams_clubteam',
    'venues_venue',
    'auth_group',
    'auth_group_permissions',
    'core_cshcuser',
    'core_cshcuser_groups',
    'core_cshcuser_user_permissions',
    'members_member',
    'competitions_league',
    'competitions_division',
    'competitions_cup',
    'opposition_club',
    'opposition_team',
    'training_trainingsession',
    'members_committeemembership',
    'members_squadmembership',
    'teams_clubteamseasonparticipation',
    'teams_teamcaptaincy',
    'matches_match',
    'matches_appearance',
    'awards_matchawardwinner',
    'awards_endofseasonawardwinner',
    'competitions_divisionresult',
    'opposition_clubstats',
    'matches_goalking',
    'teams_southerner',
    'zinnia_category',
    'zinnia_entry_authors',
    'zinnia_entry_categories',
    'zinnia_entry_related',
    'zinnia_entry_sites',
]


def connect_local(cnx):
    return sqlite3.connect(
        path.join(cnx.config.local_root, 'src', cnx.config.database.local_sqlite_db))


@task
def dump_prod(cnx):
    """ Dump the production database data to a SQL file """
    data = {
        'remote_root': cnx.config.remote_root,
        'flags': '--no-create-db --no-create-info --skip-add-locks --complete-insert --compatible=ansi ',
        'db_host': cnx.config.database.host,
        'db_name': cnx.config.database.name,
        'tables': ' '.join(tables_to_dump),
        'dump_file': '{remote_root}/{database.dump_filename}'.format(**cnx.config),
        'sed_replacement': r"s/\\\'/''/g",
    }
    init_remote(cnx)
    cnx.run(
        'mysqldump {flags} -h {db_host} {db_name} {tables} > {dump_file}'.format(**data))
    cnx.run('sed -i.bak "{sed_replacement}" {dump_file}'.format(**data))


@task
def get_prod_dump(cnx):
    """ Copy the dumped prod database data to the local machine """
    dump_prod(cnx)
    remote_file = '{remote_root}/{database.dump_filename}'.format(**cnx.config)
    local_file = path.join(cnx.config.local_root,
                           cnx.config.database.dump_filename)
    cnx.get(remote_file, local_file)


@task
def flush_local_sqlite_db(cnx):
    """ Flush the local database's table data """
    conn = connect_local(cnx)

    try:
        for table in reversed(extra_tables_to_flush + tables_to_dump):
            conn.execute('DELETE FROM ' + table)
    except Exception as ex:
        print('Failed to truncate table', ex)
    finally:
        conn.commit()
        conn.close()


@task
def import_dumped_data(cnx):
    """ Import the dumped data into the local database """
    flush_local_sqlite_db(cnx)
    local_file = path.join(cnx.config.local_root,
                           cnx.config.database.dump_filename)
    conn = connect_local(cnx)
    with open(local_file, 'r') as sql_file:
        sql = sql_file.read()
        conn.executescript(sql)

@task
def import_prod_data(cnx):
    """ Import prod data """
    get_prod_dump(cnx)
    import_dumped_data(cnx)