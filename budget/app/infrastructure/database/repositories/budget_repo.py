from ....application.dependencies import db_session_dep
from ....domain.ports import Repository
from ....domain.schemas import BudgetBase
from ....infrastructure.database.models import Budget

from sqlalchemy.future import select

class BudgetRepository(Repository[BudgetBase]):
    def __init__(self, db: db_session_dep):
        self.db = db

    async def create(self, schema: BudgetBase) -> BudgetBase:
        db_budget = Budget(**schema.model_dump())
        self.db.add(db_budget)
        await self.db.commit()
        await self.db.refresh(db_budget)
        return BudgetBase.model_validate(db_budget)

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