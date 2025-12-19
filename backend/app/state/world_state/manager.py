"""World State Manager."""
import uuid
from typing import Optional, List
from app.db.storage.interface import StorageInterface
from app.state.world_state.schemas import WorldStateCreate, WorldStateUpdate, WorldStateResponse


class WorldStateManager:
    """Manager for World State operations."""
    
    TABLE_NAME = "world_states"
    
    def __init__(self, storage: StorageInterface):
        """Initialize World State Manager.
        
        Args:
            storage: Storage interface implementation
        """
        self.storage = storage
    
    def create(self, state: WorldStateCreate) -> WorldStateResponse:
        """Create a new world state.
        
        Args:
            state: World state data to create
            
        Returns:
            Created world state
        """
        data = {
            "id": str(uuid.uuid4()),
            "key": state.key,
            "value": state.value,
        }
        result = self.storage.create(self.TABLE_NAME, data)
        return WorldStateResponse(**result)
    
    def get(self, state_id: str) -> Optional[WorldStateResponse]:
        """Get world state by ID.
        
        Args:
            state_id: State ID
            
        Returns:
            World state if found, None otherwise
        """
        result = self.storage.get(self.TABLE_NAME, state_id)
        if result:
            return WorldStateResponse(**result)
        return None
    
    def get_by_key(self, key: str) -> Optional[WorldStateResponse]:
        """Get world state by key.
        
        Args:
            key: State key
            
        Returns:
            World state if found, None otherwise
        """
        results = self.storage.list(self.TABLE_NAME, filters={"key": key})
        if results:
            return WorldStateResponse(**results[0])
        return None
    
    def update(self, state_id: str, state: WorldStateUpdate) -> Optional[WorldStateResponse]:
        """Update world state.
        
        Args:
            state_id: State ID
            state: Updated state data
            
        Returns:
            Updated world state if found, None otherwise
        """
        data = {}
        if state.value is not None:
            data["value"] = state.value
        
        if not data:
            # No updates to apply
            return self.get(state_id)
        
        result = self.storage.update(self.TABLE_NAME, state_id, data)
        if result:
            return WorldStateResponse(**result)
        return None
    
    def update_by_key(self, key: str, state: WorldStateUpdate) -> Optional[WorldStateResponse]:
        """Update world state by key.
        
        Args:
            key: State key
            state: Updated state data
            
        Returns:
            Updated world state if found, None otherwise
        """
        existing = self.get_by_key(key)
        if not existing:
            return None
        return self.update(existing.id, state)
    
    def delete(self, state_id: str) -> bool:
        """Delete world state.
        
        Args:
            state_id: State ID
            
        Returns:
            True if deleted, False if not found
        """
        return self.storage.delete(self.TABLE_NAME, state_id)
    
    def list_all(self) -> List[WorldStateResponse]:
        """List all world states.
        
        Returns:
            List of all world states
        """
        results = self.storage.list(self.TABLE_NAME)
        return [WorldStateResponse(**result) for result in results]

