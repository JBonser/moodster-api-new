"""
This is a convenience module to allow importing all the database
models into alembic for the auto-generation of migrations.
"""
from app.database.base import Base  # noqa
from app.users.model import User  # noqa
