"""
This view module is solely responsible for handling the routing of
the application. It is the entrypoint of any web request for the team
role resource.
"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.team_roles import crud, schema
from app.depends import get_db

router = APIRouter()


@router.get("/", response_model=List[schema.TeamRole])
async def get_all_team_roles(db: Session = Depends(get_db)):
    return crud.get_all_team_roles(db)
