from .base_strategy import BudgetStrategy


class PercentageStrategy(BudgetStrategy):
    def __init__(self, percentages: dict):
        self.percentages = percentages

    def validate_allocation(self, income: float) -> bool:
        return sum(self.percentages.values()) == 100
    
    def calculate_allocation(self, income: float) -> dict:
        return {k: round(value/100 * income, 2) for k, value in self.percentages.items()}