from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import Budget, SimpleBudget, PercentageBudget, EnvelopBudget
from ...domain.schemas import BudgetBase, SimpleBudget as SchemaSimple, PercentageBudget as SchemaPercentage, CategoryBudget as SchemaCategory
from ...domain.schemas.budget import CategoryBudgetItem

class BudgetLoader(ABC):
    @abstractmethod
    async def load(self, db_budget: Budget) -> BudgetBase:
        pass

class SimpleBudgetLoader(BudgetLoader):
    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db

    async def load(self, db_budget):
        simple_db = await self.db.get(SimpleBudget, db_budget.id)
        return SchemaSimple.model_validate({
            **db_budget.__dict__,
            'total_amount': simple_db.total_amount
        })

class PercentageBudgetLoader(BudgetLoader):
    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db

    async def load(self, db_budget):
        percentage_db = await self.db.get(PercentageBudget, db_budget.id)
        return SchemaPercentage.model_validate({
            **db_budget.__dict__,
            'needs_percent': percentage_db.needs_percent,
            'wants_percent': percentage_db.wants_percent,
            'savings_percent': percentage_db.savings_percent,
        })
    
class CategotyBudgetLoader(BudgetLoader):
    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db

    async def load(self, db_budget):
        stmt = select(EnvelopBudget).where(EnvelopBudget.budget_id == db_budget.id)
        result = await self.db.execute(stmt)
        envelope_dbs = result.scalars().fetchall()
        categories = [
            CategoryBudgetItem(category_id=env.category_id, amount=env.allocated_amount)
            for env in envelope_dbs
        ]
        return SchemaCategory(
            id=db_budget.id,
            start_date=db_budget.start_date,
            end_date=db_budget.end_date,
            user_id=db_budget.user_id,
            name=db_budget.name,
            currency=db_budget.currency,
            type=db_budget.type,
            categories=categories
        )