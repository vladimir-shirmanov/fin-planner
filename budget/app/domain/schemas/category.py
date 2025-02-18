from pydantic import BaseModel, ConfigDict, field_validator, Field
from typing import Optional
from enum import Enum
from uuid import UUID as UUIDType

class CategoryType(int, Enum):
    EXPENSE = 1
    WANTS = 2
    INCOME = 3
    SAVINGS = 4
    CUSTOM = 5

class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    type: CategoryType
    parent_category_id: Optional[int] = None
    favicon: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
    @field_validator('type')
    @classmethod
    def validate_type(cls, value):
        if not isinstance(value, CategoryType):
            try:
                return CategoryType(value)
            except ValueError:
                raise ValueError(f"Invalid category type. Must be one of: {[t.value for t in CategoryType]}")
        return value

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    user_id: UUIDType
