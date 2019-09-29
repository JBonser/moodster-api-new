"""
Test module for the team membership resource/endpoint.
"""
from starlette.testclient import TestClient
import pytest
from app.main import app
from app.mood_templates.schema import MoodTemplateCreate
from app.mood_templates.crud import create_mood_template

client = TestClient(app)


@pytest.fixture()
def test_mood_templates(db_session):
    test_template1 = MoodTemplateCreate(name="test_mood_template")
    test_template2 = MoodTemplateCreate(name="test_mood_template2")
    return test_template1, test_template2


def test_mood_template_creation(db_session, test_mood_templates):
    test_template, _ = test_mood_templates
    response = client.post("/mood_templates/", json=test_template.dict())
    print(response)
    json_response = response.json()
    print(json_response)
    assert response.status_code == 201
    assert json_response["name"] == test_template.name
    assert "public_id" in json_response


def test_mood_template_creation_fails_with_duplicate_name(
    db_session, test_mood_templates
):
    test_template, _ = test_mood_templates
    # First Request
    response = client.post("/mood_templates/", json=test_template.dict())
    json_response = response.json()

    assert response.status_code == 201
    assert json_response["name"] == test_template.name
    assert "public_id" in json_response

    # Duplicate Request
    response = client.post("/mood_templates/", json=test_template.dict())
    json_response = response.json()

    assert response.status_code == 400
    assert "mood_template with this name already exists" in json_response["detail"]


def test_mood_template_get_all_succeeds(db_session, test_mood_templates):
    test_template1, test_template2 = test_mood_templates
    mood_template1 = create_mood_template(db_session, test_template1)
    mood_template2 = create_mood_template(db_session, test_template2)

    response = client.get("/mood_templates/")
    json_response = response.json()

    assert response.status_code == 200
    assert any(item["public_id"] == mood_template1.public_id for item in json_response)
    assert any(item["public_id"] == mood_template2.public_id for item in json_response)


def test_mood_template_get_succeeds(db_session, test_mood_templates):
    test_template, _ = test_mood_templates
    mood_template = create_mood_template(db_session, test_template)
    response = client.get(f"/mood_templates/{mood_template.public_id}")
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["name"] == mood_template.name
    assert json_response["public_id"] == mood_template.public_id


def test_mood_template_get_fails_with_invalid_id(db_session):
    invalid_id = "invalid_id"
    response = client.get(f"/mood_templates/{invalid_id}")
    json_response = response.json()
    assert response.status_code == 404
    assert (
        json_response["detail"]
        == f"The mood_template with id {invalid_id} does not exist"
    )
