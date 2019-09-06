"""
This module contains the business level logic for authentication. It is used
to ensure that the view module can be responsbile solely for routing.
"""
import jwt
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.users.crud import get_user_by_email
from app.config import SECRET_KEY, HASH_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINS
from app.auth.hash import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return create_access_token(user.id)


def create_access_token(user_id: str):
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)
    data = {"sub": user_id, "exp": expires}
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=HASH_ALGORITHM)
    return encoded_jwt.decode("ascii")
