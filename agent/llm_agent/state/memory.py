"""Memory 管理模組，整合 LlamaIndex ChatMemoryBuffer"""

from typing import List, Optional

from llama_index.core.memory import ChatMemoryBuffer


class ChatMemory:
    """聊天記憶管理類別，封裝 LlamaIndex ChatMemoryBuffer"""

    def __init__(self, token_limit: Optional[int] = None):
        """
        初始化 ChatMemory

        Args:
            token_limit: Token 限制（可選）
        """
        self._memory = ChatMemoryBuffer.from_defaults(token_limit=token_limit)
        self.token_limit = token_limit

    def add_message(self, role: str, content: str) -> None:
        """
        新增訊息到記憶

        Args:
            role: 訊息角色（user, assistant, system）
            content: 訊息內容
        """
        from llama_index.core.llms import ChatMessage
        from llama_index.core.llms.types import MessageRole

        # 轉換角色名稱
        role_mapping = {
            "user": MessageRole.USER,
            "assistant": MessageRole.ASSISTANT,
            "system": MessageRole.SYSTEM,
        }

        message_role = role_mapping.get(role.lower(), MessageRole.USER)
        chat_message = ChatMessage(role=message_role, content=content)
        self._memory.put(chat_message)

    def get_all(self) -> List[dict]:
        """
        取得所有對話歷史

        Returns:
            對話歷史列表，每個項目包含 role 和 content
        """
        messages = self._memory.get_all()
        result = []
        for msg in messages:
            result.append({"role": msg.role.value, "content": msg.content})
        return result

    def get(self, k: int = -1) -> Optional[dict]:
        """
        取得最近的 k 條訊息（k=-1 表示取得所有）

        Args:
            k: 要取得的訊息數量

        Returns:
            訊息列表或單一訊息字典
        """
        messages = self._memory.get(k)
        if not messages:
            return None

        if isinstance(messages, list):
            if k == -1:
                return [{"role": msg.role.value, "content": msg.content} for msg in messages]
            else:
                return [{"role": msg.role.value, "content": msg.content} for msg in messages]
        else:
            return {"role": messages.role.value, "content": messages.content}

    def reset(self) -> None:
        """重置記憶"""
        self._memory.reset()

    def get_memory_buffer(self) -> ChatMemoryBuffer:
        """
        取得底層的 ChatMemoryBuffer 實例（供 LlamaIndex 使用）

        Returns:
            ChatMemoryBuffer 實例
        """
        return self._memory

    def __len__(self) -> int:
        """取得記憶中的訊息數量"""
        return len(self._memory.get_all())

