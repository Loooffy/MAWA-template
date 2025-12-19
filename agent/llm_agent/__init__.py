"""
LLM Agent 套件

提供可重用的 LLM Agent 基礎架構，基於 LlamaIndex 框架。
"""

from .agent import BaseAgent
from .config import AgentConfig
from .llm_config import (
    LLMConfig,
    LLMProvider,
    OllamaConfig,
    OpenAIConfig,
    AnthropicConfig,
)
from .schemas import AgentRequest, AgentResponse, ChatMessage
from .state.agent_state import AgentState
from .state.memory import ChatMemory

__all__ = [
    "BaseAgent",
    "AgentConfig",
    "LLMConfig",
    "LLMProvider",
    "OllamaConfig",
    "OpenAIConfig",
    "AnthropicConfig",
    "AgentRequest",
    "AgentResponse",
    "ChatMessage",
    "AgentState",
    "ChatMemory",
]

__version__ = "0.1.0"

