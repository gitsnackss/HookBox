"""FastAPI dependencies for auth and DB."""
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.project import Project
from app.services.auth_service import AuthService

DatabaseDep = Annotated[Session, Depends(get_db)]
AuthorizationDep = Annotated[str, Header()]

def get_current_project(
    authorization: AuthorizationDep,
    db: DatabaseDep,
) -> Project:
    """Validate API key and return the associated project."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Use 'Bearer {api_key}'",
        )
    api_key = authorization.replace("Bearer ", "")
    auth_service = AuthService(db)
    project = auth_service.verify_api_key(api_key)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return project

def verify_admin_key(authorization: AuthorizationDep) -> bool:
    """Validate admin API key."""
    from app.config import settings

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format",
        )
    api_key = authorization.replace("Bearer ", "")
    if api_key != settings.admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin API key",
        )
    return True

ProjectDep = Annotated[Project, Depends(get_current_project)]
AdminAuthDep = Annotated[bool, Depends(verify_admin_key)]
