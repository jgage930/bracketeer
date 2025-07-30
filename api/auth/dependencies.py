from fastapi import HTTPException, status, Depends
from typing import Annotated

from api.auth.router import oauth2_scheme
from api.auth.schemas import UserCreate
from sqlalchemy import select
from api.database import Database
from api.auth.models import User
from api.auth.schemas import UserRead
from api.auth.encrypt import decode_token
from api.utils import into_pydantic
from api.auth.crud import get_user_by_username


async def unique_user(user: UserCreate, db: Database) -> UserCreate:
    """
    Dependency to make sure user being created is unique.

    Raises:
        Http 409 error if user with user name or email already exists.
    """
    result = await db.execute(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=409, detail="User with this username or email already exists."
        )

    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Database):
    token = decode_token(token)
    user = await get_user_by_username(db, token["username"])

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return into_pydantic(user, UserRead)
