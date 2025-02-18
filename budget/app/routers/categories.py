from typing import List
from fastapi import APIRouter
from ..domain.schemas import CategoryCreate, CategoryResponse
from ..application.services import CategoryServiceDep
from ..infrastructure.auth import current_user_dep

router = APIRouter(prefix="/category", tags=["categories"])

@router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(
    category: CategoryCreate,
    user: current_user_dep,
    service: CategoryServiceDep) -> CategoryResponse:
    """Create a new category"""
    return await service.create(category, user.user_id)

@router.get("", response_model=List[CategoryResponse])
async def get_categories(user: current_user_dep, service: CategoryServiceDep):
    """Get all default categories and those created by user"""
    return await service.get(user.user_id)