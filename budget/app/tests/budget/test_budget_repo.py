import pytest
import uuid
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError

from ...infrastructure.database.repositories import BudgetRepository
from ...infrastructure.database.models.budget import BudgetType, SimpleBudget
from ...domain.schemas import SimpleBudget, PercentageBudget, CategoryBudget
from ...domain.exceptions import RepositoryError


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

@pytest.mark.asyncio
async def test_create_percentage_budget(mock_db):
    """Test create with percentage budget data should add base budget and simple budget"""
    # arrange
    budget_schema = PercentageBudget(
        user_id=uuid.uuid4(),
        name="Test Budget",
        type=BudgetType.PERCENTAGE,
        currency="USD",
        start_date="2025-01-01",
        end_date="2025-12-31",
        needs_percent=60,
        savings_percent=30,
        wants_percent=10
    )
    budget_repo = BudgetRepository(mock_db)
    mock_budget = MagicMock()
    mock_percentage_budget = MagicMock()
    with patch('app.infrastructure.database.repositories.budget_repo.Budget') as MockBudget, \
        patch('app.infrastructure.database.repositories.budget_repo.PercentageBudget') as MockSimpleBudget, \
        patch('app.infrastructure.database.repositories.budget_repo.BudgetBase.model_validate') as MockBudgetBase:
        MockBudget.return_value = mock_budget
        MockSimpleBudget.return_value = mock_percentage_budget
        MockBudgetBase.return_value = {**budget_schema.model_dump(), id: 10 }
        async def flush_side_efect():
            mock_budget.id = 10

        mock_db.flush.side_effect = flush_side_efect 

        #act
        result = await budget_repo.create(budget_schema)

        # assert
        mock_db.add.assert_any_call(mock_budget)
        mock_db.add.assert_any_call(mock_percentage_budget)
        mock_db.flush.assert_awaited_once()
        mock_db.commit.assert_awaited_once()
        mock_db.refresh.assert_awaited_once_with(mock_budget)

@pytest.mark.asyncio
async def test_create_category_budget(mock_db):
    """Test create with category budget data should add base budget and simple budget"""
    # arrange
    budget_schema = CategoryBudget(
        user_id=uuid.uuid4(),
        name="Test Budget",
        type=BudgetType.ENVELOPE,
        currency="USD",
        start_date="2025-01-01",
        end_date="2025-12-31",
        categories=[
            {"category_id": 1, "amount": 500},
            {"category_id": 2, "amount": 300}
        ],
    )
    budget_repo = BudgetRepository(mock_db)
    mock_budget = MagicMock()
    mock_category_budget = MagicMock()
    with patch('app.infrastructure.database.repositories.budget_repo.Budget') as MockBudget, \
        patch('app.infrastructure.database.repositories.budget_repo.EnvelopBudget') as MockSimpleBudget, \
        patch('app.infrastructure.database.repositories.budget_repo.BudgetBase.model_validate') as MockBudgetBase:
        MockBudget.return_value = mock_budget
        MockSimpleBudget.return_value = mock_category_budget
        MockBudgetBase.return_value = {**budget_schema.model_dump(), id: 10 }
        async def flush_side_efect():
            mock_budget.id = 10

        mock_db.flush.side_effect = flush_side_efect 

        #act
        result = await budget_repo.create(budget_schema)

        # assert
        mock_db.add.assert_any_call(mock_budget)
        mock_db.add_all.assert_called()
        mock_db.flush.assert_awaited_once()
        mock_db.commit.assert_awaited_once()
        mock_db.refresh.assert_awaited_once_with(mock_budget)

@pytest.mark.asyncio
async def test_create_db_cannot_save_should_throws_repository_exception(mock_db):
    """Test create and database can't save data, should throw repository exception"""
    # arrange
    budget_schema = CategoryBudget(
        user_id=uuid.uuid4(),
        name="Test Budget",
        type=BudgetType.ENVELOPE,
        currency="USD",
        start_date="2025-01-01",
        end_date="2025-12-31",
        categories=[
            {"category_id": 1, "amount": 500},
            {"category_id": 2, "amount": 300}
        ],
    )
    mock_db.commit.side_effect = SQLAlchemyError('Db error')
    budget_repo = BudgetRepository(mock_db)
    mock_budget = MagicMock()
    mock_category_budget = MagicMock()
    with patch('app.infrastructure.database.repositories.budget_repo.Budget') as MockBudget, \
        patch('app.infrastructure.database.repositories.budget_repo.EnvelopBudget') as MockSimpleBudget, \
        patch('app.infrastructure.database.repositories.budget_repo.BudgetBase.model_validate') as MockBudgetBase:
        MockBudget.return_value = mock_budget
        MockSimpleBudget.return_value = mock_category_budget
        MockBudgetBase.return_value = {**budget_schema.model_dump(), id: 10 }
        async def flush_side_efect():
            mock_budget.id = 10

        mock_db.flush.side_effect = flush_side_efect

        #act
        with pytest.raises(RepositoryError):
            await budget_repo.create(budget_schema)

        # assert
        mock_db.rollback.assert_awaited_once()