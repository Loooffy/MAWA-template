"""In-memory storage implementation."""
import uuid
from typing import Optional, List, Dict, Any
from app.db.storage.interface import StorageInterface


class MemoryStorage(StorageInterface):
    """In-memory storage for development and testing."""
    
    def __init__(self):
        """Initialize in-memory storage."""
        self._storage: Dict[str, Dict[str, Dict[str, Any]]] = {}
    
    def _ensure_table(self, table: str):
        """Ensure table exists in storage."""
        if table not in self._storage:
            self._storage[table] = {}
    
    def create(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record."""
        self._ensure_table(table)
        
        # Generate ID if not provided
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        
        record_id = data["id"]
        self._storage[table][record_id] = data.copy()
        return self._storage[table][record_id]
    
    def get(self, table: str, id: str) -> Optional[Dict[str, Any]]:
        """Get a record by ID."""
        self._ensure_table(table)
        return self._storage[table].get(id)
    
    def update(self, table: str, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record."""
        self._ensure_table(table)
        
        if id not in self._storage[table]:
            return None
        
        # Update fields
        self._storage[table][id].update(data)
        return self._storage[table][id]
    
    def delete(self, table: str, id: str) -> bool:
        """Delete a record."""
        self._ensure_table(table)
        
        if id in self._storage[table]:
            del self._storage[table][id]
            return True
        return False
    
    def list(self, table: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """List records with optional filters."""
        self._ensure_table(table)
        
        records = list(self._storage[table].values())
        
        if filters:
            filtered_records = []
            for record in records:
                match = True
                for key, value in filters.items():
                    if record.get(key) != value:
                        match = False
                        break
                if match:
                    filtered_records.append(record)
            return filtered_records
        
        return records

