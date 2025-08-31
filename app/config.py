"""Application configuration using pydantic‑settings."""
from typing import List

import bcrypt
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Core
    database_url: str = Field(default="sqlite:///./hookbox.db")
    admin_api_key_hash: str = Field(..., env="ADMIN_API_KEY_HASH", description="Bcrypt hash of admin API key")
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
    def validate_admin_key(self, key: str) -> bool:
        """Validate plaintext key against stored bcrypt hash (constant-time comparison)."""
        try:
            return bcrypt.checkpw(key.encode(), self.admin_api_key_hash.encode())
        except (ValueError, TypeError):
            return False

settings = Settings()

