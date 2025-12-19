"""Agent State 管理模組"""

from typing import Any, Dict, List, Optional

from .memory import ChatMemory


class AgentState:
    """Agent State 管理器，管理對話上下文、tool result、workflow context 等"""

    def __init__(self, session_id: Optional[str] = None, memory_token_limit: Optional[int] = None):
        """
        初始化 AgentState

        Args:
            session_id: 會話 ID，用於區分不同對話
            memory_token_limit: Memory token 限制
        """
        self.session_id = session_id
        self.memory = ChatMemory(token_limit=memory_token_limit)
        self.tool_results: List[Dict[str, Any]] = []
        self.workflow_context: Dict[str, Any] = {}
        self.prompt_context: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}

    def add_message(self, role: str, content: str) -> None:
        """
        新增訊息到對話歷史

        Args:
            role: 訊息角色（user, assistant, system）
            content: 訊息內容
        """
        self.memory.add_message(role, content)

    def get_chat_history(self, k: int = -1) -> List[Dict[str, str]]:
        """
        取得對話歷史

        Args:
            k: 要取得的訊息數量（-1 表示取得所有）

        Returns:
            對話歷史列表
        """
        messages = self.memory.get(k)
        if messages is None:
            return []
        if isinstance(messages, list):
            return messages
        return [messages]

    def add_tool_result(self, tool_name: str, result: Any, success: bool = True, error: Optional[str] = None) -> None:
        """
        新增工具執行結果

        Args:
            tool_name: 工具名稱
            result: 執行結果
            success: 是否執行成功
            error: 錯誤訊息（如果執行失敗）
        """
        from datetime import datetime

        self.tool_results.append(
            {
                "tool_name": tool_name,
                "result": result,
                "success": success,
                "error": error,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def get_tool_results(self, tool_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        取得工具執行結果

        Args:
            tool_name: 可選的工具名稱過濾

        Returns:
            工具執行結果列表
        """
        if tool_name:
            return [r for r in self.tool_results if r.get("tool_name") == tool_name]
        return self.tool_results.copy()

    def set_workflow_context(self, key: str, value: Any) -> None:
        """
        設定 workflow context

        Args:
            key: Context 鍵
            value: Context 值
        """
        self.workflow_context[key] = value

    def get_workflow_context(self, key: Optional[str] = None) -> Any:
        """
        取得 workflow context

        Args:
            key: Context 鍵（None 表示取得所有）

        Returns:
            Context 值或整個 context 字典
        """
        if key is None:
            return self.workflow_context.copy()
        return self.workflow_context.get(key)

    def set_prompt_context(self, key: str, value: Any) -> None:
        """
        設定 prompt context

        Args:
            key: Context 鍵
            value: Context 值
        """
        self.prompt_context[key] = value

    def get_prompt_context(self, key: Optional[str] = None) -> Any:
        """
        取得 prompt context

        Args:
            key: Context 鍵（None 表示取得所有）

        Returns:
            Context 值或整個 context 字典
        """
        if key is None:
            return self.prompt_context.copy()
        return self.prompt_context.get(key)

    def set_metadata(self, key: str, value: Any) -> None:
        """
        設定元資料

        Args:
            key: 元資料鍵
            value: 元資料值
        """
        self.metadata[key] = value

    def get_metadata(self, key: Optional[str] = None) -> Any:
        """
        取得元資料

        Args:
            key: 元資料鍵（None 表示取得所有）

        Returns:
            元資料值或整個 metadata 字典
        """
        if key is None:
            return self.metadata.copy()
        return self.metadata.get(key)

    def reset(self, keep_session: bool = False) -> None:
        """
        重置 Agent State

        Args:
            keep_session: 是否保留 session_id
        """
        self.memory.reset()
        self.tool_results.clear()
        self.workflow_context.clear()
        self.prompt_context.clear()
        self.metadata.clear()
        if not keep_session:
            self.session_id = None

    def to_dict(self) -> Dict[str, Any]:
        """
        將 Agent State 轉換為字典

        Returns:
            Agent State 字典表示
        """
        return {
            "session_id": self.session_id,
            "chat_history": self.get_chat_history(),
            "tool_results": self.tool_results,
            "workflow_context": self.workflow_context,
            "prompt_context": self.prompt_context,
            "metadata": self.metadata,
        }

