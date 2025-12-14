# /packages/domain/db.py
import os
from sqlalchemy.orm import declarative_base, Session, mapped_column
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, UUID as PG_UUID
from sqlalchemy import create_engine, DateTime, Text
from uuid import uuid4
from datetime import datetime

Base = declarative_base()


class Blueprint(Base):
    """SQLAlchemy model for storing generated baby budget blueprints."""
    __tablename__ = "blueprints"

    id = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_profile = mapped_column(JSONB)
    blueprint_json = mapped_column(JSONB)
    assumptions_version = mapped_column(Text)
    calculator_version = mapped_column(Text)
    created_at = mapped_column(DateTime, default=datetime.utcnow)
    warnings = mapped_column(ARRAY(Text))
    pdf_url = mapped_column(Text, nullable=True)


# Database connection setup
def get_database_url():
    """Get database URL from environment or use default for local development."""
    return os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://nestworth:nestworth123@localhost:5432/nestworth"
    )


def create_db_engine():
    """Create SQLAlchemy engine."""
    return create_engine(get_database_url(), future=True, pool_pre_ping=True)


def get_session():
    """Create a new database session."""
    engine = create_db_engine()
    return Session(engine)


def init_db():
    """Initialize database tables."""
    engine = create_db_engine()
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")


# Global session for simple use cases (can be replaced with dependency injection in FastAPI)
engine = None
session = None

try:
    engine = create_db_engine()
    session = Session(engine)
except Exception as e:
    print(f"Warning: Could not connect to database: {e}")
    print("Database operations will fail. Ensure PostgreSQL is running.")
