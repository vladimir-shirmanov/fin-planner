from ..domain.ports import SpecificationResolver
from  .database.resolvers.spec_resolver import SpecificationResolverRegistry
from .database.database import get_db

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends
import structlog


db_session_dep = Annotated[AsyncSession, Depends(get_db)]

class NamedLogger:
    def __init__(self, name: str):
        self.name = name

    def __call__(self) -> structlog.BoundLogger:
        return structlog.stdlib.get_logger(self.name)

def get_resolver(model_cls: type) -> SpecificationResolver:
    def resolver_factory():
        resolver_cls = SpecificationResolverRegistry.get_resolver(model_cls)
        if not resolver_cls:
            raise ValueError(f'No resolver registered for {model_cls}')
        return resolver_cls
    return resolver_factory