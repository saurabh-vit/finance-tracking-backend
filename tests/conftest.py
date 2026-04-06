"""
Test configuration and fixtures.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from database import Base


@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine."""
    engine = create_engine(settings.database_url.replace("finance.db", "test_finance.db"))
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def test_db(test_engine):
    """Create test database session."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
