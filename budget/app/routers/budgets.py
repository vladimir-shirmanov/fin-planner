from fastapi import APIRouter

router = APIRouter(tags=["budgets"])

@router.post("percentage", response_model=BudgetResponse, status_code=201)
async def create_budget(budget: PercentageBudgetCreate, budget_service = Depends(budget_service)):
    """Create a new budget"""
    return await budget_service.create_budget(budget)

@router.post("envelope", response_model=BudgetResponse, status_code=201)
async def create_budget(budget: EnvelopeBudgetCreate, budget_service = Depends(budget_service)):
    """Create a new budget"""
    return await budget_service.create_budget(budget)

@router.get("/{budget_id}/progress", response_model=BudgetProgressResponse)
async def get_budget_progress(budget_id: int, budget_service = Depends(budget_service)):
    """Get budget progress"""
    return await budget_service.calculate_progress(budget_id)