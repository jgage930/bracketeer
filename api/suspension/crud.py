from api.suspension.models import Suspension, SuspensionField
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
