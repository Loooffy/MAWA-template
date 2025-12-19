"""State Accessor for Agent to access User and World State."""
from typing import Optional, List, Dict, Any
from app.state.user_state.manager import UserStateManager
from app.state.world_state.manager import WorldStateManager
from app.state.user_state.schemas import UserStateResponse
from app.state.world_state.schemas import WorldStateResponse


class StateAccessor:
    """Provides unified interface for Agent to access User and World State."""
    
    def __init__(
        self,
        user_state_manager: UserStateManager,
        world_state_manager: WorldStateManager,
    ):
        """Initialize State Accessor.
        
        Args:
            user_state_manager: User State Manager instance
            world_state_manager: World State Manager instance
        """
        self.user_state_manager = user_state_manager
        self.world_state_manager = world_state_manager
    
    # User State methods
    
    def get_user_state(self, user_id: str, key: str) -> Optional[Dict[str, Any]]:
        """Get user state by user ID and key.
        
        Args:
            user_id: User ID
            key: State key
            
        Returns:
            User state as dictionary, or None if not found
        """
        state = self.user_state_manager.get_by_user_and_key(user_id, key)
        if state:
            return state.model_dump()
        return None
    
    def get_user_states(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all user states for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of user states as dictionaries
        """
        states = self.user_state_manager.list_by_user(user_id)
        return [state.model_dump() for state in states]
    
    def set_user_state(self, user_id: str, key: str, value: str) -> Dict[str, Any]:
        """Set user state (create or update).
        
        Args:
            user_id: User ID
            key: State key
            value: State value
            
        Returns:
            Created or updated user state as dictionary
        """
        existing = self.user_state_manager.get_by_user_and_key(user_id, key)
        if existing:
            from app.state.user_state.schemas import UserStateUpdate
            updated = self.user_state_manager.update(
                existing.id,
                UserStateUpdate(value=value)
            )
            return updated.model_dump() if updated else {}
        else:
            from app.state.user_state.schemas import UserStateCreate
            created = self.user_state_manager.create(
                UserStateCreate(user_id=user_id, key=key, value=value)
            )
            return created.model_dump()
    
    # World State methods
    
    def get_world_state(self, key: str) -> Optional[Dict[str, Any]]:
        """Get world state by key.
        
        Args:
            key: State key
            
        Returns:
            World state as dictionary, or None if not found
        """
        state = self.world_state_manager.get_by_key(key)
        if state:
            return state.model_dump()
        return None
    
    def get_world_states(self) -> List[Dict[str, Any]]:
        """Get all world states.
        
        Returns:
            List of world states as dictionaries
        """
        states = self.world_state_manager.list_all()
        return [state.model_dump() for state in states]
    
    def set_world_state(self, key: str, value: str) -> Dict[str, Any]:
        """Set world state (create or update).
        
        Args:
            key: State key
            value: State value
            
        Returns:
            Created or updated world state as dictionary
        """
        existing = self.world_state_manager.get_by_key(key)
        if existing:
            from app.state.world_state.schemas import WorldStateUpdate
            updated = self.world_state_manager.update(
                existing.id,
                WorldStateUpdate(value=value)
            )
            return updated.model_dump() if updated else {}
        else:
            from app.state.world_state.schemas import WorldStateCreate
            created = self.world_state_manager.create(
                WorldStateCreate(key=key, value=value)
            )
            return created.model_dump()

