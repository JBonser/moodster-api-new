"""
This module contains the password hashing functionality.
"""
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return crypt_context.verify(plain_password, hashed_password)


def generate_password_hash(password: str):
    return crypt_context.hash(password)
