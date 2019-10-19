"""
Test module for the team membership resource/endpoint.
"""
from starlette.testclient import TestClient
import pytest
from app.main import app
from app.users.schema import UserCreate
from app.users.crud import create_user
from app.teams.schema import TeamCreate
from app.teams.crud import create_team
from app.team_memberships.crud import create_team_membership
from app.team_member_moods.schema import TeamMemberMoodCreate
from app.team_member_moods.crud import create_team_member_mood
from app.auth.logic import create_access_token

client = TestClient(app)


@pytest.fixture()
def test_users_and_teams(db_session, default_team_roles):
    member, admin = default_team_roles
    # Create two users to be added to separate teams
    user1 = UserCreate(email="johnsmith@live.co.uk", password="password")
    user2 = UserCreate(email="stevejones@live.co.uk", password="password")
    test_user1 = create_user(db_session, user1)
    test_user2 = create_user(db_session, user2)

    # Create the two required teams
    team1 = TeamCreate(name="Team1")
    team2 = TeamCreate(name="Team2")
    test_team1 = create_team(db_session, team1, test_user1)
    test_team2 = create_team(db_session, team2, test_user2)

    # Make the users have a role of member in each of their respective teams.
    create_team_membership(db_session, test_user1, test_team1, member)
    create_team_membership(db_session, test_user2, test_team2, member)

    return test_user1, test_user2, test_team1, test_team2


def test_team_member_mood_post_single_mood_addition(
    db_session, test_users_and_teams, default_moods
):
    test_user1, _, test_team1, _ = test_users_and_teams
    awful, _, _, _, _ = default_moods
    token = create_access_token(test_user1.id)
    header = {"Authorization": f"Bearer {token}"}
    member_mood = TeamMemberMoodCreate(
        team_id=test_team1.public_id, mood_id=awful.public_id
    )
    response = client.post(
        "/team_member_moods/", json=member_mood.dict(), headers=header
    )

    json_response = response.json()

    assert response.status_code == 201
    assert json_response["team"]["public_id"] == test_team1.public_id
    assert json_response["mood"]["public_id"] == awful.public_id
    assert "user" not in json_response
    assert "public_id" in json_response


def test_team_member_moods_post_fails_with_invalid_mood(
    db_session, test_users_and_teams, default_moods
):
    invalid_id = "invalid-id"
    test_user1, _, test_team1, _ = test_users_and_teams

    token = create_access_token(test_user1.id)
    header = {"Authorization": f"Bearer {token}"}

    member_mood = TeamMemberMoodCreate(team_id=test_team1.public_id, mood_id=invalid_id)

    response = client.post(
        "/team_member_moods/", json=member_mood.dict(), headers=header
    )
    json_response = response.json()
    assert response.status_code == 404
    assert json_response["detail"] == f"The mood with id {invalid_id} does not exist"


def test_team_member_moods_post_fails_with_invalid_team(
    db_session, test_users_and_teams, default_moods
):
    invalid_id = "invalid-id"
    test_user1, _, _, _ = test_users_and_teams
    awful, _, _, _, _ = default_moods
    token = create_access_token(test_user1.id)
    header = {"Authorization": f"Bearer {token}"}

    member_mood = TeamMemberMoodCreate(team_id=invalid_id, mood_id=invalid_id)

    response = client.post(
        "/team_member_moods/", json=member_mood.dict(), headers=header
    )
    json_response = response.json()
    assert response.status_code == 404
    assert json_response["detail"] == f"The team with id {invalid_id} does not exist"


def test_team_member_moods_post_fails_with_invalid_user(
    db_session, test_users_and_teams, default_moods
):
    test_user1, _, test_team1, _ = test_users_and_teams
    awful, _, _, _, _ = default_moods

    # Create token for invalid id
    token = create_access_token(44)
    header = {"Authorization": f"Bearer {token}"}
    member_mood = TeamMemberMoodCreate(
        team_id=test_team1.public_id, mood_id=awful.public_id
    )
    response = client.post(
        "/team_member_moods/", json=member_mood.dict(), headers=header
    )

    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]


def test_team_member_mood_get_team_moods_success(
    db_session, test_users_and_teams, default_moods
):
    test_user1, test_user2, test_team1, test_team2 = test_users_and_teams
    awful, _, _, _, amazing = default_moods

    token = create_access_token(test_user1.id)
    header = {"Authorization": f"Bearer {token}"}

    create_team_member_mood(db=db_session, user=test_user1, team=test_team1, mood=awful)
    create_team_member_mood(
        db=db_session, user=test_user1, team=test_team1, mood=amazing
    )
    response = client.get(
        f"/team_member_moods/?team_id={test_team1.public_id}", headers=header
    )
    json_response = response.json()

    assert response.status_code == 200
    assert any(item["mood"]["public_id"] == awful.public_id for item in json_response)
    assert any(item["mood"]["public_id"] == amazing.public_id for item in json_response)


def test_team_member_moods_get_fails_with_invalid_team_id(db_session, token_fixture):
    invalid_id = "invalid_id"
    response = client.get(f"/team_member_moods/?team_id={invalid_id}")
    json_response = response.json()

    assert response.status_code == 404
    assert json_response["detail"] == f"The team with id {invalid_id} does not exist"
