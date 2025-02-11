from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SERVICE_NAME: str = "budget-service"
    echo_sql: bool = False
    debug_logs: bool = False
    auth_authority: str
    auth_token_url: str
    auth_url: str
    auth_audience: str
    jwks_url: str

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings_dep = Annotated[Settings, Depends(get_settings)]