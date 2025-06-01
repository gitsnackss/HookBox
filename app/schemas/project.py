"""Pydantic schemas for Project."""
from typing import List, Optional
from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    name: str = Field(..., max_length=100)
    allowed_replay_domains: Optional[List[str]] = None

class ProjectResponse(BaseModel):
    id: str
    name: str
    inbox_key: str
    api_key: str  # Only returned on creation
    allowed_replay_domains: Optional[List[str]] = None
    rate_limit_per_minute: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
