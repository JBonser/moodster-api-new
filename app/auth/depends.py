"""
This module is used for describing authentication based request dependencies.
This cover behaviour of how routes should act under different levels of
authentication/authorisation.
"""
import jwt
from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.logic import oauth2_scheme
from app.config import SECRET_KEY, HASH_ALGORITHM
from app.auth.exception import UnauthorisedTokenException
from app.users.crud import get_user_by_id
from app.depends import get_db


async def auth_required(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise UnauthorisedTokenException()
    except jwt.PyJWTError:
        raise UnauthorisedTokenException()
    user = get_user_by_id(db, user_id)
    if user is None:
        raise UnauthorisedTokenException()
    return user
