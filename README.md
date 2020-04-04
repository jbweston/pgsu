[![Build Status](https://github.com/ltalirz/pgsu/workflows/ci/badge.svg)](https://github.com/ltalirz/pgsu/actions)
[![Coverage Status](https://codecov.io/gh/ltalirz/pgsu/branch/master/graph/badge.svg)](https://codecov.io/gh/ltalirz/pgsu)
[![PyPI version](https://badge.fury.io/py/pgsu.svg)](https://badge.fury.io/py/pgsu)
[![GitHub license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/ltalirz/pgsu/blob/master/LICENSE)
# pgsu

Connect to an existing PostgreSQL cluster as the `postgres` superuser and execute SQL commands.

Use this module e.g. to create databases and database users from a command line interface.

## Features

 * autodetects postgres setup
 * uses [psycopg2](http://initd.org/psycopg/docs/index.html) to connect where possible
 * can use `sudo` to become the `postgres` UNIX user if necessary/possible
 * tested via continuous integration on
   * [Ubuntu 18.04](https://github.com/actions/virtual-environments/blob/master/images/linux/Ubuntu1804-README.md) & PostgreSQL installed via `apt`
   * [Ubuntu 18.04](https://github.com/actions/virtual-environments/blob/master/images/linux/Ubuntu1804-README.md) & PostgreSQL docker container
   * [MacOS 10.15](https://github.com/actions/virtual-environments/blob/master/images/macos/macos-10.15-Readme.md) and PostgreSQL installed via `conda`
   * [Windows Server 2019](https://github.com/actions/virtual-environments/blob/master/images/win/Windows2019-Readme.md) and PostgreSQL installed via `conda`
   
## Usage

### Python API
```python
from pgsu import PGSU
pgsu = PGSU()  # this may prompt for sudo password
pgsu.execute("CREATE USER newuser WITH PASSWORD 'newpassword'")
users = pgsu.execute("SELECT usename FROM pg_user WHERE usename='newuser'")
print(users)
```

While the main point of the package is to *guess* the PostgreSQL setup, you can also provide partial or all information abut the setup using the `dsn` parameter.
These are the default settings:
```python
from pgsu import PGSU
pgsu = PGSU(dsn={
    'host': 'localhost',
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
