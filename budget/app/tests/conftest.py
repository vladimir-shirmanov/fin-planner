import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
def mock_logger():
    logger = AsyncMock()
    logger.ainfo = AsyncMock()
    logger.aerror = AsyncMock()
    return logger


@pytest.fixture
def mock_db():
    """Mock database session"""
    db = AsyncMock(spec=AsyncSession)
    db.add = MagicMock()
    db.add_all = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.refresh.side_effect = lambda x: setattr(x, "id", 1)
    db.rollback = AsyncMock()
    return db