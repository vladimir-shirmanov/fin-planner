from ...domain.ports import Repository
from ...domain.schemas import BudgetBase
from ...infrastructure.database.repositories import BudgetRepository
from ...application.dependencies import NamedLogger
from fastapi import Depends
from typing import Annotated 

class BudgetService:
    def __init__(self, budget_repository: Repository = Depends(BudgetRepository), logger = Depends(NamedLogger('budget_service'))):
        self.budget_repository = budget_repository
    
    async def create_budget(self, budget: BudgetBase) -> BudgetBase:
        response = await self.budget_repository(budget)
        await self.logger.ainfo('END create', budget_result = response)
        return response
    
BudgetServiceDep = Annotated[BudgetService, Depends(BudgetService)]