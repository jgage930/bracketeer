from api.auth.models import AccessLevel, User
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from api.auth.schemas import AccessLevelCreate, UserCreate
from api.auth.encrypt import hash_password


async def create_access_level(
    db: AsyncSession, access_data: AccessLevelCreate
) -> AccessLevel:
    access_level = AccessLevel(name=access_data.name)
    db.add(access_level)
    await db.flush()
    return access_level


async def get_access_level(
    db: AsyncSession, access_level_id: int
) -> AccessLevel | None:
    result = await db.execute(
        select(AccessLevel).where(AccessLevel.id == access_level_id)
    )
    return result.scalar_one_or_none()


async def get_all_access_levels(db: AsyncSession) -> list[AccessLevel]:
    result = await db.execute(select(AccessLevel))
    return result.scalars().all()


async def delete_access_level(db: AsyncSession, access_level_id: int) -> bool:
    access_level = await get_access_level(db, access_level_id)
    if access_level is None:
        return False
    await db.delete(access_level)
    return True


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


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    return result.scalars().all()
