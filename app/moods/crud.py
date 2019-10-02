"""
This is the database access layer, all of the Create, Read Update Delete
functionality for mood templates go into this module.
"""
import uuid
from sqlalchemy.orm import Session

from app.moods import model
from app.mood_templates.crud import get_mood_template


def get_all_moods(db: Session, template_id: str = None):
    query = db.query(model.Mood)
    if template_id:
        template = get_mood_template(db, template_id)
        query = query.filter_by(template_id=template.id)
    return query.all()


def create_mood(db: Session, name: str, colour: str, template_id: str):
    template = get_mood_template(db, template_id)
    mood_model = model.Mood(
        public_id=str(uuid.uuid4()), name=name, colour=colour, template=template
    )
    db.add(mood_model)
    db.commit()
    db.refresh(mood_model)
    return mood_model


def get_mood(db: Session, mood_id: str):
    return db.query(model.Mood).filter_by(public_id=mood_id).first()
