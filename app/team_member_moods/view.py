"""
This view module is solely responsible for handling the routing of
the application. It is the entrypoint of any web request for the team member moods
resource.
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.exception import NoResourceWithIdError
from app.team_member_moods import crud, schema
from app.users.model import User
from app.moods.crud import get_mood
from app.teams.crud import get_team
from app.depends import get_db
from app.auth.depends import auth_required

router = APIRouter()


@router.post("/", response_model=schema.TeamMemberMood, status_code=201)
async def create_member_mood(
    team_member_mood: schema.TeamMemberMoodCreate,
    db: Session = Depends(get_db),
    auth_user: User = Depends(auth_required),
):
    team = get_team(db=db, team_id=team_member_mood.team_id)
    if not team:
        raise NoResourceWithIdError("team", team_member_mood.team_id)

    mood = get_mood(db=db, mood_id=team_member_mood.mood_id)
    if not mood:
        raise NoResourceWithIdError("mood", team_member_mood.mood_id)

    return crud.create_team_member_mood(db=db, user=auth_user, team=team, mood=mood)


@router.get("/", response_model=List[schema.TeamMemberMood])
async def get_all_member_moods_for_team(
    team_id: str,
    db: Session = Depends(get_db),
    auth_user: User = Depends(auth_required),
):
    team = get_team(db=db, team_id=team_id)
    if not team:
        raise NoResourceWithIdError("team", team_id)

    member_moods = crud.get_all_member_moods_for_team(db=db, team=team)
    return member_moods
