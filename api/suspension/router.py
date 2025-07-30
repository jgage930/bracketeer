from fastapi import APIRouter

from api.database import Database
from api.suspension.schemas import SuspensionCreate, SuspensionRead
from api.suspension.crud import create_suspension


suspension_router = APIRouter(prefix="/suspension", tags=["suspension"])


@suspension_router.post("")
async def create_new_suspension(suspension: SuspensionCreate, db: Database):
    suspension = await create_suspension(db, suspension)
    return SuspensionRead.model_validate(suspension)
