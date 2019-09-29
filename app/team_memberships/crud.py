"""
This is the database access layer, all of the Create, Read Update Delete
functionality for team memberships goes into this module.
"""
import uuid
from sqlalchemy.orm import Session

from app.teams.model import Team
from app.users.model import User
from app.team_roles.model import TeamRole
from app.team_memberships import model


def get_all_memberships_for_team(db: Session, team_id: str):
    team = db.query(Team).filter(Team.public_id == team_id).first()
    if not team:
        return None
    return db.query(model.Membership).filter_by(team=team).all()


def create_team_membership(db: Session, user: User, team: Team, role: TeamRole):
    membership = model.Membership(
        public_id=str(uuid.uuid4()), team=team, user=user, role=role
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


def membership_already_exists(db: Session, user, team, role):
    membership = (
        db.query(model.Membership).filter_by(team=team, user=user, role=role).first()
    )
    return membership is not None
