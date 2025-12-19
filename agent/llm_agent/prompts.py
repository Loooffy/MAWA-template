"""Prompt 管理模組"""

from typing import Dict, Optional


class PromptTemplate:
    """Prompt 模板基礎類別"""

    def __init__(self, template: str, variables: Optional[Dict[str, str]] = None):
        """
        初始化 Prompt 模板

        Args:
            template: 模板字串，使用 {variable_name} 作為佔位符
            variables: 可選的預設變數值
        """
        self.template = template
        self.variables = variables or {}

    def format(self, **kwargs) -> str:
        """
        格式化模板

        Args:
            **kwargs: 變數值

        Returns:
            格式化後的 prompt
        """
        # 合併預設變數和傳入的變數（傳入的優先）
        merged_vars = {**self.variables, **kwargs}
        return self.template.format(**merged_vars)

    def __call__(self, **kwargs) -> str:
        """允許直接呼叫實例"""
        return self.format(**kwargs)


class PromptManager:
    """Prompt 管理器，提供常用的 prompt 模板"""

    # 系統提示詞模板
    SYSTEM_PROMPT = PromptTemplate(
        template="""你是一個友善且專業的 AI 助手。請根據使用者的問題提供準確、有用的回答。

{additional_context}""",
        variables={"additional_context": ""},
    )

    # 對話提示詞模板
    CHAT_PROMPT = PromptTemplate(
        template="""以下是對話歷史：

{chat_history}

使用者：{user_message}

助手：""",
    )

    # 任務完成提示詞模板
    TASK_COMPLETION_PROMPT = PromptTemplate(
        template="""請完成以下任務：

任務描述：{task_description}

相關上下文：
{context}

請提供詳細的執行步驟和結果。""",
    )

    @classmethod
    def get_system_prompt(cls, additional_context: str = "") -> str:
        """
        取得系統提示詞

        Args:
            additional_context: 額外的上下文資訊

        Returns:
            系統提示詞
        """
        return cls.SYSTEM_PROMPT.format(additional_context=additional_context)

    @classmethod
    def get_chat_prompt(cls, user_message: str, chat_history: str = "") -> str:
        """
        取得對話提示詞

        Args:
            user_message: 使用者訊息
            chat_history: 對話歷史（可選）

        Returns:
            對話提示詞
        """
        return cls.CHAT_PROMPT.format(user_message=user_message, chat_history=chat_history or "（無對話歷史）")

    @classmethod
    def get_task_prompt(cls, task_description: str, context: str = "") -> str:
        """
        取得任務完成提示詞

        Args:
            task_description: 任務描述
            context: 相關上下文

        Returns:
            任務提示詞
        """
        return cls.TASK_COMPLETION_PROMPT.format(task_description=task_description, context=context or "（無額外上下文）")

    @classmethod
    def create_custom_prompt(cls, template: str, **variables) -> PromptTemplate:
        """
        建立自訂 prompt 模板

        Args:
            template: 模板字串
            **variables: 預設變數值

        Returns:
            PromptTemplate 實例
        """
        return PromptTemplate(template, variables)

