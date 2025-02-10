from typing import List, Annotated
from fastapi import Depends
from sqlalchemy.future import select
from ..dependencies.core import db_session_dep, logger_dep
from ..models.category import CategoryCreate, CategoryResponse, Category
from ..models.user import User

async def create_category(category: CategoryCreate, user:User, db: db_session_dep, log: logger_dep) -> CategoryResponse:
    """Create a new category"""
    log = log.bind(category=category)
    await log.ainfo("BEGIN create_category")
    db_category = Category(**category.model_dump(), user_id=user.user_id)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    response = CategoryResponse.model_validate(db_category)
    await log.ainfo("END create_category", response=response)
    return response

async def get_categories(db: db_session_dep, log: logger_dep) -> List[CategoryResponse]:
    """Get all categories"""
    await log.ainfo("BEGIN get_categories")
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    response = [CategoryResponse.model_validate(category) for category in categories]
    await log.ainfo("END get_categories", response=response)
    return response

CreateDependency = Annotated[CategoryResponse, Depends(create_category)]
GetDependency = Annotated[List[CategoryResponse], Depends(get_categories)]