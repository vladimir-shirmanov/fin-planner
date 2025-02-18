from datetime import date
from typing import Literal, List
from pydantic import BaseModel, ConfigDict

class BudgetBase(BaseModel):
    user_id: str
    start_date: date
    end_date: date
    type: Literal['simple', '503020', 'category']
    model_config = ConfigDict(from_attributes=True)

class SimpleBudget(BudgetBase):
    total_amount: float

class CategoryBudgetItem(BaseModel):
    category_id: int
    amount: float

class CategoryBudget(BudgetBase):
    categories: List[CategoryBudgetItem]

class PercentageBudget(BudgetBase):
    needs_percent: float
    wants_percent:float
    savings_percent:float