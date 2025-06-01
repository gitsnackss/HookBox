"""Project ORM model."""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Integer, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.webhook import Webhook

class Project(Base):
    __tablename__ = "projects"

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    inbox_key = Column(String(100), unique=True, nullable=False, index=True)
    api_key_hash = Column(String(100), nullable=False)
    allowed_replay_domains = Column(Text, nullable=True)  # JSON array
    rate_limit_per_minute = Column(Integer, default=60)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    webhooks = relationship(
        "Webhook", back_populates="project", cascade="all, delete-orphan"
    )
