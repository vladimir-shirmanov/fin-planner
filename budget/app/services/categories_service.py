from typing import List, Annotated
from fastapi import Depends
from sqlalchemy.future import select
from ..dependencies.core import db_session_dep, logger_dep
from ..models.category import CategoryCreate, CategoryResponse, Category
from ..models.user import User


class CategoryService:
    def __init__(self, db: db_session_dep, logger: logger_dep):
        self.db = db
        self.logger = logger

    async def create(self, category: CategoryCreate, user: User) -> CategoryResponse:
        """Create a new category"""
        self.logger = self.logger.bind(category=category)
        await self.logger.ainfo("BEGIN create_category")
        db_category = Category(**category.model_dump(), user_id=user.user_id)
        self.db.add(db_category)
        await self.db.commit()
        await self.db.refresh(db_category)
        response = CategoryResponse.model_validate(db_category)
        await self.logger.ainfo("END create_category", response=response)
        return response

    async def get(self) -> List[CategoryResponse]:
        """Get all categories"""
        await self.logger.ainfo("BEGIN get_categories")
        result = await self.db.execute(select(Category))
        categories = result.scalars().all()
        response = [CategoryResponse.model_validate(category) for category in categories]
        await self.logger.ainfo("END get_categories", response=response)
        return response

CategoryServiceDep = Annotated[CategoryService, Depends(CategoryService)]