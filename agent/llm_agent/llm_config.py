"""LLM 配置管理模組"""

import os
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator


class LLMProvider(str, Enum):
    """支援的 LLM Provider"""

    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    # 可以繼續擴展其他 provider


class OllamaConfig(BaseModel):
    """Ollama LLM 配置"""

    base_url: str = Field(
        default="http://localhost:11434",
        description="Ollama API 基礎 URL",
    )
    model: str = Field(
        default="llama3.2",
        description="使用的模型名稱",
    )
    temperature: float = Field(
        default=0.7,
        description="溫度參數（0.0-2.0）",
        ge=0.0,
        le=2.0,
    )
    top_p: float = Field(
        default=0.9,
        description="Top-p 參數（0.0-1.0）",
        ge=0.0,
        le=1.0,
    )
    top_k: Optional[int] = Field(
        default=None,
        description="Top-k 參數",
    )
    num_ctx: Optional[int] = Field(
        default=None,
        description="上下文窗口大小",
    )
    repeat_penalty: Optional[float] = Field(
        default=None,
        description="重複懲罰參數",
    )

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        """驗證 base_url 格式"""
        if not v.startswith(("http://", "https://")):
            raise ValueError("base_url 必須以 http:// 或 https:// 開頭")
        return v.rstrip("/")


class OpenAIConfig(BaseModel):
    """OpenAI LLM 配置"""

    api_key: str = Field(
        ...,
        description="OpenAI API Key",
    )
    model: str = Field(
        default="gpt-3.5-turbo",
        description="使用的模型名稱",
    )
    base_url: Optional[str] = Field(
        default=None,
        description="自訂 API 基礎 URL（用於兼容 API）",
    )
    temperature: float = Field(
        default=0.7,
        description="溫度參數（0.0-2.0）",
        ge=0.0,
        le=2.0,
    )
    max_tokens: Optional[int] = Field(
        default=None,
        description="最大 token 數",
    )
    top_p: float = Field(
        default=1.0,
        description="Top-p 參數（0.0-1.0）",
        ge=0.0,
        le=1.0,
    )
    frequency_penalty: float = Field(
        default=0.0,
        description="頻率懲罰（-2.0 到 2.0）",
        ge=-2.0,
        le=2.0,
    )
    presence_penalty: float = Field(
        default=0.0,
        description="存在懲罰（-2.0 到 2.0）",
        ge=-2.0,
        le=2.0,
    )


class AnthropicConfig(BaseModel):
    """Anthropic (Claude) LLM 配置"""

    api_key: str = Field(
        ...,
        description="Anthropic API Key",
    )
    model: str = Field(
        default="claude-3-sonnet-20240229",
        description="使用的模型名稱",
    )
    temperature: float = Field(
        default=0.7,
        description="溫度參數（0.0-1.0）",
        ge=0.0,
        le=1.0,
    )
    max_tokens: int = Field(
        default=1024,
        description="最大 token 數",
        gt=0,
    )
    top_p: float = Field(
        default=0.9,
        description="Top-p 參數（0.0-1.0）",
        ge=0.0,
        le=1.0,
    )


class LLMConfig(BaseModel):
    """LLM 配置類別，管理 provider、model 和 parameters"""

    provider: LLMProvider = Field(
        default=LLMProvider.OLLAMA,
        description="LLM Provider",
    )
    timeout: float = Field(
        default=60.0,
        description="請求超時時間（秒）",
        gt=0.0,
    )

    # Provider 特定配置
    ollama: Optional[OllamaConfig] = Field(
        default=None,
        description="Ollama 配置",
    )
    openai: Optional[OpenAIConfig] = Field(
        default=None,
        description="OpenAI 配置",
    )
    anthropic: Optional[AnthropicConfig] = Field(
        default=None,
        description="Anthropic 配置",
    )

    # 自訂參數（用於擴展）
    custom_params: Dict[str, Any] = Field(
        default_factory=dict,
        description="自訂參數",
    )

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, v: LLMProvider) -> LLMProvider:
        """驗證 provider"""
        return v

    def model_post_init(self, __context: Any) -> None:
        """初始化後處理，確保對應的 provider 配置存在"""
        # 如果沒有設定對應的 provider 配置，使用預設值
        if self.provider == LLMProvider.OLLAMA and self.ollama is None:
            self.ollama = OllamaConfig()
        elif self.provider == LLMProvider.OPENAI and self.openai is None:
            # OpenAI 需要 API key，如果沒有則從環境變數讀取
            api_key = os.getenv("OPENAI_API_KEY", "")
            if not api_key:
                raise ValueError("OpenAI provider 需要設定 api_key 或 OPENAI_API_KEY 環境變數")
            self.openai = OpenAIConfig(api_key=api_key)
        elif self.provider == LLMProvider.ANTHROPIC and self.anthropic is None:
            # Anthropic 需要 API key，如果沒有則從環境變數讀取
            api_key = os.getenv("ANTHROPIC_API_KEY", "")
            if not api_key:
                raise ValueError("Anthropic provider 需要設定 api_key 或 ANTHROPIC_API_KEY 環境變數")
            self.anthropic = AnthropicConfig(api_key=api_key)

    def get_model_name(self) -> str:
        """
        取得當前 provider 的模型名稱

        Returns:
            模型名稱
        """
        if self.provider == LLMProvider.OLLAMA and self.ollama:
            return self.ollama.model
        elif self.provider == LLMProvider.OPENAI and self.openai:
            return self.openai.model
        elif self.provider == LLMProvider.ANTHROPIC and self.anthropic:
            return self.anthropic.model
        else:
            raise ValueError(f"Provider {self.provider} 的配置不存在")

    def get_provider_config(self) -> BaseModel:
        """
        取得當前 provider 的配置物件

        Returns:
            Provider 配置物件
        """
        if self.provider == LLMProvider.OLLAMA and self.ollama:
            return self.ollama
        elif self.provider == LLMProvider.OPENAI and self.openai:
            return self.openai
        elif self.provider == LLMProvider.ANTHROPIC and self.anthropic:
            return self.anthropic
        else:
            raise ValueError(f"Provider {self.provider} 的配置不存在")

    @classmethod
    def from_env(cls, **kwargs) -> "LLMConfig":
        """
        從環境變數建立 LLMConfig

        Args:
            **kwargs: 額外的配置參數

        Returns:
            LLMConfig 實例
        """
        # 從環境變數讀取 provider
        provider_str = os.getenv("LLM_PROVIDER", kwargs.get("provider", "ollama")).lower()
        provider = LLMProvider(provider_str)

        # 根據 provider 建立配置
        config_data = {
            "provider": provider,
            "timeout": float(os.getenv("LLM_TIMEOUT", kwargs.get("timeout", 60.0))),
        }

        if provider == LLMProvider.OLLAMA:
            config_data["ollama"] = OllamaConfig(
                base_url=os.getenv("OLLAMA_BASE_URL", kwargs.get("ollama_base_url", "http://localhost:11434")),
                model=os.getenv("OLLAMA_MODEL", kwargs.get("ollama_model", "llama3.2")),
                temperature=float(os.getenv("OLLAMA_TEMPERATURE", kwargs.get("ollama_temperature", 0.7))),
                top_p=float(os.getenv("OLLAMA_TOP_P", kwargs.get("ollama_top_p", 0.9))),
            )
        elif provider == LLMProvider.OPENAI:
            api_key = os.getenv("OPENAI_API_KEY", kwargs.get("openai_api_key", ""))
            if not api_key:
                raise ValueError("OpenAI provider 需要設定 OPENAI_API_KEY 環境變數")
            config_data["openai"] = OpenAIConfig(
                api_key=api_key,
                model=os.getenv("OPENAI_MODEL", kwargs.get("openai_model", "gpt-3.5-turbo")),
                temperature=float(os.getenv("OPENAI_TEMPERATURE", kwargs.get("openai_temperature", 0.7))),
                base_url=os.getenv("OPENAI_BASE_URL", kwargs.get("openai_base_url")),
            )
        elif provider == LLMProvider.ANTHROPIC:
            api_key = os.getenv("ANTHROPIC_API_KEY", kwargs.get("anthropic_api_key", ""))
            if not api_key:
                raise ValueError("Anthropic provider 需要設定 ANTHROPIC_API_KEY 環境變數")
            config_data["anthropic"] = AnthropicConfig(
                api_key=api_key,
                model=os.getenv("ANTHROPIC_MODEL", kwargs.get("anthropic_model", "claude-3-sonnet-20240229")),
                temperature=float(os.getenv("ANTHROPIC_TEMPERATURE", kwargs.get("anthropic_temperature", 0.7))),
            )

        # 合併額外的 kwargs
        config_data.update(kwargs)
        return cls(**config_data)

