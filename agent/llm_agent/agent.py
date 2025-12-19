"""Agent 核心實作模組"""

import logging
from typing import Any, Dict, List, Optional

from llama_index.core.agent import ReActAgent
from llama_index.core.llms import ChatMessage, LLM
from llama_index.llms.ollama import Ollama

from .config import AgentConfig
from .llm_config import LLMProvider
from .prompts import PromptManager
from .schemas import AgentRequest, AgentResponse
from .state.agent_state import AgentState
from .tools import ToolRegistry
from .utils import format_error_message, validate_message

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base Agent 基礎類別，提供 LlamaIndex 整合的基礎框架"""

    def __init__(
        self,
        config: Optional[AgentConfig] = None,
        tools: Optional[List] = None,
        state: Optional[AgentState] = None,
    ):
        """
        初始化 BaseAgent

        Args:
            config: Agent 配置（如果為 None，則從環境變數載入）
            tools: Agent 工具列表（可選）
            state: Agent State 實例（可選，會自動建立）
        """
        self.config = config or AgentConfig()
        self.tool_registry = ToolRegistry()
        self.state = state or AgentState(memory_token_limit=self.config.memory_token_limit)

        # 初始化 LLM
        self.llm = self._create_llm()

        # 註冊工具
        if tools:
            for tool in tools:
                if hasattr(tool, "metadata"):
                    self.tool_registry.register(tool.metadata.name, tool)
                else:
                    logger.warning(f"工具 {tool} 不是有效的 FunctionTool，已跳過")

        # 初始化 Agent（如果使用 Agent 模式）
        self.agent: Optional[ReActAgent] = None
        if self.config.use_agent_mode:
            self.agent = self._create_agent()

    def _create_llm(self) -> LLM:
        """
        根據 LLMConfig 建立對應的 LLM 實例

        Returns:
            LLM 實例（根據 provider 不同而不同）
        """
        llm_config = self.config.llm
        provider = llm_config.provider

        if provider == LLMProvider.OLLAMA:
            if not llm_config.ollama:
                raise ValueError("Ollama 配置不存在")
            ollama_cfg = llm_config.ollama
            return Ollama(
                model=ollama_cfg.model,
                base_url=ollama_cfg.base_url,
                request_timeout=llm_config.timeout,
                temperature=ollama_cfg.temperature,
                top_p=ollama_cfg.top_p,
                top_k=ollama_cfg.top_k,
                num_ctx=ollama_cfg.num_ctx,
                repeat_penalty=ollama_cfg.repeat_penalty,
            )
        elif provider == LLMProvider.OPENAI:
            try:
                from llama_index.llms.openai import OpenAI
            except ImportError:
                raise ImportError(
                    "使用 OpenAI provider 需要安裝 llama-index-llms-openai: "
                    "pip install llama-index-llms-openai"
                )
            if not llm_config.openai:
                raise ValueError("OpenAI 配置不存在")
            openai_cfg = llm_config.openai
            return OpenAI(
                api_key=openai_cfg.api_key,
                model=openai_cfg.model,
                base_url=openai_cfg.base_url,
                temperature=openai_cfg.temperature,
                max_tokens=openai_cfg.max_tokens,
                top_p=openai_cfg.top_p,
                frequency_penalty=openai_cfg.frequency_penalty,
                presence_penalty=openai_cfg.presence_penalty,
                timeout=llm_config.timeout,
            )
        elif provider == LLMProvider.ANTHROPIC:
            try:
                from llama_index.llms.anthropic import Anthropic
            except ImportError:
                raise ImportError(
                    "使用 Anthropic provider 需要安裝 llama-index-llms-anthropic: "
                    "pip install llama-index-llms-anthropic"
                )
            if not llm_config.anthropic:
                raise ValueError("Anthropic 配置不存在")
            anthropic_cfg = llm_config.anthropic
            return Anthropic(
                api_key=anthropic_cfg.api_key,
                model=anthropic_cfg.model,
                temperature=anthropic_cfg.temperature,
                max_tokens=anthropic_cfg.max_tokens,
                top_p=anthropic_cfg.top_p,
                timeout=llm_config.timeout,
            )
        else:
            raise ValueError(f"不支援的 LLM provider: {provider}")

    def _create_agent(self) -> ReActAgent:
        """
        建立 ReActAgent 實例

        Returns:
            ReActAgent 實例
        """
        tools = self.tool_registry.get_all_tools()
        memory = self.state.memory.get_memory_buffer()

        return ReActAgent.from_tools(
            tools=tools,
            llm=self.llm,
            memory=memory,
            verbose=self.config.agent_verbose,
        )

    def register_tool(self, tool) -> None:
        """
        註冊工具到 Agent

        Args:
            tool: FunctionTool 實例
        """
        if hasattr(tool, "metadata"):
            self.tool_registry.register(tool.metadata.name, tool)
            # 如果使用 Agent 模式，需要重新建立 Agent
            if self.config.use_agent_mode:
                self.agent = self._create_agent()
        else:
            logger.warning(f"工具 {tool} 不是有效的 FunctionTool，已跳過")

    def chat(self, request: AgentRequest) -> AgentResponse:
        """
        與 Agent 進行對話（同步版本）

        Args:
            request: Agent 請求

        Returns:
            Agent 回應
        """
        try:
            # 驗證訊息
            if not validate_message(request.message):
                raise ValueError("訊息格式無效")

            # 更新 session_id
            if request.session_id:
                self.state.session_id = request.session_id

            # 新增使用者訊息到記憶
            self.state.add_message("user", request.message)

            # 取得回應
            if self.config.use_agent_mode and self.agent:
                # 使用 ReActAgent
                response_text = self.agent.chat(request.message).response
            else:
                # 直接使用 LLM
                response_text = self._chat_with_llm(request)

            # 新增助手回應到記憶
            self.state.add_message("assistant", response_text)

            # 建立回應
            return AgentResponse(
                response=response_text,
                session_id=self.state.session_id,
                metadata={
                    "model": self.config.llm.get_model_name(),
                    "provider": self.config.llm.provider.value,
                    "use_agent_mode": self.config.use_agent_mode,
                    "context": request.context,
                },
            )

        except Exception as e:
            error_msg = format_error_message(e, "chat")
            logger.error(error_msg, exc_info=True)
            raise

    async def achat(self, request: AgentRequest) -> AgentResponse:
        """
        與 Agent 進行對話（非同步版本）

        Args:
            request: Agent 請求

        Returns:
            Agent 回應
        """
        try:
            # 驗證訊息
            if not validate_message(request.message):
                raise ValueError("訊息格式無效")

            # 更新 session_id
            if request.session_id:
                self.state.session_id = request.session_id

            # 新增使用者訊息到記憶
            self.state.add_message("user", request.message)

            # 取得回應
            if self.config.use_agent_mode and self.agent:
                # 使用 ReActAgent（非同步）
                response_obj = await self.agent.achat(request.message)
                response_text = response_obj.response
            else:
                # 直接使用 LLM（非同步）
                response_text = await self._achat_with_llm(request)

            # 新增助手回應到記憶
            self.state.add_message("assistant", response_text)

            # 建立回應
            return AgentResponse(
                response=response_text,
                session_id=self.state.session_id,
                metadata={
                    "model": self.config.llm.get_model_name(),
                    "provider": self.config.llm.provider.value,
                    "use_agent_mode": self.config.use_agent_mode,
                    "context": request.context,
                },
            )

        except Exception as e:
            error_msg = format_error_message(e, "achat")
            logger.error(error_msg, exc_info=True)
            raise

    def _chat_with_llm(self, request: AgentRequest) -> str:
        """
        直接使用 LLM 進行對話（同步版本）

        Args:
            request: Agent 請求

        Returns:
            LLM 回應文字
        """
        # 建立 prompt
        chat_history = self.state.get_chat_history()
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history[:-1]])

        prompt = PromptManager.get_chat_prompt(
            user_message=request.message,
            chat_history=history_text,
        )

        # 呼叫 LLM
        response = self.llm.complete(prompt)
        return response.text

    async def _achat_with_llm(self, request: AgentRequest) -> str:
        """
        直接使用 LLM 進行對話（非同步版本）

        Args:
            request: Agent 請求

        Returns:
            LLM 回應文字
        """
        # 建立 prompt
        chat_history = self.state.get_chat_history()
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history[:-1]])

        prompt = PromptManager.get_chat_prompt(
            user_message=request.message,
            chat_history=history_text,
        )

        # 呼叫 LLM（非同步）
        response = await self.llm.acomplete(prompt)
        return response.text

    def complete(self, prompt: str, **kwargs) -> str:
        """
        完成文字（同步版本）

        Args:
            prompt: 提示詞
            **kwargs: 額外的參數

        Returns:
            完成的文字
        """
        try:
            response = self.llm.complete(prompt, **kwargs)
            return response.text
        except Exception as e:
            error_msg = format_error_message(e, "complete")
            logger.error(error_msg, exc_info=True)
            raise

    async def acomplete(self, prompt: str, **kwargs) -> str:
        """
        完成文字（非同步版本）

        Args:
            prompt: 提示詞
            **kwargs: 額外的參數

        Returns:
            完成的文字
        """
        try:
            response = await self.llm.acomplete(prompt, **kwargs)
            return response.text
        except Exception as e:
            error_msg = format_error_message(e, "achat")
            logger.error(error_msg, exc_info=True)
            raise

    def reset_state(self, keep_session: bool = False) -> None:
        """
        重置 Agent State

        Args:
            keep_session: 是否保留 session_id
        """
        self.state.reset(keep_session=keep_session)
        # 如果使用 Agent 模式，需要重新建立 Agent（因為 memory 已重置）
        if self.config.use_agent_mode:
            self.agent = self._create_agent()

    def get_state(self) -> Dict[str, Any]:
        """
        取得 Agent State 的字典表示

        Returns:
            Agent State 字典
        """
        return self.state.to_dict()

