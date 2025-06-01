"""Pydantic schemas for Webhook."""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class WebhookCreate(BaseModel):
    # No body – ingestion endpoint captures raw request
    pass

class WebhookListItem(BaseModel):
    id: str
    method: str
    path: str
    status_code: int = Field(default=202)
    received_at: str
    content_type: Optional[str] = None
    body_preview: Optional[str] = None

    class Config:
        from_attributes = True

class WebhookDetail(BaseModel):
    id: str
    method: str
    path: str
    headers: Dict[str, Any]
    body: Optional[str] = None  # Base64‑encoded if binary
    content_type: Optional[str] = None
    source_ip: Optional[str] = None
    user_agent: Optional[str] = None
    received_at: str

    class Config:
        from_attributes = True
