from fastapi import APIRouter, HTTPException, status

from api.database import Database
from api.suspension.schemas import SuspensionCreate, SuspensionRead
from api.suspension.crud import (
    create_suspension,
    get_suspension_by_id,
    list_all_suspension,
    delete_suspension,
)


suspension_router = APIRouter(prefix="/suspension", tags=["suspension"])


@suspension_router.post("")
async def create_new_suspension(suspension: SuspensionCreate, db: Database):
    suspension = await create_suspension(db, suspension)
    return SuspensionRead.model_validate(suspension)


@suspension_router.get("")
async def read_all_suspensions(db: Database):
    suspensions = await list_all_suspension(db)
    print(suspensions)
    return [SuspensionRead.model_validate(s) for s in suspensions]


@suspension_router.get("/{id}")
async def read_suspension_by_id(id: int, db: Database):
    suspension = await get_suspension_by_id(db, id)
    if not suspension:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No suspension found with id {id}",
        )

    return SuspensionRead.model_validate(suspension)


@suspension_router.delete("/{id}")
async def delete_suspension_by_id(id: int, db: Database):
    success = await delete_suspension(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No suspension found with id {id}",
        )

    return {"msg": f"Deleted suspension {id}"}
