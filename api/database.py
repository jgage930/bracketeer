from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from typing import Annotated
import asyncio
import logging

logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite+aiosqlite:///./data.db"


class DatabaseException(Exception): ...


engine = create_async_engine(
    DATABASE_URL,
    echo=True,
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


Database = Annotated[AsyncSession, Depends(db_session)]


# Migration
async def migrate_tables() -> None:
    logger.info("Starting to migrate")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Done migrating")


if __name__ == "__main__":
    asyncio.run(migrate_tables())
