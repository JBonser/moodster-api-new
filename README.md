# Moodster API

Moodster API Project

## Running the Application

### Development

To run the application in development mode simply run:

```bash
docker-compose up -d
```

This will use the docker-compose.override.yml and mount your local directory
within the container to allow for live changes to the application without requiring
a rebuild.

Navigate to:

```bash
http://127.0.0.1/docs
```

You can now start interacting with the API using the interactive OpenAPI documentation.

## Running the Tests

To run the unit tests simply override the default command for the moodster-api service like so:

```bash
docker-compose run moodster-api pytest tests/
```

### Running with coverage

```bash
docker-compose run moodster-api pytest --cov=app/ tests/
```

## Updating the database models

If you change any of the database models you will need to run alembic to allow it to detect any schema changes,
so that it can try and generate the migration script for you. To do this you need to run:

```bash
alembic revision --autogenerate
```

This will generate a database migration revision which you should then go and inspect to see what migrations have been
generated. This process can sometimes work incorrectly so it's important to check this revision file before comitting.

Finally if you want to add some data upgrade/downgrades to the migrations then these will also have to be done by hand.
