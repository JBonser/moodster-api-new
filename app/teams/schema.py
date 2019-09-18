"""
The schema module is responsible for defining the serialization models
for the team resource. It is used to provide validation of the data payloads
of the routes in the view module.
"""
from pydantic import BaseModel, UUID4


class TeamCreate(BaseModel):
    name: str


class Team(BaseModel):
    public_id: UUID4
    name: str

    class Config:
        orm_mode = True
