from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from fastapi import Depends
from ..configs.config import get_settings, Settings

DATABASE_NOT_INITIALIZED = "Database session manager has not been initialized"

def create_engine_and_session(settings: Settings):
    engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=settings.echo_sql)
    session_maker = async_sessionmaker(bind=engine, autocommit=False)
    return engine, session_maker

async def get_db(settings: Settings = Depends(get_settings)) -> AsyncGenerator[AsyncSession, None]:
    engine, session_maker = create_engine_and_session(settings)
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.aclose()

        await engine.dispose()