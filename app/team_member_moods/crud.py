"""
This is the database access layer, all of the Create, Read Update Delete
functionality for team memberships goes into this module.
"""
import uuid
from sqlalchemy.orm import Session

from app.teams.model import Team
from app.users.model import User
from app.moods.model import Mood
from app.team_member_moods import model


def get_all_member_moods_for_team(db: Session, team: Team):
    return db.query(model.TeamMemberMoods).filter_by(team=team).all()


def create_team_member_mood(db: Session, user: User, team: Team, mood: Mood):
    member_mood = model.TeamMemberMoods(
        public_id=str(uuid.uuid4()), team=team, user=user, mood=mood
    )

    db.add(member_mood)
    db.commit()
    db.refresh(member_mood)
    return member_mood
