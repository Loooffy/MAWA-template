"""World State Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class WorldStateBase(BaseModel):
    """Base schema for World State."""
    key: str = Field(..., description="State key")
    value: Optional[str] = Field(None, description="State value")


class WorldStateCreate(WorldStateBase):
    """Schema for creating World State."""
    pass


class WorldStateUpdate(BaseModel):
    """Schema for updating World State."""
    value: Optional[str] = Field(None, description="State value to update")


class WorldStateResponse(WorldStateBase):
    """Schema for World State response."""
    id: str = Field(..., description="State ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")
    
    class Config:
        from_attributes = True

