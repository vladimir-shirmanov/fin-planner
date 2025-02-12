from typing import List
from fastapi import APIRouter
from ..models.category import CategoryCreate, CategoryResponse
from ..services.categories_service import CategoryServiceDep
from ..services.auth import current_user_dep

router = APIRouter(prefix="/category", tags=["categories"])

@router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(
    category: CategoryCreate,
    user: current_user_dep,
    service: CategoryServiceDep) -> CategoryResponse:
    """Create a new category"""
    return await service.create(category, user)

@router.get("", response_model=List[CategoryResponse])
async def get_categories(service: CategoryServiceDep):
    """Get all categories"""
    return await service.get()