from ...models.user import User
from ...models.category import CategoryCreate, CategoryType, CategoryResponse
from uuid import UUID
import pytest
from unittest.mock import AsyncMock, MagicMock
from ...services.categories_service import CategoryService
from ...services.auth import get_current_user
from ...dependencies.database import get_db
from ...main import app
from fastapi.testclient import TestClient
from fastapi import HTTPException


TEST_USER = User(
    email="test@example.com",
    user_id=UUID("123e4567-e89b-12d3-a456-426614174000")
)

TEST_CATEGORY = CategoryCreate (
    name="Test Category",
    type=CategoryType.EXPENSE
)

@pytest.fixture
def mock_category_service():
    service = MagicMock()
    service.create = AsyncMock()
    return service

@pytest.fixture
def mock_auth():
    return TEST_USER

@pytest.fixture
def mock_db():
    return AsyncMock()

@pytest.fixture
def client(mock_category_service, mock_auth, mock_db):
    app.dependency_overrides[get_current_user] = lambda: mock_auth
    app.dependency_overrides[CategoryService] = lambda: mock_category_service
    app.dependency_overrides[get_db] = lambda: mock_db
    yield TestClient(app, raise_server_exceptions=False)
    app.dependency_overrides = {}

def test_create_category_success(client, mock_category_service):
    # Arrange
    expected_response = CategoryResponse(
        id=1,
        name=TEST_CATEGORY.name,
        type=TEST_CATEGORY.type,
        parent_category_id=None,
        user_id="123e4567-e89b-12d3-a456-426614174000"
    )
    mock_category_service.create.return_value = expected_response

    # Act
    response = client.post("/category", json=TEST_CATEGORY.model_dump())

    # Assert
    print(response.json())
    assert response.status_code == 201
    assert response.json() == expected_response.model_dump(mode='json')

def test_create_category_invalid_data(client):
    # Act
    response = client.post('/category', json={
        "name":"",
        "type":"invalid_type"
    })

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error['loc'] == ['body', 'name'] for error in errors)
    assert any(error['loc'] == ['body', 'type'] for error in errors)

def test_create_category_service_error(client, mock_category_service):
    # Arrange
    mock_category_service.create.side_effect = Exception("Service error")
    
    # Act
    response = client.post(
        "/category",
        json={
            "name": "Test Category",
            "type": CategoryType.EXPENSE
        }
    )
    
    # Assert
    assert response.status_code == 500

def test_create_category_unauthorized(client):
    # Arrange
    def mock_auth():
        raise HTTPException(status_code=401, detail="Invalid token")
    
    app.dependency_overrides[get_current_user] = mock_auth

    # Act
    response = client.post(
        "/category",
        json={
            "name": "Test Category",
            "type": CategoryType.EXPENSE
        }
    )
    
    # Assert
    assert response.status_code == 401