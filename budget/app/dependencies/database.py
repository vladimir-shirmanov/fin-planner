from typing import AsyncGenerator, Any, AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncConnection
from sqlalchemy.ext.declarative import declarative_base
from contextlib import asynccontextmanager
from ..core.config import settings

DATABASE_NOT_INITIALIZED = "Database session manager has not been initialized"

Base = declarative_base()

class DatabaseSessionManager:
    def __init__(self, host:str, engine_kwargs:dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(bind=self._engine, autocommit=False)

    async def close(self):
        if self._engine is None:
            raise RuntimeError(DATABASE_NOT_INITIALIZED)
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise RuntimeError(DATABASE_NOT_INITIALIZED)

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise
    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise RuntimeError(DATABASE_NOT_INITIALIZED)
        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

sessionmanager = DatabaseSessionManager(settings.DATABASE_URL, {"echo": settings.echo_sql})

async def get_db() -> AsyncGenerator:
    async with sessionmanager.session() as session:
        yield session