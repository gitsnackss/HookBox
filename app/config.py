"""Application configuration using pydantic‑settings."""
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Core
    database_url: str = Field(default="sqlite:///./hookbox.db")
    admin_api_key: str = Field(..., env="ADMIN_API_KEY")
    secret_key: str = Field(..., env="SECRET_KEY")

    # Logging
    log_level: str = Field(default="INFO")
    allowed_origins: List[str] = Field(default_factory=lambda: ["http://localhost:8000"])

    # Limits
    max_webhook_body_size: int = Field(default=1_048_576)  # 1 MiB

    # Replay
    default_replay_timeout: int = Field(default=10)
    max_replay_timeout: int = Field(default=30)
    block_private_ips: bool = Field(default=True)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
