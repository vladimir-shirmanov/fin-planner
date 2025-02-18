from fastapi import APIRouter
from ..domain.schemas import BudgetBase
from ..application.services import BudgetServiceDep
from ..infrastructure.auth import current_user_dep

router = APIRouter(prefix="/category", tags=["categories"])

@router.post("", response_model=BudgetBase, status_code=201)
async def create_budget(
    budget: BudgetBase,
    user: current_user_dep,
    service: BudgetServiceDep) -> BudgetBase:
    """Create a new category"""
    budget.user_id = user.user_id
    return await service.create_budget(budget)