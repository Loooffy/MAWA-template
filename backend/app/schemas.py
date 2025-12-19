"""API layer Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional, Any


class MessageRequest(BaseModel):
    """Request schema for agent chat."""
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation context")
    user_id: Optional[str] = Field(None, description="User ID for user state access")


class MessageResponse(BaseModel):
    """Response schema for agent chat."""
    response: str = Field(..., description="Agent response")
    session_id: str = Field(..., description="Session ID")


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Service version")

