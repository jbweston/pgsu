"""Test executing SQL commands.

Test creating/dropping users and databases.
"""
from __future__ import absolute_import
import conftest
import psycopg2

#def test_execute_psql(pgsu):  # pylint: disable=unused-argument
#    """Execute command using PSQL."""
#    from pgsu import PostgresConnectionMode
#    pgsu.connection_mode = PostgresConnectionMode.PSQL
#    pgsu.execute('BAD CMD')


def test_create_drop_user(pgsu, user):  # pylint: disable=unused-argument
    """Create and drop user using fixture."""


def test_create_drop_db(pgsu, user, database):  # pylint: disable=unused-argument
    """Create and drop database + user using fixture."""


def test_grant_priv(pgsu, user, database):  # pylint: disable=unused-argument
    """Create new user + database and connect as that user."""

    # grant privileges
    pgsu.execute(conftest.GRANT_PRIV_COMMAND.format(database, user))

    # connect as new user
    dsn = {
        'host': pgsu.dsn['host'] or 'localhost',
        'port': pgsu.dsn['port'],
        'user': user,
        'password': conftest.DEFAULT_PASSWORD,
        'database': database,
    }
    conn = psycopg2.connect(**dsn)
    conn.close()
