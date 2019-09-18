"""
The schema module is responsible for defining the serialization models
for the user resource. It is used to provide validation of the data payloads
of the routes in the view module.
"""
from pydantic import BaseModel, UUID4


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    public_id: UUID4

    class Config:
        orm_mode = True
