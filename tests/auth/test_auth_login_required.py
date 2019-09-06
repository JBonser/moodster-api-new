"""
Test module for the login_required dependency route functionality.
"""
from starlette.testclient import TestClient
import pytest

from app.main import app
from app.users.crud import create_user
from app.database.base import db_session
from app.users.schema import UserCreate
from app.auth.logic import create_access_token

client = TestClient(app)


@pytest.fixture()
def test_db_user():
    user_create = UserCreate(
        first_name="john",
        surname="smith",
        email="johnsmith@live.co.uk",
        password="password",
    )
    db_user = create_user(db_session, user_create)
    return db_user


def test_login_required_fails_with_invalid_users_token(db_fixture, test_db_user):
    user = test_db_user
    token = create_access_token(44)
    header = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/users/{user.id}", headers=header)

    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]


def test_login_fails_with_invalid_token_type(db_fixture, test_db_user):
    token = b"this is a random byte string"
    header = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/users/{test_db_user.id}", headers=header)

    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]


def test_login_required_succeeds(db_fixture, test_db_user):
    token = create_access_token(test_db_user.id)
    header = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/users/{test_db_user.id}", headers=header)

    assert response.status_code == 200
