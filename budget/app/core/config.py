from pydantic_settings import BaseSettings

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

    class Config:
        env_file = ".env"

settings = Settings()