# pgsu

Connect to an existing PostgreSQL cluster as the `postgres` superuser and execute SQL commands.

Use this module e.g. to create databases and database users from a command line interface.

## Features

 * autodetects postgres setup
 * uses [psycopg2](http://initd.org/psycopg/docs/index.html) to connect where possible
 * can use `sudo` to become the `postgres` UNIX user if necessary

## Usage

```python
from pgsu import Postgres
postgres = Postgres()  # this may prompt for sudo password
postgres.execute("CREATE USER newuser WITH PASSWORD 'newpassword'")
users = postgres.execute("SELECT usename FROM pg_user WHERE usename='newuser'")
print(users)
```

## Tests

Run the tests as follows:
````bash
pip install -e .[testing]
pytest
```
