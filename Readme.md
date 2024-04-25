# Fast API application Template

This template is designed to demonstrate ways of using Fast API,
hightlight different use cases of this framework, and usefull tweaks,
methods that allows easier and/or better usage according to the "best practice".

## !IMPORTANT:
<b>This project may contains some more explanations / description that are needed
for the project. Remove the unnecessary parts but if it is fits to the project
simply remove this section</b>

The list belows describes the main features of this template:

## Introduction

1. Demostrates architecure that are inspired by "Clean Architecture". More details are
metioned `apps` folder.
2. Demostrates different ways of dividing the code based on features needs, it complexicty,
and amount of the code.
3. Implements some code examples, handling entities creation, handling exceptions, schemas implementation, and etc.
4. Implements FastAPI configuration such as db connection establishing, adding middlewares, and etc.
5. Implements Settings module which looks similar to Django and reads the env variables from .env file
6. Implements auto-importing Fast API Routes / SQLAlchemy models recursively by folder for easier experience of writting
imports.
7. Migrations mechanism that autosearches the all Models and by using Alembic autogenerates migrations
for them.
8. Pre-commit hooks that are required for static code checking by using flake8, bandit.
9. Seeds mechanism that allows to write scripts for filling database with some general data (for instance
create super admin).
10. Demostrates the JWT Auth implementation example.
11. Demostrates a possibility of permissions implementation.
12. Implements logger mechanism and logs request / response / orm based on environment variables. In addition,
it implements removing sensitive data from logs. More details are in `core.loggers.logger`
13. Implements python shell based on ipython that allows to run python console and execute some code.
It has some pre-imported this such as SQLAlchemy models, Storages and Cases. More details is desribed
in `.ipython` folder.
14. Auto-generated Admin panel based on Flask-Admin (https://flask-admin.readthedocs.io/en/latest/). More details
is mentioned in `apps/admin` folder.

## How to install and run

1. Clone the repository
2. Install requirements with dev requirements via pipenv `pipenv install --dev`. Use
`pipenv install` if dev requirements is not needed.
3. Fill `.env` file based on `.env.example`
4. Activate pipenv environment (if needed) `pipenv shell`
5. Run migrations via `pipenv run migrate`
6. Run seeds `pipenv run seeds all`
7. Run API (FastAPI) server by typing `pipenv run server`
The Swagger docs will be accessible on the `/doc` endpoint
8. Run Admin Panel (Flask Admin) server by typing `pipenv run admin`
To log in use credentials from `seeds/admins.py`
9. Run Python Console (IPython) by typing `pipenv run shell`. Main classes will be imported.
10. To use the applicatin in production use gunicorn with Uvicorn. Example of the command:
`pipenv run gunicorn api:fast_api --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8003`

## How to work with migrations and ORM Models

1. Create a `models` folder at any hierarchy level inside `apps` folder.
2. Create `__init__.py` file inside newly created `models` folder. 
2. Import a model class inside `__init__.py` and it's name to `__all__` variable. The models classes
in this will be automatically imported and used in Alembic migrations.
3. Autogenerate migrations via `pipenv run auto_migration`
4. Run migrations via `pipenv run manual_migration`

Example in `apps/messages/models` folder

## How to work with Fast API Routers
1. Create any route at any hierarchy level inside `apps` folder.
2. Create `routers_{version}.py` file import route. Version is according to the version of API.
For instance, `routers_v1.py`, `routers_v2.py` files.
3. Import new routers inside this file and place into `routers` variable. The routers will be automatically
imported and added to Fast API routes.

Example in `apps/messages/routers_v1.py` file.

## Seeds

"admins" - inits database with default admin.

### Introduction

Seeds are data initialization for models such as `<Model name>`, and etc.
Sctipts are one time scripts

1. Сreate new .py file inside `scripts/seeds` / `scipts/one_time_scripts` folder
2. Write a script and add `perform` method as entrypoint into your script
3. Add filename into `script_names` in `scripts/run_seeds.py` or `scripts/run_script.py` file

### Usage

1. Run script via `pipenv run seed seed_name` / `pipenv run script <args>`
2. To run all seeds `pipenv run seed all`. Scripts has some params thus scipts can be run only by one

### !IMPORTANT

Try to write yout script by using methods `get_or_create` or similar
to avoid duplication in database


## How to run tests

1. Go to project directory
2. Call `pipenv run python -m unittest`

## To setup pre-commit hooks

1. Install requirements with dev requirements via pipenv `pipenv install --dev`.
2. `pipenv run pre-commit install`

## To setup python linter

### Vscode

1. create (if not exist) `.vscode` folder in the project
2. update exist `.vscode/settings.json` with `settings.json.vscode.example` params

   Or

   copy `settings.json.vscode.example` to `.vscode/settings.json`

3. update `"python.pythonPath"` parameter with path to your python

