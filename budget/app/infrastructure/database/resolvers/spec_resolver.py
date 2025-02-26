from sqlalchemy.orm import DeclarativeBase
from uuid import UUID

from ..models import Budget
from ....domain.ports import Specification, SpecificationResolver

class SQLAlchemySpecificationResolver(SpecificationResolver):
    def __init__(self, model: DeclarativeBase):
        self.model = model

    def resolve(self, spec: Specification):
        return spec.resolve(self)
    
    def resolve_author(self, user_id: UUID):
        return self.model.user_id == user_id

class SpecificationResolverRegistry:
    _resolvers: dict[type, type] = {}

    @classmethod
    def register(cls, model_cls: type):
        def decorator(resolver_cls: type):
            cls._resolvers[model_cls] = resolver_cls
            return resolver_cls
        return decorator
    
    @classmethod
    def get_resolver(cls, model_cls: type) -> type:
        return cls._resolvers.get(model_cls)(model_cls)
    
@SpecificationResolverRegistry.register(Budget)
class BudgetSpecificationResolver(SQLAlchemySpecificationResolver):
    def __init__(self, model: DeclarativeBase = Budget):
        super().__init__(model)