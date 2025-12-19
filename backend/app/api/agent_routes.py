"""Agent interaction API routes."""
import uuid
from fastapi import APIRouter, HTTPException, Depends
from app.schemas import MessageRequest, MessageResponse
from app.state.state_accessor import StateAccessor
from app.dependencies import get_state_accessor

router = APIRouter(prefix="/api/agent", tags=["agent"])


@router.post("/chat", response_model=MessageResponse)
async def chat_with_agent(
    request: MessageRequest,
    state_accessor: StateAccessor = Depends(get_state_accessor),
):
    """Chat with the agent.
    
    Note: This is a placeholder implementation. In a real implementation,
    this would integrate with the Agent package to process the message.
    """
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    
    # Placeholder response - in real implementation, this would call the Agent
    response_text = f"Agent received: {request.message}"
    
    # If user_id is provided, agent can access user state via state_accessor
    if request.user_id:
        user_states = state_accessor.get_user_states(request.user_id)
        if user_states:
            response_text += f" (Found {len(user_states)} user states)"
    
    return MessageResponse(response=response_text, session_id=session_id)


@router.get("/health")
async def agent_health():
    """Check agent health."""
    return {"status": "healthy", "service": "agent"}

