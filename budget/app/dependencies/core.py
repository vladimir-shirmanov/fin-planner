from typing import Annotated

from ..dependencies.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

db_session_dep = Annotated[AsyncSession, Depends(get_db)]