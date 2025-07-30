from fastapi import APIRouter, HTTPException

from api.database import Database
from api.auth.schemas import AccessLevelCreate, AccessLevelRead
import api.auth.crud as crud


access_router = APIRouter(prefix="/access", tags=["access"])


@access_router.post("")
async def create_access(access: AccessLevelCreate, db: Database):
    return await crud.create_access_level(db, access)


@access_router.get("/{id}", response_model=AccessLevelRead)
async def get_access_by_id(id: int, db: Database):
    access = await crud.get_access_level(db, id)
    if not access:
        raise HTTPException(status_code=404, detail="Access level not found")
    return access


@access_router.get("/", response_model=list[AccessLevelRead])
async def list_all_accesses(db: Database):
    return await crud.get_all_access_levels(db)


@access_router.delete("/{id}")
async def delete_access(id: int, db: Database):
    success = await crud.delete_access_level(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Access level not found")
