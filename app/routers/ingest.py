"""Public webhook ingestion endpoint."""
from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.dependencies import DatabaseDep
from app.models.project import Project
from app.services.webhook_service import store_webhook
from app.utils.id_generator import generate_id

router = APIRouter()

@router.post("/i/{project_key}", status_code=status.HTTP_202_ACCEPTED)
async def ingest_webhook(
    project_key: str,
    request: Request,
    db: DatabaseDep,
):
    # Find project by inbox_key
    project = db.query(Project).filter_by(inbox_key=project_key).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Enforce body size limit (basic check, simplified for MVP)
    # Note: request.body() loads fully into memory. For large files we'd stream,
    # but 1MB limit makes this safe enough.
    body = await request.body()
    if len(body) > 1_048_576:  # Hard‑coded limit from settings
        raise HTTPException(status_code=413, detail="Payload too large")

    # Store webhook
    webhook = await store_webhook(
        db=db,
        project=project,
        method=request.method,
        path=str(request.url.path),
        headers=dict(request.headers),
        body=body,
        source_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    return {"id": webhook.id, "received_at": webhook.received_at.isoformat()}
