from .base import Base
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, UUID, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from .category import Category
import enum

class BudgetType(enum.Enum):
    PERCENTAGE = "percentage"
    ENVELOPE = "envelope"

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(50), nullable=False)
    type = Column(Enum(BudgetType, name="budget_type_enum"), nullable=False)
    currency = Column(String(3), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    current_balance = Column(Float, default=0.0, server_default=expression.literal(0.0))
    target_total = Column(Float, nullable=True)

    percentage_breakdown = Column(JSON)
    envelops = relationship("Envelop", back_populates="budget")

class Envelop(Base):
    __tablename__ = "envelops"
    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    allocated_amount = Column(Float, nullable=False)
    spent_amount = Column(Float, default=0.0, server_default=expression.literal(0.0))
    budget = relationship("Budget", back_populates="envelops")