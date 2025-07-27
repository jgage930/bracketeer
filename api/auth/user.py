from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from api.auth.encrypt import hash_password
from api.database import Database, User
from api.utils import into_pydantic, into_pydantic_many


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


async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    return result.scalars().all()


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


@user_router.post("", response_model=UserRead)
async def register_new_user(db: Database, user: UserCreate = Depends(unique_user)):
    user = await create_user(db, user)
    return into_pydantic(user, UserRead)


@user_router.get("", response_model=list[UserRead])
async def list_users(db: Database):
    users = await get_all_users(db)
    return into_pydantic_many(users, UserRead)
