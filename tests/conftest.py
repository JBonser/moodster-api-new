"""
This module is automatically imported by pytest and so any fixtures
that need to be available to all/most tests should be defined here.
"""
import pytest

from app.main import app
from app.database.base import Base, Session
from app.auth.depends import auth_required
from app.users.crud import create_user
from app.users.schema import UserCreate
from app.team_roles.schema import TeamRoleCreate
from app.team_roles.crud import create_team_role
from tests.dependency_overrides import auth_required_override
from app.auth.logic import create_access_token


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

    session = Session()
    session.expire_on_commit = False
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


@pytest.fixture()
def default_user_auth_header(request, default_db_user):
    """
    Test fixture for overriding the login_required token
    """
    token = create_access_token(default_db_user.id)
    header = {"Authorization": f"Bearer {token}"}
    return header


@pytest.fixture()
def default_team_roles(db_session):
    """
    Test fixture for creating the two default roles.
    """
    member_role = TeamRoleCreate(name="Member")
    admin_role = TeamRoleCreate(name="Admin")

    member = create_team_role(db=db_session, team_role=member_role)
    admin = create_team_role(db=db_session, team_role=admin_role)

    return member, admin


@pytest.fixture()
def default_db_user(db_session):
    user_create = UserCreate(
        first_name="default",
        surname="db",
        email="default_db_user@live.co.uk",
        password="password",
    )

    db_user = create_user(db_session, user_create)
    return db_user
