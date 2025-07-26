from fastapi import APIRouter
from pydantic import BaseModel

from api.database import Database


user_router = APIRouter(prefix="user", tags=["user"])


class RegisterUser(BaseModel):
    username: str
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    access_level: str

    class Config:
        orm_mode = True


@user_router.post("/register")
async def register_new_user(user: RegisterUser, db: Database):
    pass
