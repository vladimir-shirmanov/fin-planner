﻿from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SERVICE_NAME: str = "budget-service"
    echo_sql: bool = False
    debug_logs: bool = False

    class Config:
        env_file = ".env"

settings = Settings()