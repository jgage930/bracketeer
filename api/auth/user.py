from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from api.auth.encrypt import hash_password
from api.database import Database, User
from api.utils import into_pydantic


user_router = APIRouter(prefix="/user", tags=["user"])


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    access_level_id: int

    class Config:
        orm_mode = True
        from_attributes = True


# CRUD
async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        access_level_id=1,
    )

    db.add(user)
    await db.flush()
    return user


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


@user_router.post("", response_model=UserRead)
async def register_new_user(user: UserCreate, db: Database):
    user = await create_user(db, user)
    return into_pydantic(user, UserRead)
