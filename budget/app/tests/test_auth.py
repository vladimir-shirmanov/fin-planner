from fastapi.security import OAuth2AuthorizationCodeBearer
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID
from fastapi import HTTPException
from jwt.exceptions import InvalidTokenError
from jwt import PyJWKClient
from ..services.auth import get_current_user, get_jwks_client

# Mock data
TEST_TOKEN = "test.jwt.token"
TEST_USER_ID = "9c699f45-8099-40e3-aca9-f023606cd5bb"
TEST_EMAIL = "test@example.com"
TEST_JWKS_URL = "http://keycloak:8080/auth/realms/test/protocol/openid-connect/certs"
TEST_AUDIENCE = "test-api"

@pytest.fixture
def mock_settings():
    settings = MagicMock()
    settings.jwks_url = TEST_JWKS_URL
    settings.auth_audience = TEST_AUDIENCE
    settings.auth_token_url = "http://auth/token"
    settings.auth_url = "http://auth/authorize"
    return settings

@pytest.fixture
def mock_logger():
    logger = AsyncMock()
    logger.ainfo = AsyncMock()
    logger.aerror = AsyncMock()
    return logger

@pytest.fixture
def mock_jwks_client():
    jwks_client = MagicMock()
    jwks_client.get_signing_key_from_jwt = MagicMock()
    return jwks_client

def test_get_jwks_client(mock_settings):
    """Test jwks client creation"""
    jwks_client = get_jwks_client(mock_settings)
    assert isinstance(jwks_client, PyJWKClient)

@pytest.mark.asyncio
async def test_get_current_user_success(mock_settings, mock_logger, mock_jwks_client):
    """Test successful user authentication"""
    # Arrange
    mock_signing_key = MagicMock()
    mock_signing_key.key = "test_key"
    mock_jwks_client.get_signing_key_from_jwt.return_value = mock_signing_key
    
    with patch('jwt.decode') as mock_decode:
        mock_decode.return_value = {
            "sub": TEST_USER_ID,
            "email": TEST_EMAIL
        }
        
        # Act
        user = await get_current_user(mock_settings, mock_logger, TEST_TOKEN, mock_jwks_client)
        
        # Assert
        assert user.user_id == UUID(TEST_USER_ID)
        assert user.email == TEST_EMAIL
        mock_jwks_client.get_signing_key_from_jwt.assert_called_once_with(TEST_TOKEN)

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(mock_settings, mock_logger, mock_jwks_client):
    """Test authentication with invalid token"""
    # Arrange
    mock_jwks_client.get_signing_key_from_jwt.side_effect = InvalidTokenError("Invalid token")
    
    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(mock_settings, mock_logger, TEST_TOKEN, mock_jwks_client)
    
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"
    mock_logger.aexception.assert_called_once()

@pytest.mark.asyncio
async def test_get_current_user_missing_claims(mock_settings, mock_logger, mock_jwks_client):
    """Test authentication with missing required claims"""
    # Arrange
    mock_signing_key = MagicMock()
    mock_signing_key.key = "test_key"
    mock_jwks_client.get_signing_key_from_jwt.return_value = mock_signing_key
    
    with patch('jwt.decode') as mock_decode:
        mock_decode.return_value = {}  # Missing required claims
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(mock_settings, mock_logger, TEST_TOKEN, mock_jwks_client)
        
        assert exc_info.value.status_code == 401
        mock_logger.aexception.assert_called_once()
