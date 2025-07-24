from collections.abc import AsyncGenerator

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import asyncio
import logging


logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite+aiosqlite:///./data.db"


class DatabaseException(Exception): ...


engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # needed for SQLite
)
Base = declarative_base()


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for accessing a db session in an endpoint.
    """

    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseException("Failed to get session.") from e


# DB Models


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
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)

    access_level_id: Mapped[int] = mapped_column(
        ForeignKey("access_levels.id"), unique=True
    )
    access_level: Mapped["AccessLevel"] = relationship(
        "AccessLevel", back_populates="user"
    )


# Migration
async def migrate_tables() -> None:
    logger.info("Starting to migrate")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Done migrating")


if __name__ == "__main__":
    asyncio.run(migrate_tables())
