"""
This is the database access layer, all of the Create, Read Update Delete
functionality for team roles goes into this module.
"""
import uuid
from sqlalchemy.orm import Session

from app.team_roles import model, schema


def get_all_team_roles(db: Session):
    return db.query(model.TeamRole).all()


def create_team_role(db: Session, team_role: schema.TeamRoleCreate):
    team_role = model.TeamRole(public_id=str(uuid.uuid4()), name=team_role.name)
    db.add(team_role)
    db.commit()
    db.refresh(team_role)
    return team_role


def get_role(db: Session, role_id: str):
    return db.query(model.TeamRole).filter_by(public_id=role_id).first()


def get_role_by_name(db: Session, role_name: str):
    return db.query(model.TeamRole).filter_by(name=role_name).first()
