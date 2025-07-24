from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from api.database import AccessLevel, db_session


access_router = APIRouter(prefix="/access", tags=["access"])


class AccessLevelCreate(BaseModel):
    name: str


class AccessLevelRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


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


@access_router.post("")
async def create_access(
    access: AccessLevelCreate, db: AsyncSession = Depends(db_session)
):
    return await create_access_level(db, access)


@access_router.get("/{id}", response_model=AccessLevelRead)
async def get_access_by_id(id: int, db: AsyncSession = Depends(db_session)):
    access = await get_access_level(db, id)
    if not access:
        raise HTTPException(status_code=404, detail="Access level not found")
    return access


@access_router.get("/", response_model=list[AccessLevelRead])
async def list_all_accesses(db: AsyncSession = Depends(db_session)):
    return await get_all_access_levels(db)


@access_router.delete("/{id}")
async def delete_access(id: int, db: AsyncSession = Depends(db_session)):
    success = await delete_access_level(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Access level not found")
