"""
This view module is solely responsible for handling the routing of
the application. It is the entrypoint of any web request for the team
resource.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.exception import NoResourceWithIdError
from app.teams import crud, schema
from app.users.model import User
from app.depends import get_db
from app.auth.depends import auth_required

router = APIRouter()


@router.post("/", response_model=schema.Team, status_code=201)
async def create_team(team: schema.TeamCreate, db: Session = Depends(get_db)):
    return crud.create_team(db=db, team=team)


@router.get("/{team_id}", response_model=schema.Team)
async def get_team(
    team_id: str, db: Session = Depends(get_db), user: User = Depends(auth_required)
):
    team = crud.get_team(db, team_id)
    if not team:
        raise NoResourceWithIdError("team", team_id)
    return team
