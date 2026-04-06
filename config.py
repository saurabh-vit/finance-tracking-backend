"""
Application configuration settings.
All sensitive values are loaded from environment variables for security.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


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
    seed_demo_data: bool = False
    bootstrap_admin_username: str | None = None
    bootstrap_admin_email: str | None = None
    bootstrap_admin_password: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


# Global settings instance
settings = Settings()
