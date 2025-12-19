"""FastAPI dependencies."""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.base import get_storage_type
from app.db.storage import MemoryStorage, SQLiteStorage, PostgreSQLStorage
from app.db.storage.interface import StorageInterface
from app.state.user_state.manager import UserStateManager
from app.state.world_state.manager import WorldStateManager
from app.state.state_accessor import StateAccessor


def get_storage(db: Session = Depends(get_db)) -> StorageInterface:
    """Get storage implementation based on configuration."""
    storage_type = get_storage_type()
    
    if storage_type == "memory":
        return MemoryStorage()
    elif storage_type == "sqlite":
        return SQLiteStorage(db)
    elif storage_type == "postgresql":
        return PostgreSQLStorage(db)
    else:
        # Default to memory
        return MemoryStorage()


def get_user_state_manager(
    storage: StorageInterface = Depends(get_storage),
) -> UserStateManager:
    """Get User State Manager instance."""
    return UserStateManager(storage)


def get_world_state_manager(
    storage: StorageInterface = Depends(get_storage),
) -> WorldStateManager:
    """Get World State Manager instance."""
    return WorldStateManager(storage)


def get_state_accessor(
    user_state_manager: UserStateManager = Depends(get_user_state_manager),
    world_state_manager: WorldStateManager = Depends(get_world_state_manager),
) -> StateAccessor:
    """Get State Accessor instance."""
    return StateAccessor(user_state_manager, world_state_manager)

