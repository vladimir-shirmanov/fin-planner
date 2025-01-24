from pydantic import BaseModel, Field, model_validator
from datetime import date
from typing import Self

class Budget(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    start_date: date = Field(ge=date.today())
    end_date: date = Field(gt=start_date)

class BudgetItem(BaseModel):
    amount: float = Field(..., gt=0)
    category_id: int = Field(...)

class FixedBudget(Budget):
    items: list[BudgetItem] = []
    total_amount: sum([i.amount for i in items])

class SplitBudget(Budget):
    savings_percent: float = Field(..., ge=0, le=100)
    necessity_percent: float = Field(..., ge=0, le=100)
    wants_percent: float = Field(..., ge=0, le=100)

    @model_validator(mode="after")
    def validate_percentages(self) -> Self:
        if sum([self.savings_percent, self.necessity_percent, self.wants_percent]) != 100:
            raise ValueError("Percentages must sum to 100")
        return self