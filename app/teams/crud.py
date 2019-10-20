"""
This is the database access layer, all of the Create, Read Update Delete
functionality for teams goes into this module.
"""
import uuid
from sqlalchemy.orm import Session

from app.teams import model, schema
from app.users.model import User
from app.team_memberships.crud import create_team_membership
from app.team_roles.crud import get_role_by_name
from app.team_roles.role_constants import ADMIN_ROLE_NAME


def get_team(db: Session, team_id: str):
    return db.query(model.Team).filter(model.Team.public_id == team_id).first()


def create_team(db: Session, team: schema.TeamCreate, user: User):
    role = get_role_by_name(db=db, role_name=ADMIN_ROLE_NAME)
    team = model.Team(public_id=str(uuid.uuid4()), name=team.name)
    db.add(team)
    db.commit()
    db.refresh(team)
    db.refresh(user)
    # Add the authenticated user as the first admin member of the team.
    create_team_membership(db=db, user=user, team=team, role=role)
    return team
