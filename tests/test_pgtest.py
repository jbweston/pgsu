"""Test compatibility with pgtest.
"""
from __future__ import absolute_import


def test_pgtest_compatibility():
    """Test using a temporary postgres cluster set up via PGTest.
    """
    from pgtest.pgtest import PGTest
    from pgsu import Postgres, PostgresConnectionMode

    with PGTest() as cluster:
        postgres = Postgres(dbinfo=cluster.dsn)

        # make sure we've connected to the right cluster
        assert cluster.dsn['port'] == postgres.dbinfo['port']
        # we should be connecting via psycopg
        assert postgres.connection_mode == PostgresConnectionMode.PSYCOPG
