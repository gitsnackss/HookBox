"""Project management API (admin‑only)."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import secrets
import bcrypt

from app.dependencies import DatabaseDep, AdminAuthDep
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse
from app.utils.id_generator import generate_id

router = APIRouter()

@router.post("/projects", response_model=ProjectResponse, status_code=201)
def create_project(
    payload: ProjectCreate,
    db: DatabaseDep,
    _: bool = Depends(AdminAuthDep),
):
    # Generate IDs & keys
    project_id = generate_id("proj")
    inbox_key = generate_id("inb")
    raw_api_key = secrets.token_urlsafe(32)
    # Hash API key
    api_key_hash = bcrypt.hashpw(raw_api_key.encode(), bcrypt.gensalt()).decode()

    # Create project
    # Note: Allowed domains stored as comma-separated string for simplicity in MVP SQLite
    allowed_domains_str = ",".join(payload.allowed_replay_domains or []) if payload.allowed_replay_domains else None

    project = Project(
        id=project_id,
        name=payload.name,
        inbox_key=inbox_key,
        api_key_hash=api_key_hash,
        allowed_replay_domains=allowed_domains_str,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    return ProjectResponse(
        id=project.id,
        name=project.name,
        inbox_key=project.inbox_key,
        api_key=raw_api_key,
        allowed_replay_domains=payload.allowed_replay_domains,
        rate_limit_per_minute=project.rate_limit_per_minute,
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat(),
    )
