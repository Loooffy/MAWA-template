"""Agent 配置管理模組"""

import os
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator

from .llm_config import LLMConfig, LLMProvider, OllamaConfig


class AgentConfig(BaseModel):
    """Agent 配置類別，從環境變數載入配置"""

    # LLM 配置
    llm: LLMConfig = Field(
        default_factory=lambda: LLMConfig.from_env(),
        description="LLM 配置",
    )

    # Agent 行為配置
    agent_verbose: bool = Field(
        default=False,
        description="是否啟用詳細日誌",
    )
    use_agent_mode: bool = Field(
        default=False,
        description="是否使用 ReActAgent 模式（False 表示直接使用 LLM）",
    )

    # Memory 配置
    memory_token_limit: Optional[int] = Field(
        default=None,
        description="Memory token 限制（None 表示無限制）",
    )

    # 向後兼容：保留舊的配置欄位（已棄用）
    ollama_base_url: Optional[str] = Field(
        default=None,
        description="[已棄用] 請使用 llm.ollama.base_url",
    )
    ollama_model: Optional[str] = Field(
        default=None,
        description="[已棄用] 請使用 llm.ollama.model",
    )
    agent_timeout: Optional[float] = Field(
        default=None,
        description="[已棄用] 請使用 llm.timeout",
    )

    @field_validator("agent_timeout")
    @classmethod
    def validate_timeout(cls, v: Optional[float]) -> Optional[float]:
        """驗證超時時間"""
        if v is not None and v <= 0:
            raise ValueError("超時時間必須大於 0")
        return v

    def model_post_init(self, __context: Any) -> None:
        """初始化後處理，處理向後兼容"""
        # 如果提供了舊的配置欄位，更新到新的 LLM 配置中
        if self.ollama_base_url or self.ollama_model or self.agent_timeout:
            # 確保使用 Ollama provider
            if self.llm.provider.value != "ollama":
                self.llm.provider = LLMProvider.OLLAMA
                if self.llm.ollama is None:
                    self.llm.ollama = OllamaConfig()

            if self.ollama_base_url:
                self.llm.ollama.base_url = self.ollama_base_url
            if self.ollama_model:
                self.llm.ollama.model = self.ollama_model
            if self.agent_timeout:
                self.llm.timeout = self.agent_timeout

    def __init__(self, **kwargs):
        """初始化配置，支援環境變數"""
        # 處理 LLM 配置
        if "llm" not in kwargs:
            # 從環境變數建立 LLM 配置
            kwargs["llm"] = LLMConfig.from_env(**kwargs)

        # 處理其他配置
        env_vars = {
            "agent_verbose": os.getenv("AGENT_VERBOSE", "false").lower() == "true" or kwargs.get("agent_verbose", False),
            "use_agent_mode": os.getenv("USE_AGENT_MODE", "false").lower() == "true" or kwargs.get("use_agent_mode", False),
            "memory_token_limit": (
                int(os.getenv("MEMORY_TOKEN_LIMIT"))
                if os.getenv("MEMORY_TOKEN_LIMIT")
                else kwargs.get("memory_token_limit")
            ),
            # 向後兼容的舊配置
            "ollama_base_url": os.getenv("OLLAMA_BASE_URL", kwargs.get("ollama_base_url")),
            "ollama_model": os.getenv("OLLAMA_MODEL", kwargs.get("ollama_model")),
            "agent_timeout": (
                float(os.getenv("AGENT_TIMEOUT"))
                if os.getenv("AGENT_TIMEOUT")
                else kwargs.get("agent_timeout")
            ),
        }
        # 合併傳入的 kwargs 和環境變數（kwargs 優先）
        merged = {**env_vars, **kwargs}
        super().__init__(**merged)

