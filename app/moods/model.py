"""
This module defines the actual database ORM model of the Mood resource.
It is the representation that is used to describe how the database schema
will look.
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.database.base import Base


class Mood(Base):
    """ Mood Model for storing types of moods"""

    __tablename__ = "moods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    colour = Column(String(50), nullable=False)
    template_id = Column(Integer, ForeignKey("mood_templates.id"), nullable=False)
    template = relationship(
        "MoodTemplate", backref=backref("moods", cascade="delete, delete-orphan")
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} ("
            f"public_id={self.public_id}, "
            f"name={self.name}, "
            f"colour={self.colour}, "
            f"template_id={self.template_id}) >"
        )
