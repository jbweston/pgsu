# -*- coding: utf-8 -*-
"""Test executing SQL commands.

Test creating/dropping users and databases.
"""
import os
import sys
from contextlib import contextmanager
from io import StringIO
import psycopg2

from pgsu import PGSU, DEFAULT_DSN
import conftest


def test_create_drop_user(user):  # pylint: disable=unused-argument
    """Create and drop user using fixture."""


def test_create_drop_db(user, database):  # pylint: disable=unused-argument
    """Create and drop database + user using fixture."""


def test_grant_priv(pgsu, user, database):  # pylint: disable=unused-argument
    """Create new user + database and connect as that user."""

    # grant privileges
    pgsu.execute(conftest.GRANT_PRIV_COMMAND.format(database, user))

    # connect as new user
    dsn = {
        'host': pgsu.dsn.get('host') or 'localhost',
        'port': pgsu.dsn.get('port'),
        'user': user,
        'password': conftest.DEFAULT_PASSWORD,
        'database': database,
    }
    conn = psycopg2.connect(**dsn)
    conn.close()


@contextmanager
def input_dsn(dsn):
    """Enter PostgreSQL connection details via terminal.

    See https://stackoverflow.com/a/36491341/1069467
    """
    inputs = []
    for key in ['host', 'port', 'user', 'database', 'password']:
        inputs.append(str(dsn.get(key, '')))

    input_str = str(os.linesep.join(inputs) + os.linesep)
    orig = sys.stdin
    sys.stdin = StringIO(input_str)
    yield
    sys.stdin = orig


def test_interactive(dsn_from_env):
    """Test that connection details can be provided via prompt."""
    dsn_from_env['port'] = DEFAULT_DSN['port']
    with input_dsn(dsn_from_env):
        PGSU(dsn={'port': 1234}, interactive=True,
             quiet=False)  # provide wrong port
        assert PGSU.is_connected
