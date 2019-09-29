"""
This module defines the actual database ORM model of the MoodTemplate resource.
It is the representation that is used to describe how the database schema
will look.
"""
from sqlalchemy import Column, Integer, String

from app.database.base import Base


class MoodTemplate(Base):
    """ Mood Template Model for storing types of mood templates"""

    __tablename__ = "mood_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} ("
            f"public_id={self.public_id}, "
            f"name={self.name} )>"
        )
