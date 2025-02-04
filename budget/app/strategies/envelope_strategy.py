from .base_strategy import BudgetStrategy

class EnvelopeStrategy(BudgetStrategy):
    def __init__(self, envelopes: List[EnvelopeCreate]):
        self.envelopes = envelopes
    
    def validate_allocation(self, income: float) -> bool:
        return sum(e.allocated_amount for e in self.envelopes) <= income
    
    def calculate_allocation(self, income: float) -> dict:
        return {e.category.name: e.allocated_amount for e in self.envelopes}