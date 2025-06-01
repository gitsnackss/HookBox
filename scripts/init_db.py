"""Create initial admin project (run once)."""
from app.database import create_tables
from app.models.project import Project
from app.utils.id_generator import generate_id
import bcrypt, secrets

def main():
    print("Initializing database...")
    create_tables()
    
    # Check if admin project exists
    # Note: Using direct DB session here would be better but for a script standalone:
    from app.database import SessionLocal
    db = SessionLocal()
    
    existing = db.query(Project).filter_by(name="Admin").first()
    if existing:
        print("Admin project already exists.")
        return

    # Create Admin Project
    raw_key = secrets.token_urlsafe(32)
    proj = Project(
        id=generate_id("proj"),
        name="Admin",
        inbox_key=generate_id("inb"),
        api_key_hash=bcrypt.hashpw(raw_key.encode(), bcrypt.gensalt()).decode(),
        rate_limit_per_minute=1000,
    )
    db.add(proj)
    db.commit()
    print(f"Admin project created!")
    print(f"Inbox Key: {proj.inbox_key}")
    print(f"API Key:   {raw_key}")
    print("SAVE THIS API KEY! It cannot be retrieved later.")

if __name__ == "__main__":
    main()
