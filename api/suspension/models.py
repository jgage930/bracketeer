from api.database import Base

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Suspension(Base):
    __tablename__ = "suspensions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String())
    type: Mapped[str] = mapped_column(String())

    fields: Mapped[list["SuspensionField"]] = relationship(
        back_populates="suspension", cascade="all, delete-orphan"
    )


class SuspensionField(Base):
    __tablename__ = "suspension_fields"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    suspension_id: Mapped[int] = mapped_column(
        ForeignKey("suspensions.id", ondelete="CASCADE")
    )

    name: Mapped[str] = mapped_column(String())
    min: Mapped[int] = mapped_column(Integer())
    max: Mapped[int] = mapped_column(Integer())
    unit: Mapped[str] = mapped_column(String())

    suspension: Mapped["Suspension"] = relationship(back_populates="fields")
