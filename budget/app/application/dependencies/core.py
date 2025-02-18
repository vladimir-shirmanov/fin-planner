from typing import Annotated
import structlog
from ...infrastructure.database.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

db_session_dep = Annotated[AsyncSession, Depends(get_db)]

class NamedLogger:
    def __init__(self, name: str):
        self.name = name

    def __call__(self) -> structlog.BoundLogger:
        return structlog.stdlib.get_logger(self.name)