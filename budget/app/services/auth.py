from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from uuid import UUID
from jwt import PyJWKClient
import jwt
from typing import Annotated
from ..core.config import settings
from ..models.user import User
from ..dependencies.core import logger_dep

oauth_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl=settings.auth_token_url,
    authorizationUrl=settings.auth_url,
    refreshUrl=settings.auth_token_url
)

async def get_current_user(logger: logger_dep, token: str = Depends(oauth_scheme)) -> User:
    try:
        await logger.ainfo("BEGIN get_current_user", jwks_url=settings.jwks_url, auth_audience=settings.auth_audience)
        jwks_client = PyJWKClient(settings.jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        claims = jwt.decode(token, signing_key.key, algorithms=["RS256"], audience=settings.auth_audience)
        user = User(email=claims["email"], user_id=UUID(claims["sub"]))
        await logger.ainfo("END get_current_user", user=user)
        return user
    except Exception as e:
        logger.error("Invalid token", error=str(e))
        raise HTTPException(status_code=401, detail="Invalid token") from e
    
current_user_dep = Annotated[User, Depends(get_current_user)]