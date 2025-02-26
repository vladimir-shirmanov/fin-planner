from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from starlette.responses import JSONResponse
from structlog import BoundLogger

from ..domain.configs.config import Settings, get_settings
from ..infrastructure import db_session_dep, NamedLogger

router = APIRouter(tags=["health"])

async def check_database_health(db: AsyncSession, logger: BoundLogger, settings: Settings) -> bool:
    """Check PostgreSQL connection by executing query"""
    try:
        await db.execute(text("SELECT 1"))
        return True
    except Exception as e:
        await logger.aerror(
            "Database connection error",
            extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "service": settings.SERVICE_NAME
            },
            exc_info=True
        )
        return False

@router.get("/health", summary="Service Health check")
async def health(db: db_session_dep, logger = Depends(NamedLogger('health')), settings: Settings = Depends(get_settings)):
    db_health = await check_database_health(db, logger, settings)
    result = {
        "service":"Budget Service",
        "status":"healthy" if db_health else "unhealthy",
        "postgresql":db_health
    }

    return JSONResponse(
        content=result,
        status_code=status.HTTP_200_OK if db_health else status.HTTP_503_SERVICE_UNAVAILABLE
    )