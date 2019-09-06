"""
This module is used for describing application wide request dependencies.
This covers things such as the database session which is required by most
routes.
"""
from starlette.requests import Request


def get_db(request: Request):
    return request.state.db
