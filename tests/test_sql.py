"""Test executing SQL commands.

Test creating/dropping users and databases.
"""
import conftest

def test_create_drop_user(postgres, user):
    # create and drop user using fixture
    pass

def test_create_drop_db(postgres, user, database):
    # create and drop db (+ user) using fixture
    pass

def test_grant_priv(postgres, user, database):
    # grant privileges using fixture
    result = postgres.execute(conftest.GRANT_PRIV_COMMAND.format(database, user))
    assert result is None
