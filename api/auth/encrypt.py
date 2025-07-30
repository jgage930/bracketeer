import hashlib
from jose import jwt
import os


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def encode_token(username: str) -> str:
    return jwt.encode(
        {"username": username}, key=os.environ["SECRET_KEY"], algorithm="HS256"
    )


def decode_token(token: str) -> dict:
    return jwt.decode(token, os.environ["SECRET_KEY"], algorithms=["HS256"])
