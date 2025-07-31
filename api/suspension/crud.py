from sqlalchemy.orm import selectinload
from api.suspension.models import Suspension, SuspensionField
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from api.suspension.schemas import SuspensionCreate


async def create_suspension(
    db: AsyncSession, suspension_data: SuspensionCreate
) -> Suspension:
    suspension = Suspension(
        name=suspension_data.name,
        type=suspension_data.type.value,
        fields=[
            SuspensionField(**field.model_dump()) for field in suspension_data.fields
        ],
    )

    db.add(suspension)
    await db.flush()

    return suspension


async def get_suspension_by_id(
    db: AsyncSession, suspension_id: int
) -> Suspension | None:
    result = await db.execute(select(Suspension).where(Suspension.id == suspension_id))
    return result.scalar_one_or_none()


async def list_all_suspension(db: AsyncSession) -> list[Suspension]:
    result = await db.execute(
        select(Suspension).options(selectinload(Suspension.fields))
    )
    return result.scalars().all()
