# encoding: utf-8
from __future__ import absolute_import
from setuptools import setup, find_packages

setup(
    name='pgsu',
    version='0.1.0',
    description=
    ('Connect to an existing PostgreSQL cluster as the `postgres` superuser and execute SQL commands.'
     ),
    url='https://github.com/ltalirz/pgsu',
    author='AiiDA Team',
    author_email='aiidateam@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'psycopg2-binary>=2.8.3',
        'click',
        "enum34; python_version<'3.5'",
    ],
    extras_require={
        'testing': ['pytest', 'pgtest>=1.3.1', 'pytest-cov'],
        # note: pre-commit hooks require python3
        "pre-commit": [
            "pre-commit==1.18.3", "yapf==0.28.0", "prospector==1.2.0",
            "pylint==2.4.4"
        ]
    },
    entry_points={'console_scripts': ["pgsu=pgsu.cli:run"]})
