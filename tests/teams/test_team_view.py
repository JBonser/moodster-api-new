"""
Test module for the team resource/endpoint.
"""
from starlette.testclient import TestClient
import pytest
from app.main import app
from app.teams.crud import create_team
from app.teams.schema import TeamCreate

client = TestClient(app)


@pytest.fixture()
def test_team_create():
    test_user_create = TeamCreate(name="test_team_name")
    return test_user_create


def test_team_get_success(db_session, test_team_create, token_fixture):
    team = create_team(db_session, test_team_create)
    response = client.get(f"/teams/{team.public_id}")
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["name"] == team.name
    assert json_response["public_id"] == team.public_id


def test_team_get_fails_with_invalid_id(db_session, token_fixture):
    team_id = "my-invalid-id"
    response = client.get(f"/teams/{team_id}")

    json_response = response.json()
    assert response.status_code == 404
    assert json_response["detail"] == f"The team with id {team_id} does not exist"


def test_team_creation(db_session, test_team_create):
    response = client.post("/teams/", json=test_team_create.dict())
    json_response = response.json()

    assert response.status_code == 201
    assert json_response["name"] == "test_team_name"
    assert "public_id" in json_response


def test_team_creation_no_name(db_session):
    response = client.post("/teams/", json={})
    json_response = response.json()

    assert response.status_code == 422
    assert json_response["detail"][0]["msg"] == "field required"
    assert json_response["detail"][0]["type"] == "value_error.missing"
