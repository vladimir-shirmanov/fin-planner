from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from uuid import UUID
from jwt import PyJWKClient
import jwt
from typing import Annotated
from ..core.config import settings_dep
from ..models.user import User
from ..dependencies.core import get_logger
from structlog.stdlib import BoundLogger

def get_auth_scheme(settings=settings_dep) -> OAuth2AuthorizationCodeBearer:
    return OAuth2AuthorizationCodeBearer(
        tokenUrl=settings.auth_token_url,
        authorizationUrl=settings.auth_url,
        refreshUrl=settings.auth_token_url
    )

def get_jwks_client(settings: settings_dep) -> PyJWKClient:
    return PyJWKClient(settings.jwks_url)

async def get_current_user(
        settings: settings_dep, 
        logger: BoundLogger =  Depends(get_logger),
        token: str = Depends(get_auth_scheme),
        jwks_client: PyJWKClient = Depends(get_jwks_client)) -> User:
    try:
        await logger.ainfo("BEGIN get_current_user", jwks_url=settings.jwks_url, auth_audience=settings.auth_audience)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        claims = jwt.decode(token, signing_key.key, algorithms=["RS256"], audience=settings.auth_audience)
        user = User(email=claims["email"], user_id=UUID(claims["sub"]))
        await logger.ainfo("END get_current_user", user=user)
        return user
    except Exception as e:
        await logger.aerror("Invalid token", error=str(e))
        raise HTTPException(status_code=401, detail="Invalid token") from e
    
current_user_dep = Annotated[User, Depends(get_current_user)]