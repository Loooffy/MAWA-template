"""PostgreSQL storage implementation."""
import uuid
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.db.storage.interface import StorageInterface
from app.db.models.user_state import UserState
from app.db.models.world_state import WorldState


class PostgreSQLStorage(StorageInterface):
    """PostgreSQL storage implementation using SQLAlchemy."""
    
    def __init__(self, db: Session):
        """Initialize PostgreSQL storage with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self._model_map = {
            "user_states": UserState,
            "world_states": WorldState,
        }
    
    def _model_to_dict(self, model) -> Dict[str, Any]:
        """Convert SQLAlchemy model to dictionary."""
        return {
            "id": model.id,
            **{k: v for k, v in model.__dict__.items() if not k.startswith("_")}
        }
    
    def create(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record."""
        if table not in self._model_map:
            raise ValueError(f"Unknown table: {table}")
        
        Model = self._model_map[table]
        
        # Generate ID if not provided
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        
        model = Model(**data)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_dict(model)
    
    def get(self, table: str, id: str) -> Optional[Dict[str, Any]]:
        """Get a record by ID."""
        if table not in self._model_map:
            raise ValueError(f"Unknown table: {table}")
        
        Model = self._model_map[table]
        model = self.db.query(Model).filter(Model.id == id).first()
        
        if model:
            return self._model_to_dict(model)
        return None
    
    def update(self, table: str, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record."""
        if table not in self._model_map:
            raise ValueError(f"Unknown table: {table}")
        
        Model = self._model_map[table]
        model = self.db.query(Model).filter(Model.id == id).first()
        
        if not model:
            return None
        
        # Update fields
        for key, value in data.items():
            if hasattr(model, key):
                setattr(model, key, value)
        
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_dict(model)
    
    def delete(self, table: str, id: str) -> bool:
        """Delete a record."""
        if table not in self._model_map:
            raise ValueError(f"Unknown table: {table}")
        
        Model = self._model_map[table]
        model = self.db.query(Model).filter(Model.id == id).first()
        
        if not model:
            return False
        
        self.db.delete(model)
        self.db.commit()
        return True
    
    def list(self, table: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """List records with optional filters."""
        if table not in self._model_map:
            raise ValueError(f"Unknown table: {table}")
        
        Model = self._model_map[table]
        query = self.db.query(Model)
        
        if filters:
            for key, value in filters.items():
                if hasattr(Model, key):
                    query = query.filter(getattr(Model, key) == value)
        
        models = query.all()
        return [self._model_to_dict(model) for model in models]

