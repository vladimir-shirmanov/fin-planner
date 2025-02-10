from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SERVICE_NAME: str = "budget-service"
    echo_sql: bool = False
    debug_logs: bool = False
    auth_athority: str
    auth_token_url: str = auth_athority + "/protocol/openid-connect/token"
    auth_url: str = auth_athority + "/protocol/openid-connect/auth"
    auth_audience: str
    jwks_url: str = auth_athority + "/protocol/openid-connect/certs"

    class Config:
        env_file = ".env"

settings = Settings()