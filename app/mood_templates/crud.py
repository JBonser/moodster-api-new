"""
This is the database access layer, all of the Create, Read Update Delete
functionality for mood templates go into this module.
"""
import uuid
from sqlalchemy.orm import Session

from app.mood_templates import model, schema


def get_all_mood_templates(db: Session):
    return db.query(model.MoodTemplate).all()


def create_mood_template(db: Session, template: schema.MoodTemplateCreate):
    mood_template = model.MoodTemplate(public_id=str(uuid.uuid4()), name=template.name)
    db.add(mood_template)
    db.commit()
    db.refresh(mood_template)
    return mood_template


def get_mood_template(db: Session, template_id):
    return db.query(model.MoodTemplate).filter_by(public_id=template_id).first()
