from typing import Annotated
import structlog
from ..dependencies.database import get_db
from ..core.logging import logger
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

db_session_dep = Annotated[AsyncSession, Depends(get_db)]

def get_logger() -> structlog.BoundLogger:
    return logger

logger_dep = Annotated[structlog.BoundLogger, Depends(get_logger)]