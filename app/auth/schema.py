"""
This module contains the authentication based schemas.
"""

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
