from collections.abc import AsyncGenerator

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

DATABASE_URL = "sqlite:///./food.db"

# engine = create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}  # needed for SQLite
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


class DatabaseException(Exception): ...


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for accessing a db session in an endpoint.
    """
    engine = create_async_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # needed for SQLite
    )

    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseException("Failed to get session.") from e
