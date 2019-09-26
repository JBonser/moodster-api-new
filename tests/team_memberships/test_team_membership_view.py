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
from app.team_memberships.schema import TeamMembershipCreate
from app.team_memberships.crud import create_team_membership

client = TestClient(app)


@pytest.fixture()
def test_users(db_session):
    user1 = UserCreate(email="johnsmith@live.co.uk", password="password")
    user2 = UserCreate(email="stevejones@live.co.uk", password="password")
    test_user1 = create_user(db_session, user1)
    test_user2 = create_user(db_session, user2)
    return test_user1, test_user2


@pytest.fixture()
def test_teams(db_session):
    team1 = TeamCreate(name="Team1")
    team2 = TeamCreate(name="Team2")
    test_team1 = create_team(db_session, team1)
    test_team2 = create_team(db_session, team2)
    return test_team1, test_team2


def test_team_memberships_post_single_member_addition(
    db_session, test_users, test_teams, default_team_roles, token_fixture
):
    test_user1, test_user2 = test_users
    test_team1, test_team2 = test_teams
    member_role, admin_role = default_team_roles
    membership = TeamMembershipCreate(
        team_id=test_team1.public_id,
        user_id=test_user1.public_id,
        role_id=member_role.public_id,
    )
    response = client.post("/memberships/", json=membership.dict())

    json_response = response.json()

    assert response.status_code == 201
    assert json_response["team"]["public_id"] == test_team1.public_id
    assert json_response["role"]["public_id"] == member_role.public_id
    assert json_response["user"]["public_id"] == test_user1.public_id
    assert "public_id" in json_response


def test_team_memberships_post_fails_with_invalid_role(
    db_session, test_users, test_teams, token_fixture
):
    invalid_id = "invalid-id"
    test_user1, test_user2 = test_users
    test_team1, test_team2 = test_teams
    membership = TeamMembershipCreate(
        team_id=test_team1.public_id, user_id=test_user1.public_id, role_id=invalid_id
    )

    response = client.post("/memberships/", json=membership.dict())
    json_response = response.json()
    assert response.status_code == 404
    assert json_response["detail"] == f"The role with id {invalid_id} does not exist"


def test_team_memberships_post_fails_with_invalid_user(
    db_session, test_teams, default_team_roles, token_fixture
):
    invalid_id = "invalid_user_id"
    test_team1, test_team2 = test_teams
    member_role, admin_role = default_team_roles
    membership = TeamMembershipCreate(
        team_id=test_team1.public_id, user_id=invalid_id, role_id=member_role.public_id
    )
    response = client.post("/memberships/", json=membership.dict())

    json_response = response.json()
    assert response.status_code == 404
    assert json_response["detail"] == f"The user with id {invalid_id} does not exist"


def test_team_memberships_post_fails_with_invalid_team_id(
    db_session, test_users, default_team_roles, token_fixture
):
    invalid_id = "invalid_team_id"
    test_user1, test_user2 = test_users
    member_role, admin_role = default_team_roles
    membership = TeamMembershipCreate(
        team_id=invalid_id, user_id=test_user1.public_id, role_id=member_role.public_id
    )
    response = client.post("/memberships/", json=membership.dict())

    json_response = response.json()
    assert response.status_code == 404
    assert json_response["detail"] == f"The team with id {invalid_id} does not exist"


def test_team_memberships_post_fails_with_duplicate_entry(
    db_session, test_users, test_teams, default_team_roles, token_fixture
):
    # First Teams Request
    test_user1, test_user2 = test_users
    test_team1, test_team2 = test_teams
    member_role, admin_role = default_team_roles
    membership = TeamMembershipCreate(
        team_id=test_team1.public_id,
        user_id=test_user1.public_id,
        role_id=member_role.public_id,
    )
    response = client.post("/memberships/", json=membership.dict())

    json_response = response.json()

    assert response.status_code == 201
    assert json_response["team"]["public_id"] == test_team1.public_id
    assert json_response["role"]["public_id"] == member_role.public_id
    assert json_response["user"]["public_id"] == test_user1.public_id
    assert "public_id" in json_response

    # Duplicate Request
    response = client.post("/memberships/", json=membership.dict())

    json_response = response.json()

    assert response.status_code == 409
    assert (
        json_response["detail"]
        == "The user already has membership of that role within the team"
    )


def test_team_memberships_post_success_for_multiple_roles_within_a_team(
    db_session, test_users, test_teams, default_team_roles, token_fixture
):
    # Member Role Request
    test_user1, test_user2 = test_users
    test_team1, test_team2 = test_teams
    member_role, admin_role = default_team_roles
    membership = TeamMembershipCreate(
        team_id=test_team1.public_id,
        user_id=test_user1.public_id,
        role_id=member_role.public_id,
    )
    response = client.post("/memberships/", json=membership.dict())

    json_response = response.json()

    assert response.status_code == 201
    assert json_response["team"]["public_id"] == test_team1.public_id
    assert json_response["role"]["public_id"] == member_role.public_id
    assert json_response["user"]["public_id"] == test_user1.public_id
    assert "public_id" in json_response

    # Admin Role Request
    membership.role_id = admin_role.public_id
    response = client.post("/memberships/", json=membership.dict())

    json_response = response.json()

    assert response.status_code == 201
    assert json_response["team"]["public_id"] == test_team1.public_id
    assert json_response["role"]["public_id"] == admin_role.public_id
    assert json_response["user"]["public_id"] == test_user1.public_id
    assert "public_id" in json_response


def test_team_memberships_post_success_for_multiple_teams(
    db_session, test_users, test_teams, default_team_roles, token_fixture
):
    # Member Role Request
    test_user1, test_user2 = test_users
    test_team1, test_team2 = test_teams
    member_role, admin_role = default_team_roles
    membership = TeamMembershipCreate(
        team_id=test_team1.public_id,
        user_id=test_user1.public_id,
        role_id=member_role.public_id,
    )
    response = client.post("/memberships/", json=membership.dict())

    json_response = response.json()

    assert response.status_code == 201
    assert json_response["team"]["public_id"] == test_team1.public_id
    assert json_response["role"]["public_id"] == member_role.public_id
    assert json_response["user"]["public_id"] == test_user1.public_id
    assert "public_id" in json_response

    # Second Teams Request
    membership.team_id = test_team2.public_id
    response = client.post("/memberships/", json=membership.dict())

    json_response = response.json()

    assert response.status_code == 201
    assert json_response["team"]["public_id"] == test_team2.public_id
    assert json_response["role"]["public_id"] == member_role.public_id
    assert json_response["user"]["public_id"] == test_user1.public_id
    assert "public_id" in json_response


def test_team_memberships_get(
    db_session, test_users, test_teams, default_team_roles, token_fixture
):
    test_user1, test_user2 = test_users
    test_team1, test_team2 = test_teams
    member_role, admin_role = default_team_roles
    team_member1 = create_team_membership(
        db=db_session, team=test_team1, user=test_user1, role=member_role
    )
    team_member2 = create_team_membership(
        db=db_session, team=test_team1, user=test_user2, role=member_role
    )

    response = client.get(f"/memberships/?team_id={test_team1.public_id}")
    json_response = response.json()

    assert response.status_code == 200
    assert any(item["public_id"] == team_member1.public_id for item in json_response)
    assert any(item["public_id"] == team_member2.public_id for item in json_response)


def test_team_memberships_get_fails_with_invalid_team_id(db_session, token_fixture):
    invalid_id = "invalid_id"
    response = client.get(f"/memberships/?team_id={invalid_id}")
    json_response = response.json()

    assert response.status_code == 404
    assert json_response["detail"] == f"The team with id {invalid_id} does not exist"
