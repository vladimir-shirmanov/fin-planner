import pytest

from uuid import UUID
from fastapi.testclient import TestClient
from fastapi import HTTPException, status
from unittest.mock import AsyncMock

from ...domain.schemas.user import User
from ...domain.exceptions import RepositoryError
from ...domain.schemas.budget import (
    BudgetBase,
    SimpleBudget,
    CategoryBudget,
    PercentageBudget
)
from ...application.services import BudgetService
from ...infrastructure.auth.auth import get_current_user
from ...infrastructure.database.database import get_db
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
    response = client.post(
        "/budget",
        json={
            'name':'default'
        }
    )
    
    # Assert
    assert response.status_code == 401

# Success Cases
def test_create_simple_budget_success(client, mock_auth, mock_budget_service):
    #arrange
    simple_budget = SimpleBudget(
        id=1,
        type="simple",
        start_date="2024-01-01",
        end_date="2024-01-31",
        total_amount=1500.0,
        name="default",
        currency="USD",
        user_id=TEST_USER.user_id
    )
    mock_budget_service.create_budget.return_value = simple_budget

    payload = {
        "type": "simple",
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
        "total_amount": 1500.0,
        "name": "default",
        "currency": "USD"
    }

    #act
    response = client.post("/budget", json=payload)

    # assert
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["type"] == "simple"
    assert "user_id" not in data
    args, _ = mock_budget_service.create_budget.call_args
    assert args[0].user_id == mock_auth.user_id


def test_create_percentage_budget_success(client, mock_auth, mock_budget_service):
    #arrange
    percentage_budget = PercentageBudget(
        id=2,
        type="percentage",
        start_date="2024-02-01",
        end_date="2024-02-28",
        needs_percent=50,
        wants_percent=30,
        savings_percent=20,
        name="default",
        currency="USD",
        user_id=TEST_USER.user_id
    )
    mock_budget_service.create_budget.return_value = percentage_budget

    payload = {
        "type": "percentage",
        "start_date": "2024-02-01",
        "end_date": "2024-02-28",
        "needs_percent": 50,
        "wants_percent": 30,
        "savings_percent": 20,
        "name": "default",
        "currency": "USD"
    }

    #act
    response = client.post("/budget", json=payload)

    #assert
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["type"] == "percentage"
    assert "user_id" not in data

def test_create_category_budget_success(client, mock_auth, mock_budget_service):
    #arrange
    category_budget = CategoryBudget(
        id=3,
        type="envelope",
        start_date="2024-03-01",
        end_date="2024-03-31",
        categories=[{"category_id": 1, "amount": 500}, {"category_id": 2, "amount": 300}],
        name="default",
        currency="USD",
        user_id=TEST_USER.user_id
    )
    mock_budget_service.create_budget.return_value = category_budget

    payload = {
        "type": "envelope",
        "start_date": "2024-03-01",
        "end_date": "2024-03-31",
        "categories": [{"category_id": 1, "amount": 500}, {"category_id": 2, "amount": 300}],
        "name": "default",
        "currency": "USD"
    }

    #act
    response = client.post("/budget", json=payload)

    #assert
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["type"] == "envelope"
    assert "categories" in data

# Validation Error Cases
def test_invalid_budget_type(client, mock_auth, mock_budget_service):
    #arrange

    payload = {
        "type": "invalid",
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
        "total_amount": 1500.0,
        "name": "default",
        "currency": "USD"
    }

    #act
    response = client.post("/budget", json=payload)

    #assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "type" in response.text


def test_missing_required_field(client, mock_auth, mock_budget_service):
    # arrange
    payload = {
        "type": "simple",
        "start_date": "2024-01-01",
        # Missing end_date, total_amount, etc.
        "name": "default",
        "currency": "USD"
    }

    #act
    response = client.post("/budget", json=payload)

    #assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_value_error_from_service(client, mock_budget_service):
    # arrange
    mock_budget_service.create_budget.side_effect = ValueError("Invalid percentages")
    
    # Sum is 110
    payload = {
        "type": "percentage",
        "start_date": "2024-02-01",
        "end_date": "2024-02-28",
        "needs_percent": 60,
        "wants_percent": 30,
        "savings_percent": 20,
        "name": "default",
        "currency": "USD"
    }

    #act
    response = client.post("/budget", json=payload)

    #assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    lst = response.json()['detail']
    assert "Percentages must sum to 100" in lst[0]['msg']

def test_date_error_from_service(client, mock_budget_service):
    # arrange
    mock_budget_service.create_budget.side_effect = ValueError("Invalid percentages")
    
    # Sum is 110
    payload = {
        "type": "percentage",
        "start_date": "2024-02-01",
        "end_date": "2024-01-28",
        "needs_percent": 60,
        "wants_percent": 30,
        "savings_percent": 20,
        "name": "default",
        "currency": "USD"
    }

    #act
    response = client.post("/budget", json=payload)

    #assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    lst = response.json()['detail']
    assert "End date must be after start date" in lst[0]['msg']

def test_repository_error_from_service(client, mock_auth, mock_budget_service):
    #arrange
    mock_budget_service.create_budget.side_effect = RepositoryError("Database error")

    payload = {
        "type": "simple",
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
        "total_amount": 1500.0,
        "name": "default",
        "currency": "USD"
    }

    #act
    response = client.post("/budget", json=payload)

    #assert
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Database error" in response.json()["detail"]