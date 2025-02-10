from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from pydantic import BaseModel, ConfigDict, field_validator, Field
from typing import Optional
from enum import Enum
from uuid import UUID as UUIDType

class CategoryType(int, Enum):
    NEEDS = 1
    WANTS = 2
    SAVINGS = 3
    CUSTOM = 4

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, nullable=False)
    name = Column(String(50), nullable=False)
    type = Column(Integer, nullable=False)
    parent_category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    children = relationship("Category", backref="parent", remote_side=[id], cascade='all')
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, type={self.type}, parent_category_id={self.parent_category_id})>"

class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    type: CategoryType
    parent_category_id: Optional[int] = None
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

    
