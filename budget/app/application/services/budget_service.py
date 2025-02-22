from ...domain.ports import Repository
from ...domain.specifications import AuthorSpec
from ...domain.schemas import BudgetBase
from ...infrastructure.database.repositories import BudgetRepository
from ...infrastructure import NamedLogger

from fastapi import Depends
from typing import Annotated, List
from uuid import UUID

class BudgetService:
    def __init__(self, budget_repository: Repository[BudgetBase] = Depends(BudgetRepository), logger = Depends(NamedLogger('budget_service'))):
        self.budget_repository = budget_repository
        self.logger = logger
    
    async def create_budget(self, budget: BudgetBase) -> BudgetBase:
        response = await self.budget_repository.create(budget)
        await self.logger.ainfo('END create', budget_result = response)
        return response
    
    async def get_all_budgets(self, user_id: UUID) -> List[BudgetBase]:
        response = await self.budget_repository.find(AuthorSpec(user_id))
        await self.logger.ainfo('END get_all_budgets', budgets_count=len(response))
        return response
    
BudgetServiceDep = Annotated[BudgetService, Depends(BudgetService)]