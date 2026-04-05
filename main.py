"""
Finance Tracking System — FastAPI application entry point.

Responsibilities:
  - Create the FastAPI app with metadata
  - Register all routers
  - Create DB tables on startup
  - Seed default users and sample transactions on first run
"""

import logging
from contextlib import asynccontextmanager
from datetime import date

from fastapi import FastAPI
from sqlalchemy.orm import Session

from finance_system.database import engine, SessionLocal
from finance_system.models import User, Transaction  # registers all ORM models with Base
from finance_system.database import Base
from finance_system.services.auth_service import hash_password
from finance_system.routers import auth, transactions, summary, users
from finance_system.schemas.transaction import HealthResponse


# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler("finance_system.log"),  # File output
    ],
)

logger = logging.getLogger(__name__)

_SEED_USERS = [
    {"username": "admin_user",   "email": "admin@finance.io",   "password": "admin123",   "role": "admin"},
    {"username": "analyst_user", "email": "analyst@finance.io", "password": "analyst123", "role": "analyst"},
    {"username": "viewer_user",  "email": "viewer@finance.io",  "password": "viewer123",  "role": "viewer"},
]

_SEED_TRANSACTIONS = [
    # admin_user transactions (mix across 2024-2025)
    {"amount": 50000.0, "type": "income",  "category": "salary",        "date": date(2025, 1, 1),  "notes": "January salary"},
    {"amount": 50000.0, "type": "income",  "category": "salary",        "date": date(2025, 2, 1),  "notes": "February salary"},
    {"amount": 50000.0, "type": "income",  "category": "salary",        "date": date(2025, 3, 1),  "notes": "March salary"},
    {"amount": 15000.0, "type": "income",  "category": "freelance",     "date": date(2025, 1, 15), "notes": "Web design project"},
    {"amount": 12000.0, "type": "income",  "category": "freelance",     "date": date(2025, 3, 20), "notes": "Mobile app contract"},
    {"amount": 8500.0,  "type": "expense", "category": "rent",          "date": date(2025, 1, 5),  "notes": "Monthly rent"},
    {"amount": 8500.0,  "type": "expense", "category": "rent",          "date": date(2025, 2, 5),  "notes": "Monthly rent"},
    {"amount": 8500.0,  "type": "expense", "category": "rent",          "date": date(2025, 3, 5),  "notes": "Monthly rent"},
    {"amount": 3200.0,  "type": "expense", "category": "food",          "date": date(2025, 1, 31), "notes": "Groceries & dining"},
    {"amount": 2900.0,  "type": "expense", "category": "food",          "date": date(2025, 2, 28), "notes": "Groceries & dining"},
    {"amount": 3100.0,  "type": "expense", "category": "food",          "date": date(2025, 3, 31), "notes": "Groceries & dining"},
    {"amount": 1200.0,  "type": "expense", "category": "transport",     "date": date(2025, 1, 20), "notes": "Fuel & metro"},
    {"amount": 4500.0,  "type": "expense", "category": "entertainment", "date": date(2025, 2, 14), "notes": "Valentine's dinner & movie"},
    {"amount": 2800.0,  "type": "expense", "category": "health",        "date": date(2025, 3, 10), "notes": "Gym membership + medicines"},
    {"amount": 45000.0, "type": "income",  "category": "salary",        "date": date(2024, 12, 1), "notes": "December 2024 salary"},
]


def _seed_database(db: Session) -> None:
    """Insert seed users and transactions only when the DB is empty."""
    if db.query(User).count() > 0:
        return  # Already seeded

    # Create users
    user_objects: dict[str, User] = {}
    for u in _SEED_USERS:
        user = User(
            username=u["username"],
            email=u["email"],
            hashed_password=hash_password(u["password"]),
            role=u["role"],
        )
        db.add(user)
        user_objects[u["username"]] = user

    db.flush()  # Assign IDs without committing

    # Attach all transactions to admin_user
    admin = user_objects["admin_user"]
    for t in _SEED_TRANSACTIONS:
        txn = Transaction(
            user_id=admin.id,
            amount=t["amount"],
            type=t["type"],
            category=t["category"],
            date=t["date"],
            notes=t.get("notes"),
        )
        db.add(txn)

    db.commit()
    print("✅  Database seeded with default users and sample transactions.")


# ---------------------------------------------------------------------------
# Application lifespan (replaces on_event which is deprecated)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        _seed_database(db)
    finally:
        db.close()
    yield
    # Shutdown (nothing special needed for SQLite)


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Finance Tracking System",
    description=(
        "REST API for managing personal financial records.\n\n"
        "## Quick Start\n"
        "1. **Login** via `POST /auth/login` with one of the seed users.\n"
        "2. Click **Authorize** (top-right) and paste your token.\n"
        "3. Explore the endpoints!\n\n"
        "### Seed credentials\n"
        "| Username | Password | Role |\n"
        "|---|---|---|\n"
        "| admin_user | admin123 | admin |\n"
        "| analyst_user | analyst123 | analyst |\n"
        "| viewer_user | viewer123 | viewer |"
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Register routers
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(summary.router)
app.include_router(users.router)


@app.get("/", response_model=HealthResponse, tags=["Health"], summary="Health check")
def health_check() -> HealthResponse:
    """Returns API status and application information."""
    return HealthResponse(status="ok", app="Finance Tracking System", version="1.0.0")
