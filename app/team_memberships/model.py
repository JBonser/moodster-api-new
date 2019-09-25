"""
This module defines the actual database ORM model of the Team Membership resource.
It is the representation that is used to describe how the database schema
will look.
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.database.base import Base


class Membership(Base):
    """ Membership Model for storing team membership information """

    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String(100), unique=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship(
        "Team", backref=backref("memberships", cascade="delete, delete-orphan")
    )
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(
        "User", backref=backref("memberships", cascade="delete, delete-orphan")
    )
    role_id = Column(Integer, ForeignKey("team_roles.id"))
    role = relationship(
        "TeamRole", backref=backref("memberships", cascade="delete, delete-orphan")
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} ("
            f"team_id={self.team_id}, "
            f"user_id={self.user_id}, "
            f"role_id={self.role_id}) >"
        )
