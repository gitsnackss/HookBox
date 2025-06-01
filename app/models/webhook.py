"""Webhook ORM model."""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Text, LargeBinary, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.replay import Replay

class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(String(50), primary_key=True)
    project_id = Column(String(50), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    method = Column(String(10), nullable=False)
    path = Column(String(500), nullable=False)
    headers = Column(Text, nullable=False)  # JSON string
    body = Column(LargeBinary, nullable=True)
    content_type = Column(String(200), nullable=True)
    source_ip = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    received_at = Column(DateTime, server_default=func.now(), index=True)

    project = relationship("Project", back_populates="webhooks")
    replays = relationship(
        "Replay", back_populates="webhook", cascade="all, delete-orphan"
    )
