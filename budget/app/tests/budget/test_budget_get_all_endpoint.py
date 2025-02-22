import pytest

from uuid import UUID
from fastapi.testclient import TestClient
from fastapi import HTTPException, status
from unittest.mock import AsyncMock

from ...domain.schemas.user import User
from ...domain.exceptions import RepositoryError
from ...domain.schemas.budget import (
    BudgetBase
)
from ...application.services import BudgetService
from ...infrastructure.auth.auth import get_current_user
from ...infrastructure.database.database import get_db
from ...infrastructure.database.models.budget import BudgetType
from ...main import app

TEST_USER = User(
    email="test@example.com",
    user_id=UUID("123e4567-e89b-12d3-a456-426614174000")
)

BUDGET = BudgetBase(
        id=1,
        start_date='2025-02-20',
        currency='USD',
        end_date='2025-02-22',
        name='default',
        type='simple',
        user_id=TEST_USER.user_id
    )

@pytest.fixture
def mock_auth():
    return TEST_USER

@pytest.fixture
def mock_budget_service():
    budget_service = AsyncMock()
    budget_service.create_budget.return_value = BUDGET
    return budget_service

@pytest.fixture
def client(mock_budget_service, mock_auth, mock_db):
    app.dependency_overrides[get_current_user] = lambda: mock_auth
    app.dependency_overrides[BudgetService] = lambda: mock_budget_service
    app.dependency_overrides[get_db] = lambda: mock_db
    yield TestClient(app, raise_server_exceptions=False)
    app.dependency_overrides = {} 

def test_create_category_unauthorized(client):
    # Arrange
    def mock_auth():
        raise HTTPException(status_code=401, detail="Invalid token")
    app.dependency_overrides[get_current_user] = mock_auth

    # Act
    response = client.get(
        "/budget"
    )
    
    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_all_budgets_success(client, mock_budget_service):
    #arrange
    mock_budget_service.get_all_budgets.return_value = [
        BudgetBase(
            user_id=TEST_USER.user_id,
            currency='USD',
            end_date='2024-03-31',
            start_date='2024-03-30',
            id=1,
            name='default',
            type=BudgetType.SIMPLE
        )
    ]

    #act
    response = client.get("/budget")

    #assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()[0]
    assert data["type"] == "simple"
    assert data['id'] == 1


def test_repository_error_from_service(client, mock_budget_service):
    #arrange
    mock_budget_service.get_all_budgets.side_effect = RepositoryError("Database error")

    #act
    response = client.get("/budget")

    #assert
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Database error" in response.json()["detail"]