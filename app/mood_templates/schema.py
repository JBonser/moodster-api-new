"""
The schema module is responsible for defining the serialization models
for the mood template resource. It is used to provide validation of the data payloads
of the routes in the view module.
"""
from pydantic import BaseModel


class MoodTemplateCreate(BaseModel):
    name: str


class MoodTemplate(MoodTemplateCreate):
    public_id: str

    class Config:
        orm_mode = True
