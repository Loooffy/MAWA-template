"""Agent 基礎資料模型"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """聊天訊息模型"""

    role: str = Field(..., description="訊息角色：user, assistant, system")
    content: str = Field(..., description="訊息內容")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="訊息時間戳")

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "你好，請介紹一下你自己",
                "timestamp": "2024-01-01T00:00:00",
            }
        }


class AgentRequest(BaseModel):
    """Agent 請求模型"""

    message: str = Field(..., description="使用者訊息")
    session_id: Optional[str] = Field(default=None, description="會話 ID，用於區分不同對話")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="額外的上下文資訊")
    stream: bool = Field(default=False, description="是否使用串流回應")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "請幫我查詢天氣",
                "session_id": "session_123",
                "context": {"location": "台北"},
                "stream": False,
            }
        }


class AgentResponse(BaseModel):
    """Agent 回應模型"""

    response: str = Field(..., description="Agent 回應內容")
    session_id: Optional[str] = Field(default=None, description="會話 ID")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="回應的元資料")
    timestamp: datetime = Field(default_factory=datetime.now, description="回應時間戳")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "根據您的要求，我已經查詢了天氣資訊...",
                "session_id": "session_123",
                "metadata": {"model": "llama3.2", "tokens_used": 150},
                "timestamp": "2024-01-01T00:00:00",
            }
        }


class ToolResult(BaseModel):
    """工具執行結果模型"""

    tool_name: str = Field(..., description="工具名稱")
    result: Any = Field(..., description="工具執行結果")
    success: bool = Field(default=True, description="是否執行成功")
    error: Optional[str] = Field(default=None, description="錯誤訊息（如果執行失敗）")
    timestamp: datetime = Field(default_factory=datetime.now, description="執行時間戳")

    class Config:
        json_schema_extra = {
            "example": {
                "tool_name": "get_weather",
                "result": {"temperature": 25, "condition": "晴天"},
                "success": True,
                "error": None,
                "timestamp": "2024-01-01T00:00:00",
            }
        }

