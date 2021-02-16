# -*- coding: utf-8 -*-
"""Test compatibility with pgtest.
"""
from pgtest.pgtest import PGTest, which
import pytest
from pgsu import PGSU, PostgresConnectionMode

try:
    PG_CTL = which('pg_ctl')
except FileNotFoundError:
    PG_CTL = None


@pytest.mark.skipif(not PG_CTL, reason='pg_ctl not found in PATH')
def test_pgtest_compatibility():
    """Test using a temporary postgres cluster set up via PGTest.
    """

    with PGTest() as cluster:
        pgsu = PGSU(dsn=cluster.dsn)

        # make sure we've connected to the right cluster
        assert cluster.dsn['port'] == pgsu.dsn['port']
        # we should be connecting via psycopg
        assert pgsu.connection_mode == PostgresConnectionMode.PSYCOPG
