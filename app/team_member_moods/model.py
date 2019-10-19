"""
This module defines the actual database ORM model of the Team Member Mood resource.
It is the representation that is used to describe how the database schema
will look.
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.database.base import Base


class TeamMemberMoods(Base):
    """ Team Member Mood Model for storing member mood information """

    __tablename__ = "team_member_moods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String(100), unique=True, nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    team = relationship(
        "Team", backref=backref("team_member_moods", cascade="delete, delete-orphan")
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship(
        "User", backref=backref("team_member_moods", cascade="delete, delete-orphan")
    )
    mood_id = Column(Integer, ForeignKey("moods.id"), nullable=False)
    mood = relationship(
        "Mood", backref=backref("team_member_moods", cascade="delete, delete-orphan")
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} ("
            f"team_id={self.team_id}, "
            f"user_id={self.user_id}, "
            f"role_id={self.mood_id}) >"
        )
