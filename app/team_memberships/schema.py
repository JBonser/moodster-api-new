"""
The schema module is responsible for defining the serialization models
for the team resource. It is used to provide validation of the data payloads
of the routes in the view module.
"""
from pydantic import BaseModel
from app.team_roles.schema import TeamRole
from app.teams.schema import Team
from app.users.schema import User


class TeamMembershipCreate(BaseModel):
    team_id: str
    user_id: str
    role_id: str


class TeamMembership(BaseModel):
    public_id: str
    team: Team
    user: User
    role: TeamRole

    class Config:
        orm_mode = True
