from api.database import Base

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AccessLevel(Base):
    __tablename__ = "access_levels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    # Establish reverse 1-1 relationship
    user: Mapped["User"] = relationship(
        "User", back_populates="access_level", uselist=False
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)

    access_level_id: Mapped[int] = mapped_column(
        ForeignKey("access_levels.id"),
    )
    access_level: Mapped["AccessLevel"] = relationship(
        "AccessLevel", back_populates="user"
    )
