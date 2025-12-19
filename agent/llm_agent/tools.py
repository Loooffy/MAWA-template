"""Agent 工具定義框架模組"""

from typing import Any, Callable, Dict, List, Optional

from llama_index.core.tools import FunctionTool


class ToolRegistry:
    """工具註冊表，管理 Agent 可用的工具"""

    def __init__(self):
        """初始化工具註冊表"""
        self._tools: Dict[str, FunctionTool] = {}

    def register(self, name: str, tool: FunctionTool) -> None:
        """
        註冊工具

        Args:
            name: 工具名稱
            tool: FunctionTool 實例
        """
        self._tools[name] = tool

    def register_function(
        self,
        fn: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> FunctionTool:
        """
        註冊函數為工具

        Args:
            fn: 要註冊的函數
            name: 工具名稱（預設使用函數名稱）
            description: 工具描述（預設使用函數 docstring）

        Returns:
            建立的 FunctionTool 實例
        """
        tool = FunctionTool.from_defaults(
            fn=fn,
            name=name or fn.__name__,
            description=description or (fn.__doc__ or ""),
        )
        self.register(tool.metadata.name, tool)
        return tool

    def get_tool(self, name: str) -> Optional[FunctionTool]:
        """
        取得工具

        Args:
            name: 工具名稱

        Returns:
            FunctionTool 實例或 None
        """
        return self._tools.get(name)

    def get_all_tools(self) -> List[FunctionTool]:
        """
        取得所有工具

        Returns:
            工具列表
        """
        return list(self._tools.values())

    def unregister(self, name: str) -> bool:
        """
        取消註冊工具

        Args:
            name: 工具名稱

        Returns:
            是否成功取消註冊
        """
        if name in self._tools:
            del self._tools[name]
            return True
        return False

    def clear(self) -> None:
        """清除所有工具"""
        self._tools.clear()

    def __len__(self) -> int:
        """取得工具數量"""
        return len(self._tools)

    def __contains__(self, name: str) -> bool:
        """檢查工具是否存在"""
        return name in self._tools


def create_tool_from_function(
    fn: Callable,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> FunctionTool:
    """
    從函數建立工具（便利函數）

    Args:
        fn: 要轉換為工具的函數
        name: 工具名稱（預設使用函數名稱）
        description: 工具描述（預設使用函數 docstring）

    Returns:
        FunctionTool 實例

    Example:
        >>> def get_weather(location: str) -> str:
        ...     '''取得指定地點的天氣資訊'''
        ...     return f"{location} 的天氣是晴天"
        ...
        >>> tool = create_tool_from_function(get_weather)
        >>> print(tool.metadata.name)
        get_weather
    """
    return FunctionTool.from_defaults(
        fn=fn,
        name=name or fn.__name__,
        description=description or (fn.__doc__ or ""),
    )

