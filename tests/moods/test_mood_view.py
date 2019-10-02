"""
Test module for the moods resource/endpoint.
"""
from starlette.testclient import TestClient
from fastapi.encoders import jsonable_encoder
import pytest
from app.main import app
from app.mood_templates.crud import create_mood_template
from app.mood_templates.schema import MoodTemplateCreate
from app.moods.crud import create_mood
from app.moods.schema import MoodCreate

client = TestClient(app)


@pytest.fixture()
def test_mood_templates(db_session):
    test_template1 = MoodTemplateCreate(name="test_mood_template")
    test_template2 = MoodTemplateCreate(name="test_mood_template2")
    mood_template1 = create_mood_template(db_session, test_template1)
    mood_template2 = create_mood_template(db_session, test_template2)
    return mood_template1, mood_template2


@pytest.fixture()
def test_mood_create(test_mood_templates):
    template1, template2 = test_mood_templates
    test_mood1 = MoodCreate(
        name="mood1", colour="blue", template_id=template1.public_id
    )
    test_mood2 = MoodCreate(name="mood2", colour="red", template_id=template2.public_id)
    return test_mood1, test_mood2


def test_mood_get_success(db_session, test_mood_create):
    mood_create, _ = test_mood_create
    mood = create_mood(
        db_session,
        mood_create.name,
        mood_create.colour.as_hex(),
        mood_create.template_id,
    )

    response = client.get(f"/moods/{mood.public_id}")
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["name"] == mood.name
    assert json_response["public_id"] == mood.public_id
    assert json_response["colour"] == mood_create.colour.as_named()


def test_mood_get_fails_with_invalid_id(db_session, test_mood_create):
    invalid_id = "invalid_id"
    mood_create, _ = test_mood_create
    create_mood(
        db_session,
        mood_create.name,
        mood_create.colour.as_hex(),
        mood_create.template_id,
    )

    response = client.get(f"/moods/{invalid_id}")
    json_response = response.json()

    assert response.status_code == 404
    assert json_response["detail"] == f"The mood with id {invalid_id} does not exist"


def test_mood_creation_success(db_session, test_mood_create):
    mood_create, _ = test_mood_create
    response = client.post("/moods/", json=jsonable_encoder(mood_create))
    json_response = response.json()

    assert response.status_code == 201
    assert json_response["name"] == mood_create.name
    assert json_response["colour"] == mood_create.colour.as_named()
    assert json_response["template"]["public_id"] == mood_create.template_id
    assert "public_id" in json_response


def test_mood_get_all_success(db_session, test_mood_create):
    mood_create1, mood_create2 = test_mood_create
    mood1 = create_mood(
        db_session,
        mood_create1.name,
        mood_create1.colour.as_hex(),
        mood_create1.template_id,
    )
    mood2 = create_mood(
        db_session,
        mood_create2.name,
        mood_create2.colour.as_hex(),
        mood_create2.template_id,
    )

    response = client.get("/moods")

    assert response.status_code == 200
    json_response = jsonable_encoder(response.json())

    response_mood1 = next(
        mood for mood in json_response if mood["public_id"] == mood1.public_id
    )
    response_mood2 = next(
        mood for mood in json_response if mood["public_id"] == mood2.public_id
    )

    # Check they both exist
    assert response_mood1
    assert response_mood2

    # Check mood1 data is correct
    assert response_mood1["public_id"] == mood1.public_id
    assert response_mood1["name"] == mood_create1.name
    assert response_mood1["colour"] == mood_create1.colour.as_named()

    # Check mood2 data is correct
    assert response_mood2["public_id"] == mood2.public_id
    assert response_mood2["name"] == mood_create2.name
    assert response_mood2["colour"] == mood_create2.colour.as_named()


def test_mood_get_all_with_template_id_success(db_session, test_mood_create):
    mood_create1, mood_create2 = test_mood_create
    mood1 = create_mood(
        db_session,
        mood_create1.name,
        mood_create1.colour.as_hex(),
        mood_create1.template_id,
    )
    mood2 = create_mood(
        db_session,
        mood_create2.name,
        mood_create2.colour.as_hex(),
        mood_create2.template_id,
    )
    response = client.get(f"/moods/?template_id={mood_create1.template_id}")

    assert response.status_code == 200
    json_response = jsonable_encoder(response.json())

    response_mood1 = next(
        mood for mood in json_response if mood["public_id"] == mood1.public_id
    )
    # Shouldn't be able to find mood2
    with pytest.raises(StopIteration):
        next(mood for mood in json_response if mood["public_id"] == mood2.public_id)

    # Check they both exist
    assert response_mood1

    # Check mood1 data is correct
    assert response_mood1["public_id"] == mood1.public_id
    assert response_mood1["name"] == mood_create1.name
    assert response_mood1["colour"] == mood_create1.colour.as_named()


def test_mood_get_all_with_invalid_template_id_fails(db_session, test_mood_create):
    invalid_id = "invalid-id"
    response = client.get(f"/moods/?template_id={invalid_id}")
    json_response = response.json()
    assert response.status_code == 404
    assert (
        json_response["detail"]
        == f"The mood_template with id {invalid_id} does not exist"
    )
