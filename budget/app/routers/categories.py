from typing import List
from fastapi import APIRouter
from ..models.category import CategoryCreate, CategoryResponse
from ..services.categories_service import CreateDependency, GetDependency
from ..services.auth import current_user_dep

router = APIRouter(prefix="/category", tags=["categories"])

@router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(
    category: CategoryCreate,
    user: current_user_dep,
    create: CreateDependency):
    """Create a new category"""
    return create

@router.get("", response_model=List[CategoryResponse])
async def get_categories(get: GetDependency):
    """Get all categories"""
    return get