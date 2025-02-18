from .base import Base
from sqlalchemy import Column, Date, ForeignKey, Integer, String, UUID, Enum, Numeric
from sqlalchemy.orm import relationship
import enum

class BudgetType(enum.Enum):
    PERCENTAGE = "percentage"
    ENVELOPE = "envelope"
    SIMPLE = 'simple'

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(50), nullable=False)
    type = Column(Enum(BudgetType, name="budget_type_enum"), nullable=False)
    currency = Column(String(3), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    simple_budget = relationship('SimpleBudget', uselist=False, back_populates='budget')
    percentage_budget = relationship('PercentageBudget', uselist=False, back_populates='budget')
    envelop_budget = relationship('EnvelopBudget', uselist=False, back_populates='budget')

class SimpleBudget(Base):
    __tablename__ = "simple_budgets"
    id = Column(Integer, ForeignKey('budgets.id'), primary_key=True)
    total_amount = Column(Numeric(10,2))
    budget = relationship('Budget', back_populates='simple_budget')

class PercentageBudget(Base):
    __tablename__ = "percentage_budgets"
    id = Column(Integer, ForeignKey('budgets.id'), primary_key=True)
    needs_percent = Column(Numeric(5,2), default=50.0)
    wants_percent = Column(Numeric(5,2), default=30.0)
    savings_percent = Column(Numeric(5,2), default=20.0)

    budget = relationship('Budget', back_populates='percentage_budget')

class EnvelopBudget(Base):
    __tablename__ = "envelop_budgets"
    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    allocated_amount = Column(Numeric(10,2), nullable=False)
    budget = relationship("Budget", back_populates="envelop_budget")