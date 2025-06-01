"""API‑key authentication service."""
import bcrypt
from sqlalchemy.orm import Session
from app.models.project import Project

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def verify_api_key(self, api_key: str) -> Project | None:
        """Return the project matching the given API key, or None."""
        projects = self.db.query(Project).all()
        for proj in projects:
            if bcrypt.checkpw(api_key.encode(), proj.api_key_hash.encode()):
                return proj
        return None
