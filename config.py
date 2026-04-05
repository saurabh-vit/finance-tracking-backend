"""
Application configuration settings.
All sensitive values are loaded from environment variables for security.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses .env file for local development and system env vars in production.
    """
    # JWT Configuration
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database Configuration
    database_url: str = "sqlite:///./finance.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instantiate settings to be imported by other modules
settings = Settings()


# Global settings instance
settings = Settings()
