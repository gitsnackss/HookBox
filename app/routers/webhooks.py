"""Webhooks CRUD + replay API."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.dependencies import DatabaseDep, ProjectDep
from app.models.webhook import Webhook
from app.models.project import Project
from app.schemas.webhook import WebhookListItem, WebhookDetail
from app.schemas.replay import ReplayRequest, ReplayResponse
from app.services.replay_service import replay_webhook

router = APIRouter()

@router.get(
    "/projects/{project_id}/webhooks",
    response_model=List[WebhookListItem],
)
def list_webhooks(
    project_id: str,
    db: DatabaseDep,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    project: ProjectDep = Depends(ProjectDep),
):
    # Ensure project access
    if project.id != project_id:
        raise HTTPException(status_code=403, detail="Not authorized for this project")

    offset = (page - 1) * limit
    query = (
        db.query(Webhook)
        .filter_by(project_id=project_id)
        .order_by(Webhook.received_at.desc())
        .offset(offset)
        .limit(limit)
    )
    results = query.all()
    return [
        WebhookListItem(
            id=w.id,
            method=w.method,
            path=w.path,
            received_at=w.received_at.isoformat(),
            content_type=w.content_type,
            body_preview=w.body[:200].decode(errors="replace") if w.body else None,
        )
        for w in results
    ]

@router.get(
    "/webhooks/{webhook_id}",
    response_model=WebhookDetail,
)
def get_webhook_detail(
    webhook_id: str,
    db: DatabaseDep,
    project: ProjectDep = Depends(ProjectDep),
):
    # Verify webhook belongs to authorized project
    webhook = db.query(Webhook).filter_by(id=webhook_id, project_id=project.id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    return WebhookDetail(
        id=webhook.id,
        method=webhook.method,
        path=webhook.path,
        headers=json.loads(webhook.headers),
        body=webhook.body.decode(errors="replace") if webhook.body else None,
        content_type=webhook.content_type,
        source_ip=webhook.source_ip,
        user_agent=webhook.user_agent,
        received_at=webhook.received_at.isoformat(),
    )

@router.post(
    "/webhooks/{webhook_id}/replay",
    response_model=ReplayResponse,
    status_code=200,
)
def replay_endpoint(
    webhook_id: str,
    payload: ReplayRequest,
    db: DatabaseDep,
    project: ProjectDep = Depends(ProjectDep),
):
    webhook = db.query(Webhook).filter_by(id=webhook_id, project_id=project.id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    replay = replay_webhook(
        db=db,
        webhook=webhook,
        target_url=str(payload.target_url),
        include_original_headers=payload.include_original_headers,
        timeout=payload.timeout_seconds,
    )
    return ReplayResponse(
        replay_id=replay.id,
        target_url=replay.target_url,
        status_code=replay.response_status_code,
        response_time_ms=replay.response_time_ms,
        error=replay.error,
        replayed_at=replay.replayed_at.isoformat(),
    )
