"""World State API routes."""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.state.world_state.manager import WorldStateManager
from app.state.world_state.schemas import (
    WorldStateCreate,
    WorldStateUpdate,
    WorldStateResponse,
)
from app.dependencies import get_world_state_manager

router = APIRouter(prefix="/api/world-states", tags=["world-states"])


@router.post("", response_model=WorldStateResponse, status_code=201)
async def create_world_state(
    state: WorldStateCreate,
    manager: WorldStateManager = Depends(get_world_state_manager),
):
    """Create a new world state."""
    try:
        return manager.create(state)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[WorldStateResponse])
async def list_world_states(
    manager: WorldStateManager = Depends(get_world_state_manager),
):
    """List all world states."""
    return manager.list_all()


@router.get("/{state_id}", response_model=WorldStateResponse)
async def get_world_state(
    state_id: str,
    manager: WorldStateManager = Depends(get_world_state_manager),
):
    """Get world state by ID."""
    state = manager.get(state_id)
    if not state:
        raise HTTPException(status_code=404, detail="World state not found")
    return state


@router.get("/key/{key}", response_model=WorldStateResponse)
async def get_world_state_by_key(
    key: str,
    manager: WorldStateManager = Depends(get_world_state_manager),
):
    """Get world state by key."""
    state = manager.get_by_key(key)
    if not state:
        raise HTTPException(status_code=404, detail="World state not found")
    return state


@router.put("/{state_id}", response_model=WorldStateResponse)
async def update_world_state(
    state_id: str,
    state: WorldStateUpdate,
    manager: WorldStateManager = Depends(get_world_state_manager),
):
    """Update world state."""
    updated = manager.update(state_id, state)
    if not updated:
        raise HTTPException(status_code=404, detail="World state not found")
    return updated


@router.put("/key/{key}", response_model=WorldStateResponse)
async def update_world_state_by_key(
    key: str,
    state: WorldStateUpdate,
    manager: WorldStateManager = Depends(get_world_state_manager),
):
    """Update world state by key."""
    updated = manager.update_by_key(key, state)
    if not updated:
        raise HTTPException(status_code=404, detail="World state not found")
    return updated


@router.delete("/{state_id}", status_code=204)
async def delete_world_state(
    state_id: str,
    manager: WorldStateManager = Depends(get_world_state_manager),
):
    """Delete world state."""
    deleted = manager.delete(state_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="World state not found")
    return None

