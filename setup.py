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
        'psycopg2',
        'click',
        "enum34; python_version<'3.5'",
    ],
    extras_require={
        'testing': ['pytest'],
        # note: pre-commit hooks require python3
        "pre-commit": [
            "pre-commit==1.11.0", "yapf==0.27.0", "prospector==1.1.6.2",
            "pylint==2.1.1"
        ]
    })
