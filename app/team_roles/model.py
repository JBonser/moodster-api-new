"""
This module defines the actual database ORM model of the Team Role resource.
It is the representation that is used to describe how the database schema
will look.
"""
from sqlalchemy import Column, Integer, String

from app.database.base import Base


class TeamRole(Base):
    """ Team Role Model for storing team role details """

    __tablename__ = "team_roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String(100), unique=True)
    name = Column(String(30), nullable=False)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} ("
            f"public_id={self.public_id}, "
            f"name={self.name}, "
        )
