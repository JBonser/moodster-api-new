"""
The schema module is responsible for defining the serialization models
for the mood resource. It is used to provide validation of the data payloads
of the routes in the view module.
"""
from datetime import datetime
from pydantic import BaseModel
from pydantic.color import Color
from app.mood_templates.schema import MoodTemplate


class MoodCreate(BaseModel):
    name: str
    colour: Color
    template_id: str


class Mood(BaseModel):
    public_id: str
    name: str
    colour: Color
    template: MoodTemplate
    created_at: datetime

    class Config:
        orm_mode = True
