"""
This is a convenience module to allow importing all the database
models into alembic for the auto-generation of migrations.
"""
from app.database.base import Base  # noqa
from app.users.model import User  # noqa
from app.teams.model import Team  # noqa
from app.team_roles.model import TeamRole  # noqa
from app.team_memberships.model import Membership  # noqa
from app.mood_templates.model import MoodTemplate  # noqa
