"""
The schema module is responsible for defining the serialization models
for the team role resource. It is used to provide validation of the data payloads
of the routes in the view module.
"""
from pydantic import BaseModel


class TeamRoleCreate(BaseModel):
    name: str


class TeamRole(BaseModel):
    public_id: str
    name: str

    class Config:
        orm_mode = True
