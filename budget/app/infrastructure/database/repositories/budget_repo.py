from ....application.dependencies import db_session_dep
from ....domain.ports import Repository
from ....domain.schemas import BudgetBase
from ....domain.exceptions import RepositoryError
from ....infrastructure.database.models import Budget, SimpleBudget, EnvelopBudget, PercentageBudget
from ..models.budget import BudgetType

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

class BudgetRepository(Repository[BudgetBase]):
    def __init__(self, db: db_session_dep):
        self.db = db

    async def create(self, schema: BudgetBase) -> BudgetBase:
        try:
            db_budget = Budget(
                user_id = schema.user_id,
                name = schema.name,
                type = schema.type,
                currency = schema.currency,
                start_date = schema.start_date,
                end_date = schema.end_date
            )
            self.db.add(db_budget)
            await self.db.flush()
            specific = None
            match schema.type:
                case BudgetType.SIMPLE:
                    specific = SimpleBudget(
                        id=db_budget.id,
                        total_amount=schema.total_amount
                    )
                case BudgetType.PERCENTAGE:
                    specific = PercentageBudget(
                        id=db_budget.id,
                        needs_percent=schema.needs_percent,
                        wants_percent=schema.wants_percent,
                        savings_percent=schema.savings_percent
                    )
                case BudgetType.ENVELOPE:
                    specific = [EnvelopBudget(
                        budget_id=db_budget.id,
                        category_id=c.category_id,
                        allocated_amount=c.amount
                    ) for c in schema.categories]

            if specific:
                if isinstance(specific, list):
                    self.db.add_all(specific)
                else:
                    self.db.add(specific)
            
            await self.db.commit()
            await self.db.refresh(db_budget)
            return BudgetBase.model_validate(db_budget)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RepositoryError('Database operation failed') from e

    async def update(self, schema):
        pass

    async def get_all(self):
        query = await self.db.execute(select(Budget))
        budgets = query.scalars().all()
        return (BudgetBase.model_validate(budget) for budget in budgets)

    async def get_by_id(self, id: int):
        pass

    async def delete(self, id: int):
        pass