from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from uuid import UUID
import jwt
from jwt import PyJWKClient
from typing import Annotated
from ...domain.configs.config import settings_dep, get_settings
from ...domain.schemas.user import User
from ...application.dependencies.core import NamedLogger
from structlog.stdlib import BoundLogger

settings = get_settings()
auth_scheme = OAuth2AuthorizationCodeBearer(
        tokenUrl=settings.auth_token_url,
        authorizationUrl=settings.auth_url,
        refreshUrl=settings.auth_token_url
    )

def get_jwks_client(settings: settings_dep) -> PyJWKClient:
    return PyJWKClient(settings.jwks_url)

async def get_current_user(
        settings: settings_dep, 
        logger: BoundLogger =  Depends(NamedLogger('auth')),
        token:str = Depends(auth_scheme),
        jwks_client: PyJWKClient = Depends(get_jwks_client)) -> User:
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        claims = jwt.decode(token, signing_key.key, algorithms=["RS256"], audience=settings.auth_audience)
        user = User(email=claims["email"], user_id=UUID(claims["sub"]))
        return user
    except Exception as e:
        await logger.aexception("Invalid token", exc_info=e)
        raise HTTPException(status_code=401, detail="Invalid token") from e
    
current_user_dep = Annotated[User, Depends(get_current_user)]