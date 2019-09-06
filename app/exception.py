"""
Exceptions for common errors.
"""

from starlette.status import HTTP_400_BAD_REQUEST
from fastapi import HTTPException


class DuplicateResourceError(HTTPException):
    def __init__(self, resource, value):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"{resource} with this {value} already exists",
        )
