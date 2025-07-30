from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.auth.encrypt import hash_password, encode_token
from api.database import Database
from api.auth.crud import get_user_by_username


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
auth_router = APIRouter(tags=["auth"])


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
