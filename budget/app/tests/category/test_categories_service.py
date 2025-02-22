from pydantic import ValidationError
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID
import uuid

from ...domain.schemas import User, CategoryCreate, CategoryResponse, CategoryType
from ...infrastructure.database.models import Category
from ...application.services import CategoryService

@pytest.fixture
def category_service(mock_db, mock_logger):
    return CategoryService(mock_db, mock_logger)

@pytest.mark.asyncio
async def test_create_category_invalid_data():
    """Test create_category with invalid data should raise ValidationError"""
    invalid_data = {
        "name": "",
        "type": 999,
    }

    with pytest.raises(ValidationError) as exc_info:
        CategoryCreate(**invalid_data)
    
    errors = exc_info.value.errors()
    assert len(errors) == 2
    
    error_types = {(error["loc"][0], error["type"]) for error in errors}
    assert ("name", "string_too_short") in error_types
    assert ("type", "enum") in error_types



@pytest.mark.asyncio
async def test_create_category(category_service):
    """Test create_category with valid data should return CategoryResponse"""
    # Arrange
    category_create = CategoryCreate(
        name="Test Category",
        type=CategoryType.EXPENSE,
        parent_category_id=None
    )
    user = User(user_id=uuid.uuid4(), email='s')

    # Act
    result = await category_service.create(category_create, user.user_id)

    # Assert
    assert isinstance(result, CategoryResponse)
    assert result.name == "Test Category"
    assert result.type == CategoryType.EXPENSE
    assert isinstance(result.user_id, UUID)
    
    # Verify DB calls
    category_service.db.add.assert_called_once()
    category_service.db.commit.assert_called_once()
    category_service.db.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_get_categories(category_service):
    """Test get_categories should return list of CategoryResponse"""
    # Arrange
    mock_categories = [
        Category(
            id=1,
            name="Category 1",
            type=CategoryType.EXPENSE,
            user_id=UUID('12345678-1234-5678-1234-567812345678')
        ),
        Category(
            id=2,
            name="Category 2",
            type=CategoryType.WANTS,
            user_id=UUID('12345678-1234-5678-1234-567812345679')
        )
    ]
    user_id = UUID('12345678-1234-5678-1234-567812345678')
    mock_result = AsyncMock()
    mock_scalars = AsyncMock()
    mock_result.scalars = MagicMock(return_value=mock_scalars)
    mock_scalars.all = MagicMock(return_value=mock_categories)

    category_service.db.execute.return_value = mock_result

    # Act
    result = await category_service.get(user_id)

    # Assert
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, CategoryResponse) for item in result)
    assert result[0].name == "Category 1"
    assert result[1].name == "Category 2"
    
    # Verify DB calls
    category_service.db.execute.assert_called_once()

@pytest.mark.asyncio
async def test_create_category_with_parent(category_service):
    """Test create_category with parent category should return CategoryResponse"""
    # Arrange
    category_create = CategoryCreate(
        name="Child Category",
        type=CategoryType.EXPENSE,
        parent_category_id=1,
    )
    user = User(user_id=uuid.uuid4(), email='s')

    # Act
    result = await category_service.create(category_create, user.user_id)

    # Assert
    assert isinstance(result, CategoryResponse)
    assert result.name == "Child Category"
    assert result.parent_category_id == 1

@pytest.mark.asyncio
async def test_get_categories_empty(category_service):
    """Test get_categories with no data should return empty list"""
    # Arrange
    mock_result = AsyncMock()
    mock_scalars = AsyncMock()
    mock_result.scalars = MagicMock(return_value=mock_scalars)
    mock_scalars.all = MagicMock(return_value=[])
    user_id = uuid.uuid4()
    category_service.db.execute.return_value = mock_result

    # Act
    result = await category_service.get(user_id)

    # Assert
    assert isinstance(result, list)
    assert len(result) == 0
