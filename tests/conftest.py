"""
This module is automatically imported by pytest and so any fixtures
that need to be available to all/most tests should be defined here.
"""
import pytest

from app.main import app
from app.database.base import Base, db_session as session
from app.auth.depends import auth_required
from tests.dependency_overrides import auth_required_override


@pytest.fixture(scope="session")
def engine():
    from app.database.base import engine

    return engine


@pytest.yield_fixture()
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.yield_fixture()
def db_session(engine, tables):
    """Returns an sqlalchemy session, and after the test
    tears down everything properly.
    """
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture()
def token_fixture(request):
    """
    Test fixture for overriding the login_required token dependency
    This allows us to more easily test the logic of the routes, without
    being tripped up by the authentication constantly.
    """
    app.dependency_overrides[auth_required] = auth_required_override

    def teardown():
        app.dependency_overrides = {}

    request.addfinalizer(teardown)
