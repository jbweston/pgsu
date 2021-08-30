# -*- coding: utf-8 -*-
"""Commandline interface for pgsu

"""
import pprint
import click
from . import PGSU

GET_DBS_COMMAND = 'SELECT datname FROM pg_database'


@click.command()
@click.argument('query', type=str, default=GET_DBS_COMMAND)
def run(query):
    """Execute SQL command as PostrgreSQL superuser."""
    pgsu = PGSU(interactive=True, quiet=False)
    click.echo(f'Executing query: {query}')
    dbs = pgsu.execute(query)
    click.echo(pprint.pformat(dbs))
