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
    db_session, test_users, test_teams, default_team_roles
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
    db_session, test_users, test_teams
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


# def test_team_memberships_post_fails_with_invalid_user(self):
#     invalid_id = "invalid_user_id"
#     response = self.send_team_memberships_post(
#         self.test_team1.public_id, self.member_role.public_id, invalid_id
#     )

#     json_response = response.get_json()

#     self.assertEqual(response.status_code, 404)
#     self.assertEqual(json_response["status"], "Failed")
#     self.assertEqual(
#         json_response["message"], f"User with id {invalid_id} does not exist"
#     )


# def test_team_memberships_post_fails_with_invalid_team_url(self):
#     invalid_id = "invalid_team_url"
#     response = self.send_team_memberships_post(
#         invalid_id, self.member_role.public_id, self.test_user1.public_id
#     )

#     json_response = response.get_json()

#     self.assertEqual(response.status_code, 404)
#     self.assertEqual(json_response["status"], "Failed")
#     self.assertEqual(
#         json_response["message"], f"Team with id {invalid_id} does not exist"
#     )


# def test_team_memberships_post_fails_with_duplicate_entry(self):
#     # First Teams Request
#     response = self.send_team_memberships_post(
#         self.test_team1.public_id, self.member_role.public_id, self.test_user1.public_id
#     )

#     json_response = response.get_json()

#     self.assertEqual(response.status_code, 201)
#     self.assertIn("id", json_response)
#     self.assertEqual(json_response["team_id"], self.test_team1.public_id)
#     self.assertEqual(json_response["team_role_id"], self.member_role.public_id)
#     self.assertEqual(json_response["user_id"], self.test_user1.public_id)

#     # Duplicate Request
#     response = self.send_team_memberships_post(
#         self.test_team1.public_id, self.member_role.public_id, self.test_user1.public_id
#     )

#     json_response = response.get_json()

#     self.assertEqual(response.status_code, 409)
#     self.assertEqual(json_response["status"], "Failed")
#     self.assertEqual(
#         json_response["message"],
#         "The user already has membership of that role within the team",
#     )


# def test_team_memberships_post_success_for_multiple_roles_within_a_team(self):
#     # Member Role Request
#     response = self.send_team_memberships_post(
#         self.test_team1.public_id, self.member_role.public_id, self.test_user1.public_id
#     )

#     json_response = response.get_json()

#     self.assertEqual(response.status_code, 201)
#     self.assertIn("id", json_response)
#     self.assertEqual(json_response["team_id"], self.test_team1.public_id)
#     self.assertEqual(json_response["team_role_id"], self.member_role.public_id)
#     self.assertEqual(json_response["user_id"], self.test_user1.public_id)

#     # Admin Role Request
#     response = self.send_team_memberships_post(
#         self.test_team1.public_id, self.admin_role.public_id, self.test_user1.public_id
#     )

#     json_response = response.get_json()

#     self.assertEqual(response.status_code, 201)
#     self.assertIn("id", json_response)
#     self.assertEqual(json_response["team_id"], self.test_team1.public_id)
#     self.assertEqual(json_response["team_role_id"], self.admin_role.public_id)
#     self.assertEqual(json_response["user_id"], self.test_user1.public_id)


# def test_team_memberships_post_success_for_multiple_teams(self):
#     # First Teams Request
#     response = self.send_team_memberships_post(
#         self.test_team1.public_id, self.member_role.public_id, self.test_user1.public_id
#     )

#     json_response = response.get_json()

#     self.assertEqual(response.status_code, 201)
#     self.assertIn("id", json_response)
#     self.assertEqual(json_response["team_id"], self.test_team1.public_id)
#     self.assertEqual(json_response["team_role_id"], self.member_role.public_id)
#     self.assertEqual(json_response["user_id"], self.test_user1.public_id)

#     # Second Teams Request
#     response = self.send_team_memberships_post(
#         self.test_team2.public_id, self.member_role.public_id, self.test_user1.public_id
#     )

#     json_response = response.get_json()

#     self.assertEqual(response.status_code, 201)
#     self.assertIn("id", json_response)
#     self.assertEqual(json_response["team_id"], self.test_team2.public_id)
#     self.assertEqual(json_response["team_role_id"], self.member_role.public_id)
#     self.assertEqual(json_response["user_id"], self.test_user1.public_id)


# def test_team_memberships_get(self):
#     team_member1 = create_membership_in_db(
#         self.test_team1, self.test_user1, self.member_role
#     )
#     team_member2 = create_membership_in_db(
#         self.test_team1, self.test_user2, self.member_role
#     )

#     response = self.client.get(f"/teams/{self.test_team1.public_id}/memberships/")
#     data = response.get_json()["data"]

#     self.assertEqual(response.status_code, 200)
#     self.assertTrue(any(item["id"] == team_member1.public_id for item in data))
#     self.assertTrue(any(item["id"] == team_member2.public_id for item in data))


# def test_team_memberships_get_fails_with_invalid_team_id(self):
#     team_id = "invalid-team-id"
#     response = self.client.get(f"/teams/{team_id}/memberships/")

#     json_response = response.get_json()
#     self.assertEqual(response.status_code, 404)
#     self.assertEqual(json_response["status"], "Failed")
#     self.assertEqual(
#         json_response["message"], f"The team with id {team_id} does not exist"
#     )


# def send_team_memberships_post(self, team_id, role_id, user_id):
#     team_member = {"user_id": user_id, "team_role_id": role_id}
#     return self.client.post(f"/teams/{team_id}/memberships/", json=team_member)
