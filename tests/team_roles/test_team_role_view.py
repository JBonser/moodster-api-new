"""
Test module for the team role resource/endpoint.
"""
from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_team_roles_get_default_roles(db_session, default_team_roles):
    member, admin = default_team_roles

    response = client.get("/team_roles")

    json_response = response.json()
    assert response.status_code == 200
    assert any(item["public_id"] == member.public_id for item in json_response)
    assert any(item["public_id"] == admin.public_id for item in json_response)
