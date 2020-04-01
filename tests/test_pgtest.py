"""Test compatibility with pgtest.
"""
from __future__ import absolute_import
from pgtest.pgtest import PGTest, which
from pgsu import PGSU, PostgresConnectionMode
import pytest

try:
    pg_ctl = which('pg_ctl')
except FileNotFoundError:
    pg_ctl = None


@pytest.mark.skipif(not pg_ctl, reason="pg_ctl not found in PATH")
def test_pgtest_compatibility():
    """Test using a temporary postgres cluster set up via PGTest.
    """

    with PGTest() as cluster:
        postgres = PGSU(dsn=cluster.dsn)

        # make sure we've connected to the right cluster
        assert cluster.dsn['port'] == postgres.dsn['port']
        # we should be connecting via psycopg
        assert postgres.connection_mode == PostgresConnectionMode.PSYCOPG
