"""
Test module for the login_required dependency route functionality.
"""
from starlette.testclient import TestClient

from app.main import app
from app.auth.logic import create_access_token

client = TestClient(app)


def test_login_required_fails_with_invalid_users_token(db_session, default_db_user):
    user = default_db_user
    token = create_access_token(44)
    header = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/users/{user.public_id}", headers=header)

    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]


def test_login_required_fails_with_none_token(db_session, default_db_user):
    user = default_db_user
    token = create_access_token(None)
    header = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/users/{user.public_id}", headers=header)

    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]


def test_login_fails_with_invalid_token_type(db_session, default_db_user):
    token = b"this is a random byte string"
    header = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/users/{default_db_user.public_id}", headers=header)

    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]


def test_login_required_succeeds(db_session, default_db_user):
    token = create_access_token(default_db_user.id)
    header = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/users/{default_db_user.public_id}", headers=header)

    assert response.status_code == 200
