"""HTML dashboard routes using Jinja2 + HTMX."""
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import DatabaseDep
from app.models.webhook import Webhook
from app.models.project import Project
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Landing page - redirects to webhooks list or shows welcome."""
    # For MVP without login UI, we'll just render the list page.
    # In a real app we'd check session or redirect to login.
    # We will pass dummy data or expect query params for project context if needed.
    # Simplified: Render a basic 'Connect' or 'List' view.
    return templates.TemplateResponse("webhooks_list.html", {"request": request, "page": 1, "webhooks": [], "has_next": False})

@router.get("/webhooks", response_class=HTMLResponse)
def list_webhooks_html(
    request: Request,
    db: DatabaseDep,
    page: int = 1,
    # Auth is tricky for HTML views without a cookie session.
    # MVP: We'll skip strict auth for the PUBLIC dashboard demo
    # or assume a hardcoded 'demo' project exists.
    # Let's act as if we are listing latest global webhooks for the MVP 'personal' use case.
):
    limit = 20
    offset = (page - 1) * limit
    query = (
        db.query(Webhook)
        .order_by(Webhook.received_at.desc())
        .offset(offset)
        .limit(limit)
    )
    webhooks: List[Webhook] = query.all()
    return templates.TemplateResponse(
        "webhooks_list.html",
        {
            "request": request,
            "webhooks": webhooks,
            "page": page,
            "has_next": len(webhooks) == limit,
        },
    )

@router.get("/webhooks/{webhook_id}", response_class=HTMLResponse)
def webhook_detail_html(
    request: Request,
    webhook_id: str,
    db: DatabaseDep,
):
    webhook = db.query(Webhook).filter_by(id=webhook_id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return templates.TemplateResponse(
        "webhook_detail.html",
        {"request": request, "webhook": webhook},
    )

