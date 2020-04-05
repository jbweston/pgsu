# encoding: utf-8
from __future__ import absolute_import
from setuptools import setup, find_packages
import os

THIS_FOLDER = os.path.split(os.path.abspath(__file__))[0]

setup(
    name='pgsu',
    version='0.1.0',
    description=
    ('Connect to an existing PostgreSQL cluster as a postgres superuser and execute SQL commands.'
     ),
    long_description=open(os.path.join(THIS_FOLDER, 'README.md')).read(),
    long_description_content_type='text/markdown',
    url='https://github.com/aiidateam/pgsu',
    author='AiiDA Team',
    author_email='aiidateam@gmail.com',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
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
