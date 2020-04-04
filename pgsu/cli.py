# -*- coding: utf-8 -*-
"""Commandline interface for pgsu

"""
from __future__ import absolute_import
import click
import pprint
from . import PGSU

GET_DBS_COMMAND = "SELECT datname FROM pg_database"


@click.command()
@click.argument('query', type=str, default=GET_DBS_COMMAND)
def run(query):
    """Execute SQL command as PostrgreSQL superuser."""
    click.echo("Trying to connect to PostgreSQL...")
    pgsu = PGSU()
    click.echo("Executing query: {}".format(query))
    dbs = pgsu.execute(query)
    click.echo(pprint.pformat(dbs))
