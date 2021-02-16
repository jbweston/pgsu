# -*- coding: utf-8 -*-
"""Test command line interface.

"""
import getpass
from click.testing import CliRunner
from pgsu.cli import run


def test_plain(pgsu):  # pylint: disable=unused-argument
    """Run cli without parameters.

    Check that 'template1' standard DB is found in the output.
    """
    result = CliRunner().invoke(run)
    assert 'template1' in result.output


def test_users(pgsu):  # pylint: disable=unused-argument
    """Ask for database users."""
    result = CliRunner().invoke(run, ['SELECT usename FROM pg_user'])

    specified_user = pgsu.dsn.get('user')
    if specified_user:
        assert specified_user in result.output, result.output
    else:
        # If the user is None, it means the connection worked without specifying the user.
        # In practice, it then the PostgreSQL superuser is either 'postgres' or the current UNIX user
        assert ('postgres'
                in result.output) or (getpass.getuser()
                                      in result.output), result.output
