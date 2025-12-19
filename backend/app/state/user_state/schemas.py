"""User State Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserStateBase(BaseModel):
    """Base schema for User State."""
    user_id: str = Field(..., description="User ID")
    key: str = Field(..., description="State key")
    value: Optional[str] = Field(None, description="State value")


class UserStateCreate(UserStateBase):
    """Schema for creating User State."""
    pass


class UserStateUpdate(BaseModel):
    """Schema for updating User State."""
    value: Optional[str] = Field(None, description="State value to update")


class UserStateResponse(UserStateBase):
    """Schema for User State response."""
    id: str = Field(..., description="State ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")
    
    class Config:
        from_attributes = True

