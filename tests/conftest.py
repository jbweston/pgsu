from __future__ import absolute_import
import pytest
from pgsu import PGSU
import os
import platform

if platform.system() == 'Windows':
    locale = 'en-US'
else:
    locale = 'en_US.UTF-8'

USER_EXISTS_COMMAND = "SELECT usename FROM pg_user WHERE usename='{}'"
CREATE_USER_COMMAND = """CREATE USER "{}" WITH PASSWORD '{}'"""
DROP_USER_COMMAND = 'DROP USER "{}"'

DB_EXISTS_COMMAND = "SELECT datname FROM pg_database WHERE datname='{}'"
CREATE_DB_COMMAND = \
"""CREATE DATABASE "{{}}" OWNER "{{}}" ENCODING 'UTF8' LC_COLLATE='{loc}' LC_CTYPE='{loc}' TEMPLATE=template0"""\
    .format(loc=locale)
DROP_DB_COMMAND = 'DROP DATABASE "{}"'
COPY_DB_COMMAND = 'CREATE DATABASE "{}" WITH TEMPLATE "{}" OWNER "{}"'

GRANT_PRIV_COMMAND = 'GRANT ALL PRIVILEGES ON DATABASE "{}" TO "{}"'

DEFAULT_USER = 'newuser'
DEFAULT_PASSWORD = 'newpassword'  # noqa
DEFAULT_DB = 'newdb'


@pytest.fixture()
def dsn_from_env():
    """Read DSN from test environment variables.

    For testing postgresql configurations with passwords / nonstandard ports, you can set the environment variables:
      * PGSU_TEST_HOST
      * PGSU_TEST_PORT
      * PGSU_TEST_PASSWORD
      * PGSU_TEST_USER
      * PGSU_TEST_database

    :returns:  Dictionary with (only) the DSN keys provided via environment variables.
    """
    dsn = {
        'host': os.getenv('PGSU_TEST_HOST'),
        'port': os.getenv('PGSU_TEST_PORT'),
        'password': os.getenv('PGSU_TEST_PASSWORD'),
        'user': os.getenv('PGSU_TEST_USER'),
        'database': os.getenv('PGSU_TEST_DATABASE'),
    }
    return {k: v for k, v in dsn.items() if v}


@pytest.fixture
def pgsu(dsn_from_env):
    """Return configured PGSU instance.

    """
    return PGSU(dsn=dsn_from_env)


@pytest.fixture
def user(pgsu):
    """Create a new user in the DB cluster.

    User is deleted again after tests finish.
    """
    # if user already exists, fail (we don't want to cause trouble)
    assert not pgsu.execute(USER_EXISTS_COMMAND.format(DEFAULT_USER))

    pgsu.execute(CREATE_USER_COMMAND.format(DEFAULT_USER, DEFAULT_PASSWORD))
    yield DEFAULT_USER
    pgsu.execute(DROP_USER_COMMAND.format(DEFAULT_USER))


@pytest.fixture
def database(pgsu, user):
    """Create test database.

    The test DB is deleted again after tests finish.
    """
    # if database already exists, fail (we don't want to cause trouble)
    assert not pgsu.execute(DB_EXISTS_COMMAND.format(DEFAULT_DB))

    pgsu.execute(CREATE_DB_COMMAND.format(DEFAULT_DB, user))
    yield DEFAULT_DB
    pgsu.execute(DROP_DB_COMMAND.format(DEFAULT_DB))
