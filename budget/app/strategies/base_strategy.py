from abc import ABC, abstractmethod


class BudgetStrategy(ABC):
    @abstractmethod
    def validate_allocation(self, income: float) -> bool:
        pass

    @abstractmethod
    def calculate_allocation(self, income: float) -> dict:
        pass