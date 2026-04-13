"""User Service configuration."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """User Service settings."""

    service_name: str = "user_service"
    service_port: int = 8001

    class Config:
        env_prefix = "USER_SERVICE_"


settings = Settings()
