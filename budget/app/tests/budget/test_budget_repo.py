import pytest
import uuid
from unittest.mock import patch, MagicMock

from ...infrastructure.database.repositories import BudgetRepository
from ...infrastructure.database.models.budget import BudgetType, Budget, SimpleBudget
from ...domain.schemas import SimpleBudget


@pytest.mark.asyncio
async def test_create_simple_budget(mock_db):
    """Test create with simple budget data should add base budget and simple budget"""
    # arrange
    budget_schema = SimpleBudget(
        user_id=uuid.uuid4(),
        name="Test Budget",
        type=BudgetType.SIMPLE,
        currency="USD",
        start_date="2025-01-01",
        end_date="2025-12-31",
        total_amount=1000
    )
    budget_repo = BudgetRepository(mock_db)
    mock_budget = MagicMock()
    mock_simple_budget = MagicMock()
    with patch('app.infrastructure.database.repositories.budget_repo.Budget') as MockBudget, \
        patch('app.infrastructure.database.repositories.budget_repo.SimpleBudget') as MockSimpleBudget, \
        patch('app.infrastructure.database.repositories.budget_repo.BudgetBase.model_validate') as MockBudgetBase:
        MockBudget.return_value = mock_budget
        MockSimpleBudget.return_value = mock_simple_budget
        MockBudgetBase.return_value = {**budget_schema.model_dump(), id: 10 }
        async def flush_side_efect():
            mock_budget.id = 10

        mock_db.flush.side_effect = flush_side_efect 

        #act
        result = await budget_repo.create(budget_schema)

        # assert
        mock_db.add.assert_any_call(mock_budget)
        mock_db.add.assert_any_call(mock_simple_budget)
        mock_db.flush.assert_awaited_once()
        mock_db.commit.assert_awaited_once()
        mock_db.refresh.assert_awaited_once_with(mock_budget)
        assert result.id == 10

