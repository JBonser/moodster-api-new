"""
Exceptions for common authentication errors.
"""

from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from fastapi import HTTPException


class InvalidLoginException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Could not validate email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UnauthorisedTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
