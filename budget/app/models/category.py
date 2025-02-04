from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from .base import Base
from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum

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


class CategoryCreate(BaseModel):
    name: str
    type: CategoryType
    parent_category_id: int = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    type: CategoryType
    parent_category_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)
    
