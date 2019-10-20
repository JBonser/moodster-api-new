"""
The schema module is responsible for defining the serialization models
for the team resource. It is used to provide validation of the data payloads
of the routes in the view module.
"""
from pydantic import BaseModel
from app.moods.schema import Mood
from app.teams.schema import Team


class TeamMemberMoodCreate(BaseModel):
    team_id: str
    mood_id: str


class TeamMemberMood(BaseModel):
    public_id: str
    team: Team
    mood: Mood

    class Config:
        orm_mode = True
