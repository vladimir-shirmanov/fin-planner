from fastapi import APIRouter, HTTPException, status
from ..domain.schemas import BudgetCreatePayload, SimpleBudget, CategoryBudget, PercentageBudget, BudgetBase
from ..domain.exceptions import RepositoryError
from ..application.services import BudgetServiceDep
from ..infrastructure.auth import current_user_dep
from typing import Union, List

router = APIRouter(prefix="/budget", tags=["budgets"])

@router.post("", 
            response_model=Union[SimpleBudget, PercentageBudget, CategoryBudget],
            responses={
                201: {
                    "description": "Successfully created budget",
                    "content": {
                        "application/json": {
                            "examples": {
                                "Simple": {
                                    "summary": "Simple Budget",
                                    "value": SimpleBudget.model_config["json_schema_extra"]["examples"][0]
                                },
                                "Percentage": {
                                    "summary": "50/30/20 Budget",
                                    "value": PercentageBudget.model_config["json_schema_extra"]["examples"][0]
                                },
                                "Envelope": {
                                    "summary": "Category Budget",
                                    "value": CategoryBudget.model_config["json_schema_extra"]["examples"][0]
                                }
                            }
                        }
                    }
                }
            },
            openapi_extra={
                "requestBody": {
                    "content": {
                        "application/json": {
                            "examples": {
                                "SimpleBudgetExample": {
                                    "summary": "Simple Budget",
                                    "value": {
                                        "type": "simple",
                                        "start_date": "2024-01-01",
                                        "end_date": "2024-01-31",
                                        "total_amount": 1500.0,
                                        "name":"default",
                                        "currency":"USD"
                                    }
                                },
                                "PercentageBudgetExample": {
                                    "summary": "50/30/20 Budget",
                                    "value": {
                                        "type": "percentage",
                                        "start_date": "2024-02-01",
                                        "end_date": "2024-02-28",
                                        "needs_percent": 50,
                                        "wants_percent": 30,
                                        "savings_percent": 20,
                                        "name":"default",
                                        "currency":"USD"
                                    }
                                },
                                "EnvelopeBudgetExample": {
                                    "summary": "Category Budget",
                                    "value": {
                                        "type": "envelope",
                                        "start_date": "2024-03-01",
                                        "end_date": "2024-03-31",
                                        "categories": [
                                            {"category_id": 1, "amount": 500},
                                            {"category_id": 2, "amount": 300}
                                        ],
                                        "name":"default",
                                        "currency":"USD"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            status_code=status.HTTP_201_CREATED,
            response_model_exclude={"user_id"})
async def create_budget(
    payload: BudgetCreatePayload,
    user: current_user_dep,
    service: BudgetServiceDep) -> Union[SimpleBudget, PercentageBudget, CategoryBudget]:
    """Create a new category"""
    try:
        budget_data = payload.model_dump()
        budget_data['user_id'] = user.user_id
        return await service.create_budget(payload.model_validate(budget_data))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RepositoryError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get('',
            response_model=list[BudgetBase],
            status_code=status.HTTP_200_OK)
async def get_created_budgets(
    user: current_user_dep,
    service: BudgetServiceDep
) -> List[BudgetBase]:
    """Get budgets created by user"""
    try:
        return await service.get_all_budgets(user.user_id)
    except RepositoryError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('{id}',
            response_model=Union[SimpleBudget, PercentageBudget, CategoryBudget],
            status_code=status.HTTP_200_OK)
async def get_by_id(
    id: int,
    user: current_user_dep,
    service: BudgetServiceDep
) -> Union[SimpleBudget, PercentageBudget, CategoryBudget]:
    """Get budget by id"""
    try:
        budget = await service.get_budget_by_id(user.user_id, id)
        if not budget:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You're not an author")
        return budget
    except RepositoryError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

