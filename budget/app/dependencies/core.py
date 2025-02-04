from typing import Annotated
from structlog import BoundLogger
from ..dependencies.database import get_db
from ..core.logging import logger
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

db_session_dep = Annotated[AsyncSession, Depends(get_db)]

def get_logger() -> BoundLogger:
    return logger

logger_dep = Annotated[BoundLogger, Depends(get_logger)]