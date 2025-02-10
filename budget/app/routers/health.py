from fastapi import APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from starlette.responses import JSONResponse

from ..core.config import settings
from ..dependencies.core import db_session_dep, logger_dep

router = APIRouter(tags=["health"])

async def check_database_health(db: AsyncSession, logger) -> bool:
    """Check PostgreSQL connection by executing query"""
    try:
        await db.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(
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
async def health(db: db_session_dep, logger: logger_dep):
    db_health = await check_database_health(db, logger)
    result = {
        "service":"Budget Service",
        "status":"healthy" if db_health else "unhealthy",
        "postgresql":db_health
    }

    return JSONResponse(
        content=result,
        status_code=status.HTTP_200_OK if db_health else status.HTTP_503_SERVICE_UNAVAILABLE
    )