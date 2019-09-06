"""
Test module for the user resource/endpoint.
"""
from starlette.testclient import TestClient
import pytest

from app.main import app
from app.users.crud import create_user
from app.database.base import db_session
from app.users.schema import UserCreate, User

client = TestClient(app)


@pytest.fixture()
def test_user():
    test_user_create = UserCreate(
        email="johnsmith@live.co.uk",
        password="password",
    )
    test_user_get = User(
        public_id="1",
        email="johnsmith@live.co.uk",
    )
    return test_user_create, test_user_get


def test_user_creation_success(db_fixture, test_user):
    test_user_create, test_user_get = test_user
    response = client.post("/users/", json=test_user_create.dict())

    assert response.status_code == 200
    assert response.json() == test_user_get


def test_user_creation_fails_with_duplicate_entry(db_fixture, test_user):
    test_user_create, test_user_get = test_user
    create_user(db_session, test_user_create)

    response = client.post(f"/users/", json=test_user_create.dict())
    assert response.status_code == 400
    assert "user with this email already exists" in response.json()["detail"]


def test_user_get(db_fixture, test_user, token_fixture):
    test_user_create, test_user_get = test_user
    user = create_user(db_session, test_user_create)

    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json() == test_user_get


def test_user_get_fails_without_authenticating(db_fixture, test_user):
    test_user_create, test_user_get = test_user
    user = create_user(db_session, test_user_create)

    response = client.get(f"/users/{user.public_id}")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
