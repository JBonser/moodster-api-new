"""
Test module for the user resource/endpoint.
"""
from starlette.testclient import TestClient
import pytest

from app.main import app
from app.users.crud import create_user, get_user_by_email
from app.database.base import db_session
from app.users.schema import UserCreate

client = TestClient(app)


@pytest.fixture()
def test_user():
    test_user_create = UserCreate(email="johnsmith@live.co.uk", password="password")
    return test_user_create


def test_user_creation_success(db_fixture, test_user):
    user_create_schema = test_user
    response = client.post("/users/", json=user_create_schema.dict())
    user = get_user_by_email(db_session, user_create_schema.email)

    json_response = response.json()
    assert response.status_code == 200
    assert json_response["email"] == user.email
    assert json_response["public_id"] == user.public_id


def test_user_creation_fails_with_duplicate_entry(db_fixture, test_user):
    user_create_schema = test_user
    create_user(db_session, user_create_schema)

    response = client.post(f"/users/", json=user_create_schema.dict())
    assert response.status_code == 400
    assert "user with this email already exists" in response.json()["detail"]


def test_user_get(db_fixture, test_user, token_fixture):
    user_create_schema = test_user
    user = create_user(db_session, user_create_schema)

    response = client.get(f"/users/{user.public_id}")
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["email"] == user.email
    assert json_response["public_id"] == user.public_id


def test_user_get_fails_without_authenticating(db_fixture, test_user):
    test_user_create = test_user
    user = create_user(db_session, test_user_create)

    response = client.get(f"/users/{user.public_id}")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
