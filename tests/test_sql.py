"""Test executing SQL commands.

Test creating/dropping users and databases.
"""
from __future__ import absolute_import
import conftest

#def test_execute_psql(postgres):  # pylint: disable=unused-argument
#    """Execute command using PSQL."""
#    from pgsu import PGSUConnectionMode
#    postgres.connection_mode = PGSUConnectionMode.PSQL
#    postgres.execute('BAD CMD')


def test_create_drop_user(postgres, user):  # pylint: disable=unused-argument
    """Create and drop user using fixture."""


def test_create_drop_db(postgres, user, database):  # pylint: disable=unused-argument
    """Create and drop database + user using fixture."""


def test_grant_priv(postgres, user, database):  # pylint: disable=unused-argument
    """Create new user + database and connect as that user."""
    import psycopg2

    # grant privileges
    postgres.execute(conftest.GRANT_PRIV_COMMAND.format(database, user))

    # connect as new user
    dbinfo = {
        'host': postgres.dbinfo['host'] or 'localhost',
        'port': postgres.dbinfo['port'],
        'user': user,
        'password': conftest.DEFAULT_PASSWORD,
        'database': database,
    }
    conn = psycopg2.connect(**dbinfo)
    conn.close()
