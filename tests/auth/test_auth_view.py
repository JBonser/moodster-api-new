"""
Test module for the auth resource/endpoint.
"""
from starlette.testclient import TestClient
import pytest

from app.main import app
from app.users.crud import create_user
from app.database.base import db_session
from app.users.schema import UserCreate

client = TestClient(app)


@pytest.fixture()
def test_db_user():
    test_user_create = UserCreate(
        first_name="john",
        surname="smith",
        email="johnsmith@live.co.uk",
        password="password",
    )
    create_user(db_session, test_user_create)
    return test_user_create


def test_auth_login_success(db_fixture, test_db_user):
    login_data = {"username": test_db_user.email, "password": test_db_user.password}
    response = client.post("/auth/", data=login_data)

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_auth_login_fails_with_incorrect_password(db_fixture, test_db_user):
    login_data = {"username": test_db_user.email, "password": "incorred_password"}
    response = client.post("/auth/", data=login_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Could not validate email or password"


def test_auth_login_fails_with_unknown_user(db_fixture, test_db_user):
    login_data = {"username": "nobody@live.com", "password": test_db_user.password}
    response = client.post("/auth/", data=login_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Could not validate email or password"
