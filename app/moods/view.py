"""
This view module is solely responsible for handling the routing of
the application. It is the entrypoint of any web request for the mood
resource.
"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.moods import crud, schema
from app.mood_templates.crud import get_mood_template
from app.depends import get_db
from app.exception import NoResourceWithIdError

router = APIRouter()


@router.post("/", response_model=schema.Mood, status_code=201)
async def create_mood(mood: schema.MoodCreate, db: Session = Depends(get_db)):
    template = get_mood_template(db, mood.template_id)
    if not template:
        raise NoResourceWithIdError("mood_template", mood.template_id)
    return crud.create_mood(db, mood.name, mood.colour.as_hex(), mood.template_id)


@router.get("/{mood_id}", response_model=schema.Mood)
async def get_mood(mood_id: str, db: Session = Depends(get_db)):
    mood = crud.get_mood(db, mood_id)
    if not mood:
        raise NoResourceWithIdError("mood", mood_id)
    return mood


@router.get("/", response_model=List[schema.Mood])
async def get_all_moods(template_id: str = None, db: Session = Depends(get_db)):
    if template_id:
        template = get_mood_template(db, template_id)
        if not template:
            raise NoResourceWithIdError("mood_template", template_id)
    return crud.get_all_moods(db, template_id)
