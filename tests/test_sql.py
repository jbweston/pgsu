"""Test executing SQL commands.

Test creating/dropping users and databases.
"""
from __future__ import absolute_import
import conftest


def test_create_drop_user(postgres, user):  # pylint: disable=unused-argument
    # create and drop user using fixture
    pass


def test_create_drop_db(postgres, user, database):  # pylint: disable=unused-argument
    # create and drop db (+ user) using fixture
    pass


def test_grant_priv(postgres, user, database):  # pylint: disable=unused-argument

    # grant privileges using fixture
    result = postgres.execute(
        conftest.GRANT_PRIV_COMMAND.format(database, user))
    assert result is None
