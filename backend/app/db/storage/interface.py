"""Storage interface abstraction."""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class StorageInterface(ABC):
    """Abstract interface for storage implementations."""
    
    @abstractmethod
    def create(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record.
        
        Args:
            table: Table name (e.g., 'user_states', 'world_states')
            data: Dictionary containing record data
            
        Returns:
            Created record as dictionary
        """
        pass
    
    @abstractmethod
    def get(self, table: str, id: str) -> Optional[Dict[str, Any]]:
        """Get a record by ID.
        
        Args:
            table: Table name
            id: Record ID
            
        Returns:
            Record as dictionary, or None if not found
        """
        pass
    
    @abstractmethod
    def update(self, table: str, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record.
        
        Args:
            table: Table name
            id: Record ID
            data: Dictionary containing fields to update
            
        Returns:
            Updated record as dictionary, or None if not found
        """
        pass
    
    @abstractmethod
    def delete(self, table: str, id: str) -> bool:
        """Delete a record.
        
        Args:
            table: Table name
            id: Record ID
            
        Returns:
            True if deleted, False if not found
        """
        pass
    
    @abstractmethod
    def list(self, table: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """List records with optional filters.
        
        Args:
            table: Table name
            filters: Optional dictionary of filters (e.g., {'user_id': '123'})
            
        Returns:
            List of records as dictionaries
        """
        pass

