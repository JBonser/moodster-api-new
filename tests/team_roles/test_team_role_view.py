"""
Test module for the team role resource/endpoint.
"""
from starlette.testclient import TestClient
import pytest
from app.main import app
from app.team_roles.crud import create_team_role
from app.team_roles.schema import TeamRoleCreate

client = TestClient(app)


@pytest.fixture()
def test_team_roles():
    member_role = TeamRoleCreate(name="Member")
    admin_role = TeamRoleCreate(name="Admin")
    return member_role, admin_role


def test_team_roles_get_default_roles(db_session, test_team_roles):
    member, admin = test_team_roles
    member_role = create_team_role(db_session, member)
    admin_role = create_team_role(db_session, admin)

    response = client.get("/team_roles")
    json_response = response.json()

    assert response.status_code == 200
    assert any(item["public_id"] == member_role.public_id for item in json_response)
    assert any(item["public_id"] == admin_role.public_id for item in json_response)
