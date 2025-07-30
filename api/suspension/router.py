from fastapi import APIRouter

from api.database import Database
from api.suspension.schemas import SuspensionCreate, SuspensionRead
from api.suspension.crud import create_suspension
from api.utils import into_pydantic


suspension_router = APIRouter(prefix="/suspension", tags=["suspension"])


@suspension_router.post("", response_model=SuspensionRead)
async def create_new_suspension(suspension: SuspensionCreate, db: Database):
    suspension = await create_suspension(db, suspension)
    return into_pydantic(suspension, SuspensionRead)
