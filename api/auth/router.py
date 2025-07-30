from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from api.auth.encrypt import hash_password, encode_token, decode_token
from api.auth.user import get_user_by_username
from api.database import Database
from api.utils import into_pydantic


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
auth_router = APIRouter(tags=["auth"])


class CurrentUser(BaseModel):
    id: int
    email: str
    username: str


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Database):
    token = decode_token(token)
    user = await get_user_by_username(db, token["username"])

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return into_pydantic(user, CurrentUser)


@auth_router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Database
):
    user = await get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="User name not found.")

    hashed_password = hash_password(form_data.password)
    if not hashed_password == user.password_hash:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = encode_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@auth_router.get("/users/me")
async def read_users_me(
    current_user: Annotated[dict, Depends(get_current_user)],
):
    return current_user
