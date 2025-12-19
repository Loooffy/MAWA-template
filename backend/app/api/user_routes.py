"""User State API routes."""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.state.user_state.manager import UserStateManager
from app.state.user_state.schemas import (
    UserStateCreate,
    UserStateUpdate,
    UserStateResponse,
)
from app.dependencies import get_user_state_manager

router = APIRouter(prefix="/api/user-states", tags=["user-states"])


@router.post("", response_model=UserStateResponse, status_code=201)
async def create_user_state(
    state: UserStateCreate,
    manager: UserStateManager = Depends(get_user_state_manager),
):
    """Create a new user state."""
    try:
        return manager.create(state)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{state_id}", response_model=UserStateResponse)
async def get_user_state(
    state_id: str,
    manager: UserStateManager = Depends(get_user_state_manager),
):
    """Get user state by ID."""
    state = manager.get(state_id)
    if not state:
        raise HTTPException(status_code=404, detail="User state not found")
    return state


@router.get("/user/{user_id}", response_model=List[UserStateResponse])
async def list_user_states(
    user_id: str,
    manager: UserStateManager = Depends(get_user_state_manager),
):
    """List all user states for a user."""
    return manager.list_by_user(user_id)


@router.put("/{state_id}", response_model=UserStateResponse)
async def update_user_state(
    state_id: str,
    state: UserStateUpdate,
    manager: UserStateManager = Depends(get_user_state_manager),
):
    """Update user state."""
    updated = manager.update(state_id, state)
    if not updated:
        raise HTTPException(status_code=404, detail="User state not found")
    return updated


@router.delete("/{state_id}", status_code=204)
async def delete_user_state(
    state_id: str,
    manager: UserStateManager = Depends(get_user_state_manager),
):
    """Delete user state."""
    deleted = manager.delete(state_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User state not found")
    return None

