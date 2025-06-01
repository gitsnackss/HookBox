"""Replay ORM model."""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, func
from app.database import Base

if TYPE_CHECKING:
    from app.models.webhook import Webhook

class Replay(Base):
    __tablename__ = "replays"

    id = Column(String(50), primary_key=True)
    webhook_id = Column(String(50), ForeignKey("webhooks.id", ondelete="CASCADE"), nullable=False, index=True)
    target_url = Column(String(1000), nullable=False)
    request_headers = Column(Text, nullable=True)  # JSON
    request_body = Column(Text, nullable=True)     # Stored as base64 string if needed
    response_status_code = Column(Integer, nullable=True)
    response_headers = Column(Text, nullable=True)  # JSON
    response_body = Column(Text, nullable=True)    # First 10 KB
    response_time_ms = Column(Integer, nullable=True)
    error = Column(Text, nullable=True)
    replayed_at = Column(DateTime, server_default=func.now())

    webhook = relationship("Webhook", back_populates="replays")
