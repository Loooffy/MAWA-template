"""User State Manager."""
import uuid
from typing import Optional, List
from app.db.storage.interface import StorageInterface
from app.state.user_state.schemas import UserStateCreate, UserStateUpdate, UserStateResponse


class UserStateManager:
    """Manager for User State operations."""
    
    TABLE_NAME = "user_states"
    
    def __init__(self, storage: StorageInterface):
        """Initialize User State Manager.
        
        Args:
            storage: Storage interface implementation
        """
        self.storage = storage
    
    def create(self, state: UserStateCreate) -> UserStateResponse:
        """Create a new user state.
        
        Args:
            state: User state data to create
            
        Returns:
            Created user state
        """
        data = {
            "id": str(uuid.uuid4()),
            "user_id": state.user_id,
            "key": state.key,
            "value": state.value,
        }
        result = self.storage.create(self.TABLE_NAME, data)
        return UserStateResponse(**result)
    
    def get(self, state_id: str) -> Optional[UserStateResponse]:
        """Get user state by ID.
        
        Args:
            state_id: State ID
            
        Returns:
            User state if found, None otherwise
        """
        result = self.storage.get(self.TABLE_NAME, state_id)
        if result:
            return UserStateResponse(**result)
        return None
    
    def get_by_user_and_key(self, user_id: str, key: str) -> Optional[UserStateResponse]:
        """Get user state by user ID and key.
        
        Args:
            user_id: User ID
            key: State key
            
        Returns:
            User state if found, None otherwise
        """
        results = self.storage.list(self.TABLE_NAME, filters={"user_id": user_id, "key": key})
        if results:
            return UserStateResponse(**results[0])
        return None
    
    def list_by_user(self, user_id: str) -> List[UserStateResponse]:
        """List all user states for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of user states
        """
        results = self.storage.list(self.TABLE_NAME, filters={"user_id": user_id})
        return [UserStateResponse(**result) for result in results]
    
    def update(self, state_id: str, state: UserStateUpdate) -> Optional[UserStateResponse]:
        """Update user state.
        
        Args:
            state_id: State ID
            state: Updated state data
            
        Returns:
            Updated user state if found, None otherwise
        """
        data = {}
        if state.value is not None:
            data["value"] = state.value
        
        if not data:
            # No updates to apply
            return self.get(state_id)
        
        result = self.storage.update(self.TABLE_NAME, state_id, data)
        if result:
            return UserStateResponse(**result)
        return None
    
    def delete(self, state_id: str) -> bool:
        """Delete user state.
        
        Args:
            state_id: State ID
            
        Returns:
            True if deleted, False if not found
        """
        return self.storage.delete(self.TABLE_NAME, state_id)
    
    def list_all(self) -> List[UserStateResponse]:
        """List all user states.
        
        Returns:
            List of all user states
        """
        results = self.storage.list(self.TABLE_NAME)
        return [UserStateResponse(**result) for result in results]

