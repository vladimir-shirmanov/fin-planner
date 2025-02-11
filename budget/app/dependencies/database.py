from typing import AsyncGenerator, Any, AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncConnection
from contextlib import asynccontextmanager
from fastapi import Depends
from ..core.config import settings_dep, Settings

DATABASE_NOT_INITIALIZED = "Database session manager has not been initialized"

class DatabaseSessionManager:
    def __init__(self, settings: Settings):
        self._engine = create_async_engine(settings.DATABASE_URL, {'echo': settings.echo_sql})
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

def get_session_manager(settings: settings_dep) -> DatabaseSessionManager:
    return DatabaseSessionManager(settings)

async def get_db(sessionmanager:DatabaseSessionManager = Depends(get_session_manager)) -> AsyncGenerator:
    async with sessionmanager.session() as session:
        yield session