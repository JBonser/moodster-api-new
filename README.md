# Moodster API
Moodster API Project

## Installation

```bash
python3 -m venv env
source env/bin/activate
pip install -e .
```

## Running the Application

### Development

If running for the first time you will need to create the DB, run:

```bash
alembic upgrade head
```

To run the application in development simply call:

```bash
uvicorn app.main:app --reload
```

Navigate to:

```bash
http://127.0.0.1:8000/docs
```

You can now start interacting with the API using the interactive OpenAPI documentation.

## Running the Tests

To run the unit tests use the unittest discovery like so:

```bash
pytest tests/
```

### Running with coverage

```bash
pytest --cov=app/ tests/
```

## Updating the database models

If you change any of the database models you will need to ruin alembic to allow it to detect any schema changes,
so that it can try and generate the migration script for you. To do this you need to run:

```bash
alembic revision --autogenerate
```

This will generate a database migration revision which you should then go and inspect to see what migrations have been
generated. This process can sometimes work incorrectly so it's important to check this revision file before comitting.

## Initialising the database with default data
For development of the application it is sometimes useful to have some default data in the database so you don't have to re-create this every time.
To apply this defult data, simply call this script after you've ran the database migrations above:
```
python -m scripts.dev_db_initialise
```