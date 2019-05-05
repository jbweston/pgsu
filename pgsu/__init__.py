# -*- coding: utf-8 -*-
"""Connect to an existing PostgreSQL cluster as the `postgres` superuser and execute SQL commands.
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess

from enum import IntEnum
import click

DEFAULT_DBINFO = {
    'host': None,
    'port': None,
    'user': None,
    'password': None,
    'database': None,
}


class PostgresConnectionMode(IntEnum):
    """Describe mode of connecting to postgres."""

    DISCONNECTED = 0
    PSYCOPG = 1
    PSQL = 2


class Postgres(object):  # pylint: disable=useless-object-inheritance
    """
    Connect to an existing PostgreSQL cluster as the `postgres` superuser and execute SQL commands.

    Tries to use psycopg2 with a fallback to psql subcommands (using ``sudo su`` to run as postgres user).

    Simple Example::

        postgres = Postgres()
        postgres.execute("CREATE USER testuser PASSWORD 'testpw'")

    Complex Example::

        postgres = Postgres(interactive=True, dbinfo={'port': 5433})
        postgres.execute("CREATE USER testuser PASSWORD 'testpw'")

    Note: In postgresql
     * you cannot drop databases you are currently connected to
     * 'template0' is the unmodifiable template database (which you cannot connect to)
     * 'template1' is the modifiable template database (which you can connect to)
    """

    def __init__(self,
                 interactive=False,
                 quiet=True,
                 dbinfo=None,
                 determine_setup=True):
        """Store postgres connection info.

        :param interactive: use True for verdi commands
        :param quiet: use False to show warnings/exceptions
        :param dbinfo: psycopg dictionary containing keys like 'host', 'user', 'port', 'database'
        :param determine_setup: Whether to determine setup upon instantiation.
            You may set this to False and use the 'determine_setup()' method instead.
        """
        self.interactive = interactive
        self.quiet = quiet
        self.connection_mode = PostgresConnectionMode.DISCONNECTED
        self.setup_fail_callback = prompt_db_info
        self.setup_fail_counter = 0
        self.setup_max_tries = 1

        if dbinfo is None:
            self.dbinfo = DEFAULT_DBINFO
        else:
            self.dbinfo = dbinfo

        if determine_setup:
            self.determine_setup()

    def execute(self, command, **kwargs):
        """Execute postgres command using determined connection mode.

        :param command: A psql command line as a str
        :param kwargs: will be forwarded to _execute_... function
        """
        kw_copy = self.dbinfo.copy()
        kw_copy.update(kwargs)

        if self.connection_mode == PostgresConnectionMode.PSYCOPG:  # pylint: disable=no-else-return
            return _execute_psyco(command, **kw_copy)
        elif self.connection_mode == PostgresConnectionMode.PSQL:
            return _execute_sh(command, **kw_copy)

        raise ValueError('Could not connect to postgres.')

    def set_setup_fail_callback(self, callback):
        """
        Set a callback to be called when setup cannot be determined automatically

        :param callback: a callable with signature ``callback(dbinfo)``
        """
        self.setup_fail_callback = callback

    def determine_setup(self):
        """ Find out how postgres can be accessed.

        Depending on how postgres is set up, psycopg2 can be used to create dbs and db users,
        otherwise a subprocess has to be used that executes psql as an os user with the right permissions.

        Note: We aim for a setup that is can manipulate (create/drop) databases and database users.
         We therefore do *not* want to connect to databases of AiiDA profiles and will connect to 'template1'.

        """
        # find out if we run as a postgres superuser or can connect as postgres
        # This will work on OSX in some setups but not in the default Debian one
        dbinfo = self.dbinfo.copy()

        pg_users = [dbinfo['user']
                    ] if dbinfo['user'] is not None else [None, 'postgres']
        for pg_user in pg_users:
            dbinfo['user'] = pg_user
            if _try_connect_psycopg(**dbinfo):
                self.dbinfo = dbinfo
                self.connection_mode = PostgresConnectionMode.PSYCOPG
                return True

        # This will work for the default Debian postgres setup, assuming that sudo is available to the user
        # Check if the user can find the sudo command
        if _sudo_exists():
            dbinfo['user'] = 'postgres'
            if _try_subcmd(non_interactive=bool(not self.interactive),
                           **dbinfo):
                self.dbinfo = dbinfo
                self.connection_mode = PostgresConnectionMode.PSQL
                return True
        elif not self.quiet:
            click.echo(
                'Warning: Could not find `sudo` for connecting to the database.'
            )

        self.setup_fail_counter += 1
        self._no_setup_detected()
        return False

    def _no_setup_detected(self):
        """Print a warning message and calls the failed setup callback"""
        message = '\n'.join([
            'Warning: Unable to autodetect postgres setup - do you know how to access it?',
        ])
        if not self.quiet:
            click.echo(message)
        if self.interactive and self.setup_fail_callback and self.setup_fail_counter <= self.setup_max_tries:
            self.dbinfo = self.setup_fail_callback(self.dbinfo)
            self.determine_setup()


def prompt_db_info(dbinfo):
    """
    Prompt interactively for postgres database connection details

    Can be used as a setup fail callback for :py:class:`aiida.manage.external.postgres.Postgres`

    :return: dictionary with the following keys: host, port, database, user
    """
    access = False
    while not access:
        dbinfo_new = {}
        dbinfo_new['host'] = click.prompt('postgres host',
                                          default=dbinfo['host'],
                                          type=str)
        dbinfo_new['port'] = click.prompt('postgres port',
                                          default=dbinfo['port'],
                                          type=int)
        dbinfo_new['user'] = click.prompt('postgres super user',
                                          default=dbinfo['user'],
                                          type=str)
        dbinfo_new['database'] = click.prompt('database',
                                              default=dbinfo['database'],
                                              type=str)
        click.echo('')
        click.echo('Trying to access postgres ...')
        if _try_connect_psycopg(**dbinfo_new):
            access = True
        else:
            dbinfo_new['password'] = click.prompt(
                'postgres password of {}'.format(dbinfo_new['user']),
                hide_input=True,
                type=str,
                default='')
            if not dbinfo_new.get('password'):
                dbinfo_new.pop('password')
    return dbinfo_new


def _try_connect_psycopg(**kwargs):
    """
    try to start a psycopg2 connection.

    :return: True if successful, False otherwise
    """
    from psycopg2 import connect
    success = False
    try:
        conn = connect(**kwargs)
        success = True
        conn.close()
    except Exception:  # pylint: disable=broad-except
        pass
    return success


def _sudo_exists():
    """
    Check that the sudo command can be found

    :return: True if successful, False otherwise
    """
    try:
        subprocess.check_output(['sudo', '-V'])
    except subprocess.CalledProcessError:
        return False
    except OSError:
        return False

    return True


def _try_subcmd(**kwargs):
    """
    try to run psql in a subprocess.

    :return: True if successful, False otherwise
    """
    success = False
    try:
        kwargs['stderr'] = subprocess.STDOUT
        _execute_sh(r'\q', **kwargs)
        success = True
    except subprocess.CalledProcessError:
        pass
    return success


def _execute_psyco(command, **kwargs):
    """
    executes a postgres commandline through psycopg2

    :param command: A psql command line as a str
    :param kwargs: will be forwarded to psycopg2.connect
    """
    import psycopg2

    output = None
    with psycopg2.connect(**kwargs) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(command)
            if cursor.description is not None:
                output = cursor.fetchall()

    # see http://initd.org/psycopg/docs/usage.html#with-statement
    conn.close()
    return output


def _execute_sh(command, user='postgres', **kwargs):
    """
    executes a postgres command line as another system user in a subprocess.

    :param command: A psql command line as a str
    :param user: Name of a system user with postgres permissions
    :param kwargs: connection details to forward to psql, signature as in psycopg2.connect

    To stop `sudo` from asking for a password and fail if one is required,
    pass `non_interactive=True` as a kwarg.
    """
    options = ''
    database = kwargs.pop('database', None)
    if database:
        options += '-d {}'.format(database)
    kwargs.pop('password', None)
    host = kwargs.pop('host', None)
    if host and host != 'localhost':
        #if host:
        options += ' -h {}'.format(host)
    port = kwargs.pop('port', None)
    if port:
        options += ' -p {}'.format(port)

    # Build command line
    sudo_cmd = ['sudo']
    non_interactive = kwargs.pop('non_interactive', None)
    if non_interactive:
        sudo_cmd += ['-n']
    su_cmd = ['su', user, '-c']

    psql_cmd = [
        'psql {options} -tc {}'.format(escape_for_bash(command),
                                       options=options)
    ]
    sudo_su_psql = sudo_cmd + su_cmd + psql_cmd
    result = subprocess.check_output(sudo_su_psql, **kwargs)
    result = result.decode('utf-8').strip().split('\n')
    result = [i for i in result if i]

    return result


def escape_for_bash(str_to_escape):
    """
    This function takes any string and escapes it in a way that
    bash will interpret it as a single string.

    Explanation:

    At the end, in the return statement, the string is put within single
    quotes. Therefore, the only thing that I have to escape in bash is the
    single quote character. To do this, I substitute every single
    quote ' with '"'"' which means:

    First single quote: exit from the enclosing single quotes

    Second, third and fourth character: "'" is a single quote character,
    escaped by double quotes

    Last single quote: reopen the single quote to continue the string

    Finally, note that for python I have to enclose the string '"'"'
    within triple quotes to make it work, getting finally: the complicated
    string found below.
    """
    escaped_quotes = str_to_escape.replace("'", """'"'"'""")
    return "'{}'".format(escaped_quotes)
