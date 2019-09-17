"""
This is the database access layer, all of the Create, Read Update Delete
functionality for teams goes into this module.
"""
import uuid
from sqlalchemy.orm import Session

from app.teams import model, schema


def get_team(db: Session, team_id: str):
    return db.query(model.Team).filter(model.Team.public_id == team_id).first()


def create_team(db: Session, team: schema.TeamCreate):
    team = model.Team(public_id=str(uuid.uuid4()), name=team.name)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team
