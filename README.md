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
   * Ubuntu 18.04 & PostgreSQL installed via `apt`
   * Ubuntu 18.04 & PostgreSQL docker container
   * MacOS 10.15 and PostgreSQL installed via `conda`
   * Windows 2019 and PostgreSQL installed via `conda`
   
## Usage

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

## Tests

Run the tests as follows:
````bash
pip install -e .[testing]
pytest
```
