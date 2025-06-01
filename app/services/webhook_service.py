"""Business logic for storing and retrieving webhooks."""
import json
from datetime import datetime
from app.utils.id_generator import generate_id
from app.models.project import Project
from app.models.webhook import Webhook
from sqlalchemy.orm import Session

async def store_webhook(
    db: Session,
    project: Project,
    method: str,
    path: str,
    headers: dict,
    body: bytes,
    source_ip: str | None = None,
    user_agent: str | None = None,
) -> Webhook:
    webhook = Webhook(
        id=generate_id("wh"),
        project_id=project.id,
        method=method,
        path=path,
        headers=json.dumps(headers),
        body=body,
        content_type=headers.get("content-type"),
        source_ip=source_ip,
        user_agent=user_agent,
        received_at=datetime.utcnow(),
    )
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook
