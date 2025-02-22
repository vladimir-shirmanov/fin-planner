from typing import List, Annotated
from fastapi import Depends
from sqlalchemy.future import select
from ...infrastructure import db_session_dep, NamedLogger
from ...domain.schemas.category import CategoryCreate, CategoryResponse
from ...domain.configs.categories_init import ADMIN_USER_ID
from ...infrastructure.database.models.category import Category
from uuid import UUID

class CategoryService:
    def __init__(self, db: db_session_dep, logger = Depends(NamedLogger('category_service'))):
        self.db = db
        self.logger = logger

    async def create(self, category: CategoryCreate, user_id: UUID) -> CategoryResponse:
        """Create a new category"""
        db_category = Category(**category.model_dump(), user_id=user_id)
        self.db.add(db_category)
        await self.db.commit()
        await self.db.refresh(db_category)
        response = CategoryResponse.model_validate(db_category)
        await self.logger.ainfo('END create', response=response, user_id=user_id)
        return response

    async def get(self, user_id: UUID) -> List[CategoryResponse]:
        """Get all categories"""
        result = await self.db.execute(select(Category).where(Category.user_id.in_([user_id, ADMIN_USER_ID])))
        categories = result.scalars().all()
        response = [CategoryResponse.model_validate(category) for category in categories]
        return response

CategoryServiceDep = Annotated[CategoryService, Depends(CategoryService)]