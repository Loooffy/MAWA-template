"""SQLAlchemy Base and Engine configuration."""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Create engine
if DATABASE_URL.startswith("sqlite"):
    # SQLite specific configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,
    )
else:
    # PostgreSQL or other databases
    engine = create_engine(DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()


def get_storage_type() -> str:
    """Determine storage type from DATABASE_URL or STORAGE_TYPE env var."""
    storage_type = os.getenv("STORAGE_TYPE")
    if storage_type:
        return storage_type.lower()
    
    if DATABASE_URL.startswith("sqlite"):
        return "sqlite"
    elif DATABASE_URL.startswith("postgresql"):
        return "postgresql"
    else:
        return "memory"

