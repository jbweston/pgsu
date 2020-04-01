from __future__ import absolute_import
import sys
import pytest
from pgsu import PGSU
from contextlib import contextmanager
import os
from io import StringIO

CREATE_USER_COMMAND = 'CREATE USER "{}" WITH PASSWORD \'{}\''
DROP_USER_COMMAND = 'DROP USER "{}"'
CREATE_DB_COMMAND = ('CREATE DATABASE "{}" OWNER "{}" ENCODING \'UTF8\' '
                     'LC_COLLATE=\'en_US.UTF-8\' LC_CTYPE=\'en_US.UTF-8\' '
                     'TEMPLATE=template0')
DROP_DB_COMMAND = 'DROP DATABASE "{}"'
GRANT_PRIV_COMMAND = 'GRANT ALL PRIVILEGES ON DATABASE "{}" TO "{}"'
GET_USERS_COMMAND = "SELECT usename FROM pg_user WHERE usename='{}'"
GET_DBS_COMMAND = "SELECT datname FROM pg_database WHERE datname='{}'"
COPY_DB_COMMAND = 'CREATE DATABASE "{}" WITH TEMPLATE "{}" OWNER "{}"'

DEFAULT_USER = 'newuser'
DEFAULT_PASSWORD = 'newpassword'  # noqa
DEFAULT_DB = 'newdb'


@contextmanager
def enter_password():
    """Replace standard input with password.

    See https://stackoverflow.com/a/36491341/1069467
    """
    pgsu_pw = os.getenv("PGSU_TEST_PASSWORD")
    if not pgsu_pw:
        yield
    else:
        orig = sys.stdin
        sys.stdin = StringIO(pgsu_pw + '\n')
        yield
        sys.stdin = orig


@pytest.fixture
def postgres():
    with enter_password():

        dsn = {
            'host': os.getenv('PGSU_TEST_HOST'),
            'port': os.getenv('PGSU_TEST_PORT'),
            'password': os.getenv('PGSU_TEST_PASSWORD'),
            'user': os.getenv('PGSU_TEST_USER'),
            'database': os.getenv('PGSU_TEST_database'),
        }
        return PGSU(dsn={k: v for k, v in dsn.items() if v})


@pytest.fixture
def user(postgres):
    # if user already exists, fail (we don't want to cause trouble)
    assert not postgres.execute(GET_USERS_COMMAND.format(DEFAULT_USER))

    postgres.execute(CREATE_USER_COMMAND.format(DEFAULT_USER,
                                                DEFAULT_PASSWORD))
    yield DEFAULT_USER
    postgres.execute(DROP_USER_COMMAND.format(DEFAULT_USER))


@pytest.fixture
def database(postgres, user):
    # if database already exists, fail (we don't want to cause trouble)
    assert not postgres.execute(GET_DBS_COMMAND.format(DEFAULT_DB))

    postgres.execute(CREATE_DB_COMMAND.format(DEFAULT_DB, user))
    yield DEFAULT_DB
    postgres.execute(DROP_DB_COMMAND.format(DEFAULT_DB))
