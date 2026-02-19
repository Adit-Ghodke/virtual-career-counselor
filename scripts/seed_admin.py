"""
Seed an admin user into the Users table.
Run: python scripts/seed_admin.py
"""
import os
import sys
from typing import Any, Dict, Optional
import bcrypt
from dotenv import load_dotenv  # type: ignore[import-untyped]

# Ensure project root is on sys.path so 'app' package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

load_dotenv()

# We need an app context for dynamo_service helpers
from app import create_app
from app.services.dynamo_service import create_user, get_user_by_email

app = create_app()

ADMIN_EMAIL: str = os.environ.get("ADMIN_EMAIL", "admin@example.com") or "admin@example.com"
ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD", "admin123") or "admin123"
ADMIN_NAME: str = "Admin"

with app.app_context():
    existing: Optional[Dict[str, Any]] = get_user_by_email(ADMIN_EMAIL)
    if existing:
        print(f"Admin user already exists: {ADMIN_EMAIL}")
    else:
        hashed: str = bcrypt.hashpw(ADMIN_PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user: Dict[str, Any] = create_user(name=ADMIN_NAME, email=ADMIN_EMAIL, password_hash=hashed, role="admin")
        print(f"✅ Admin user created: {ADMIN_EMAIL} (user_id: {user['user_id']})")
