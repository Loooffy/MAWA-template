"""Database session management for FastAPI."""
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.base import SessionLocal


def get_db() -> Session:
    """FastAPI dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

