"""
This view module is solely responsible for handling the routing of
the application. It is the entrypoint of any web request for the team membership
resource.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_409_CONFLICT

from app.exception import NoResourceWithIdError
from app.team_memberships import crud, schema
from app.users.model import User
from app.users.crud import get_user
from app.team_roles.crud import get_role
from app.teams.crud import get_team
from app.depends import get_db
from app.auth.depends import auth_required

router = APIRouter()


@router.post("/", response_model=schema.TeamMembership, status_code=201)
async def create_team_membership(
    team_membership: schema.TeamMembershipCreate,
    db: Session = Depends(get_db),
    auth_user: User = Depends(auth_required),
):
    user = get_user(db, team_membership.user_id)
    if not user:
        raise NoResourceWithIdError("user", team_membership.user_id)

    team = get_team(db=db, team_id=team_membership.team_id)
    if not team:
        raise NoResourceWithIdError("team", team_membership.team_id)

    role = get_role(db=db, role_id=team_membership.role_id)
    if not role:
        raise NoResourceWithIdError("role", team_membership.role_id)

    found = crud.membership_already_exists(db=db, user=user, team=team, role=role)
    if found:
        raise HTTPException(
            HTTP_409_CONFLICT,
            detail="The user already has membership of that role within the team",
        )

    return crud.create_team_membership(db=db, user=user, team=team, role=role)


@router.get("/", response_model=List[schema.TeamMembership])
async def get_all_memberships_for_team(
    team_id: str,
    db: Session = Depends(get_db),
    auth_user: User = Depends(auth_required),
):
    memberships = crud.get_all_memberships_for_team(db, team_id)
    if not memberships:
        raise NoResourceWithIdError("team", team_id)
    return memberships
