[![Build Status](https://github.com/aiidateam/pgsu/workflows/ci/badge.svg)](https://github.com/aiidateam/pgsu/actions)
[![Coverage Status](https://codecov.io/gh/aiidateam/pgsu/branch/master/graph/badge.svg)](https://codecov.io/gh/aiidateam/pgsu)
[![PyPI version](https://badge.fury.io/py/pgsu.svg)](https://badge.fury.io/py/pgsu)
[![GitHub license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/aiidateam/pgsu/blob/master/LICENSE)
# pgsu

Connect to an existing PostgreSQL cluster as a PostgreSQL [SUPERUSER](https://www.postgresql.org/docs/current/sql-createrole.html) and execute SQL commands.

[`psycopg2`](https://pypi.org/project/psycopg2/) has a great API for interacting with PostgreSQL, once you provide it with the connection parameters for a given database.
However, what if your desired database and database user do not yet exist?
In order to create them, you will need to connect to PostgreSQL as a SUPERUSER.

## Features

 * autodetects postgres setup, tested on
   * [Ubuntu 18.04](https://github.com/actions/virtual-environments/blob/master/images/linux/Ubuntu1804-README.md) & PostgreSQL installed via `apt`
   * [Ubuntu 18.04](https://github.com/actions/virtual-environments/blob/master/images/linux/Ubuntu1804-README.md) & PostgreSQL docker container
   * [MacOS 10.15](https://github.com/actions/virtual-environments/blob/master/images/macos/macos-10.15-Readme.md) and PostgreSQL installed via `conda`
   * [Windows Server 2019](https://github.com/actions/virtual-environments/blob/master/images/win/Windows2019-Readme.md) and PostgreSQL installed via `conda`
 * uses [psycopg2](http://initd.org/psycopg/docs/index.html) to connect if possible
 * can use `sudo` to become the `postgres` UNIX user if necessary/possible (default Ubuntu PostgreSQL setups)
   
## Usage

### Python API
```python
from pgsu import PGSU
pgsu = PGSU()  # On Ubuntu, this may prompt for sudo password
pgsu.execute("CREATE USER newuser WITH PASSWORD 'newpassword'")
users = pgsu.execute("SELECT usename FROM pg_user WHERE usename='newuser'")
print(users)
```

While the main point of the package is to *guess* how to connect as a postgres superuser, you can also provide partial or all information abut the setup using the `dsn` parameter.
These are the default settings:
```python
from pgsu import PGSU
pgsu = PGSU(dsn={
    'host': None,
    'port': 5432,
    'user': 'postgres',
    'password': None,
    'database': 'template1',  # Note: you cannot drop databases you are connected to
})
```

### Command line tool

The package also comes with a very basic `pgsu` command line tool that allows users to execute PostgreSQL commands as the superuser:
```
$ pgsu "SELECT usename FROM pg_user"
Trying to connect to PostgreSQL...
Executing query: SELECT usename FROM pg_user
[('aiida_qs_leopold',),
 ('postgres',)]
```

## Tests

Run the tests as follows:
```bash
pip install -e .[testing]
pytest
```
