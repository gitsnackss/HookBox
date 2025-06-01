"""Pydantic schemas for Replay."""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, field_validator

class ReplayRequest(BaseModel):
    target_url: HttpUrl
    include_original_headers: bool = True
    timeout_seconds: int = Field(default=10, ge=1, le=30)

    @field_validator("timeout_seconds")
    @classmethod
    def within_limits(cls, v: int) -> int:
        if v < 1 or v > 30:
            raise ValueError("Timeout must be between 1 and 30 seconds")
        return v

class ReplayResponse(BaseModel):
    replay_id: str
    target_url: str
    status_code: Optional[int] = None
    response_time_ms: Optional[int] = None
    error: Optional[str] = None
    replayed_at: str

    class Config:
        from_attributes = True
