from fastapi import APIRouter, Depends

from api.database import Database
from api.auth.schemas import UserRead, UserCreate
from api.auth.dependencies import unique_user
import api.auth.crud as crud

from api.utils import into_pydantic, into_pydantic_many


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("", response_model=UserRead)
async def register_new_user(db: Database, user: UserCreate = Depends(unique_user)):
    user = await crud.create_user(db, user)
    return into_pydantic(user, UserRead)


@user_router.get("", response_model=list[UserRead])
async def list_users(db: Database):
    users = await crud.get_all_users(db)
    return into_pydantic_many(users, UserRead)
