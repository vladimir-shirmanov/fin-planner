from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str | None
    SERVICE_NAME: str = "budget-service"
    echo_sql: bool = False
    debug_logs: bool = False
    auth_authority: str | None
    auth_token_url: str | None
    auth_url: str | None
    auth_audience: str | None
    jwks_url: str | None
    json_logs: bool = False

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings_dep = Annotated[Settings, Depends(get_settings)]