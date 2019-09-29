"""
This view module is solely responsible for handling the routing of
the application. It is the entrypoint of any web request for the mood
template resource.
"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.mood_templates import crud, schema
from app.depends import get_db
from app.exception import NoResourceWithIdError

router = APIRouter()


@router.get("/", response_model=List[schema.MoodTemplate])
async def get_all_mood_templates(db: Session = Depends(get_db)):
    return crud.get_all_mood_templates(db)


@router.post("/", response_model=schema.MoodTemplate)
async def create_mood_template(
    template: schema.MoodTemplate, db: Session = Depends(get_db)
):
    return crud.create_mood_template(db, template)


@router.get("/{template_id}", response_model=schema.MoodTemplate)
async def get_mood_template(template_id: str, db: Session = Depends(get_db)):
    template = crud.get_mood_template(db, template_id)
    if not template:
        raise NoResourceWithIdError("mood_template", template_id)
    return template
