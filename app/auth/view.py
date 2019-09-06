"""
This view module is solely responsible for handling the routing of
the application. It is the entrypoint of any web request related to authentication
"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.exception import InvalidLoginException
from app.auth.logic import authenticate_user
from app.depends import get_db
from app.auth.schema import Token


router = APIRouter()


@router.post("/", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    token = authenticate_user(db, form_data.username, form_data.password)
    if not token:
        raise InvalidLoginException()
    return {"access_token": token, "token_type": "bearer"}
