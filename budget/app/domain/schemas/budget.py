from datetime import date
from typing import Literal, List, Union, Annotated, Optional
from pydantic import BaseModel, ConfigDict, model_validator, Field
from uuid import UUID
from ...infrastructure.database.models.budget import BudgetType

class BudgetBase(BaseModel):
    start_date: date
    end_date: date
    user_id: Optional[UUID] = Field(exclude=True, default=None)
    name: str
    currency: Literal['USD', 'HUF', 'UAH']
    type: BudgetType = Field(..., description="Type of budget to create")
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after')
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError('End date must be after start date')
        return self

class SimpleBudget(BudgetBase):
    type: Literal[BudgetType.SIMPLE]
    total_amount: float = Field(..., gt=0)

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "type": "simple",
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "total_amount": 1500.0,
                "name":"default",
                "currency":"USD"
            }]
        }
    }

class CategoryBudgetItem(BaseModel):
    category_id: int = Field(...)
    amount: float = Field(..., gt=0)

class CategoryBudget(BudgetBase):
    type: Literal[BudgetType.ENVELOPE]
    categories: List[CategoryBudgetItem]

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "type": "envelope",
                "start_date": "2024-03-01",
                "end_date": "2024-03-31",
                "categories": [
                    {"category_id": 1, "amount": 500},
                    {"category_id": 2, "amount": 300}
                ],
                "name":"default",
                "currency":"USD"
            }]
        }
    }

class PercentageBudget(BudgetBase):
    type: Literal[BudgetType.PERCENTAGE]
    needs_percent: float = Field(50.0, ge=0, le=100)
    wants_percent:float = Field(30.0, ge=0, le=100)
    savings_percent:float = Field(20.0, ge=0, le=100)

    @model_validator(mode='after')
    def validate_percentage(self):
        total = sum([self.needs_percent, self.wants_percent, self.savings_percent])
        if not 99.9 <= total <= 100.1:
            raise ValueError('Percentages must sum to 100')
        return self
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "type": "percentage",
                "start_date": "2024-02-01",
                "end_date": "2024-02-28",
                "needs_percent": 50,
                "wants_percent": 30,
                "savings_percent": 20,
                "name":"default",
                "currency":"USD"
            }]
        }
    }

BudgetCreatePayload = Annotated[
    Union[SimpleBudget, PercentageBudget, CategoryBudget],
    Field(discriminator='type')
]