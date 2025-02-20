import pytest
import uuid
from unittest.mock import AsyncMock

from ...application.services import BudgetService
from ...domain.schemas import BudgetBase
from ...infrastructure.database.models.budget import BudgetType

BUDGET = BudgetBase(
        id=1,
        start_date='2025-02-20',
        currency='USD',
        end_date='2025-02-22',
        name='default',
        type=BudgetType.SIMPLE,
        user_id=uuid.uuid4()
    )

@pytest.fixture
def mock_repository():
    repo = AsyncMock()
    repo.create.return_value = BUDGET
    return repo

@pytest.fixture
def budget_service(mock_repository, mock_logger):
    return BudgetService(mock_repository, mock_logger)

@pytest.mark.asyncio
async def test_create_budget_success_flow(budget_service, mock_logger):
    # arrange

    # act
    result = await budget_service.create_budget(BUDGET)

    #assert
    mock_logger.ainfo.assert_awaited_once()
    assert result.id == 1