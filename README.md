# :desktop_computer: Epic Events :desktop_computer:

It is a first version of CRM to help with client, contract and event management.

***
## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Basic use and commands](#commands)
5. [Tests](#tests)
6. [Sentry](#sentry)

### :newspaper: General Info :newspaper:
***
This is an OpenClassrooms student project. 
The objective is to create a secure CRM (Customer Relationship Management) which can be used via the command line.
It includes a permission system and Sentry logging.

### :briefcase: Technologies :briefcase:
*** 
- [Python](https://www.python.org/): Version ^3.10
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/2.0.20/): Version ^2.0.20
- [Click](https://pypi.org/project/click/): Version ^8.1.7
- [Python-dotenv](https://pypi.org/project/python-dotenv/): Version ^1.0.0
- [Psychopg2-binary](https://pypi.org/project/psycopg2-binary/2.9.7/): Version ^2.9.7
- [Argon2-cffi](https://pypi.org/project/argon2-cffi/): Version ^23.1.0
- [Pyjwt](https://pypi.org/project/PyJWT/): Version ^2.8.0
- [Pytest](https://pypi.org/project/pytest/7.4.2/): Version ^7.4.2
- [Flake8](https://pypi.org/project/flake8/): Version ^6.1.0
- [Coverage](https://pypi.org/project/coverage/): Version ^7.3.1
- [Pytest-sqlalchemy-mock](https://pypi.org/project/pytest-sqlalchemy-mock/): Version ^0.1.5
- [Sentry-sdk](https://pypi.org/project/sentry-sdk/1.35.0/): Version ^1.35.0
- [Poetry](https://pypi.org/project/poetry/1.6.1/): Version 1.6.1
- [Docker](https://docs.docker.com/get-docker/): Version 24.0.7
- PostgreSQL

### :wrench: Installation :wrench:
***
Prerequisites: Docker, Python, Poetry, Sentry
***
In your directory for the project:

Clone repository from:
- [Epic Events](https://github.com/SpiritF0rest/OC_Python_P12_Epic_Events)

#### :wrench: Virtual environment and modules :wrench:

```
To install modules:
$ poetry install

To active the virtual environment (Linux):
$ source $(poetry env info --path)/bin/activate

To active the virtual environment (Windows Powershell):
$ & ((poetry env info --path) + "\Scripts\activate.ps1")

To deactive the virtual environment: 
$ deactivate
```

#### :whale2: Docker :whale2:

```
To pull postgres image:
$ docker pull postgres

To create and run the Postgres container:
$ docker run --name ee-postgres -p 5432:5432 -e POSTGRES_PASSWORD={your_password} -e POSTGRES_DB={DB_name} -d postgres

Ensure that the Postgres container is built and currently executing:
$ docker ps
```

#### :wrench: Dotenv and init DB :wrench:

```
Copy the .env.example in a .env file and fill with the correct data:
DB_URL : be careful that it matches what you put when creating the docker container
FIRST_USER_* : the first manager who will be responsible for creating the first users

When your container is running, .env is filled, the modules are installed and the environment is activated, Init the database:
$ poetry run python epic_events/database.py
```
Now, you can use the app :tada:

### :keyboard: Basic use and commands :keyboard:
***
```
All commands start with:
$ python3 -m epic_events

If you need help to find a main command:
$ python3 -m epic_events --help

If you need help to find a secondary command, example: 
$ python3 -m epic_events client --help

To connect you:
$ python3 -m epic_events auth login -e {your_email}

To know what the options are for a command (when you're connected), example:
$ python3 -m epic_events contract create --help

To disconnect you:
$ python3 -m epic_events auth logout    
```

### :newspaper: Tests :newspaper:
***
```
To test:
$ pytest

To generate Flake 8 report:
$ flake8

To see coverage:
$ coverage run -m pytest
$ coverage report
$ coverage html
```

### :eyes: Sentry :eyes:
***
On sentry you will find unexpected errors. And also information logs when a user is created or modified and a contract is signed

:snake: Enjoy :snake:
