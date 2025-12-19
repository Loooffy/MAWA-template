"""通用工具函數模組"""

import json
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def parse_json_response(text: str) -> Optional[Dict[str, Any]]:
    """
    從文字回應中解析 JSON 內容

    Args:
        text: 包含 JSON 的文字內容

    Returns:
        解析後的 JSON 字典，如果解析失敗則返回 None
    """
    try:
        # 嘗試直接解析
        return json.loads(text)
    except json.JSONDecodeError:
        # 嘗試從文字中提取 JSON（尋找 {...} 或 [...]）
        import re

        json_pattern = r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]"
        matches = re.findall(json_pattern, text, re.DOTALL)

        for match in matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue

        logger.warning(f"無法從文字中解析 JSON: {text[:100]}...")
        return None


def safe_json_parse(text: str, default: Any = None) -> Any:
    """
    安全地解析 JSON，失敗時返回預設值

    Args:
        text: 要解析的 JSON 字串
        default: 解析失敗時的預設值

    Returns:
        解析後的 JSON 物件或預設值
    """
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        logger.warning(f"JSON 解析失敗，使用預設值: {text[:100] if text else 'None'}...")
        return default


def extract_code_blocks(text: str, language: Optional[str] = None) -> list[str]:
    """
    從文字中提取程式碼區塊

    Args:
        text: 包含程式碼區塊的文字
        language: 可選的程式語言過濾（如 'python', 'javascript'）

    Returns:
        提取的程式碼區塊列表
    """
    import re

    # 匹配 ```language\ncode\n``` 格式
    pattern = r"```(?:\w+)?\n(.*?)```"
    if language:
        pattern = rf"```{language}\n(.*?)```"

    matches = re.findall(pattern, text, re.DOTALL)
    return [match.strip() for match in matches]


def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
    """
    清理和截斷文字

    Args:
        text: 要清理的文字
        max_length: 最大長度（可選）

    Returns:
        清理後的文字
    """
    if not text:
        return ""

    # 移除多餘的空白字元
    text = " ".join(text.split())

    if max_length and len(text) > max_length:
        text = text[:max_length] + "..."

    return text


def format_error_message(error: Exception, context: Optional[str] = None) -> str:
    """
    格式化錯誤訊息

    Args:
        error: 例外物件
        context: 可選的上下文資訊

    Returns:
        格式化後的錯誤訊息
    """
    error_msg = f"{type(error).__name__}: {str(error)}"
    if context:
        error_msg = f"[{context}] {error_msg}"
    return error_msg


def validate_message(message: str, min_length: int = 1, max_length: int = 10000) -> bool:
    """
    驗證訊息格式

    Args:
        message: 要驗證的訊息
        min_length: 最小長度
        max_length: 最大長度

    Returns:
        是否通過驗證
    """
    if not isinstance(message, str):
        return False
    if len(message.strip()) < min_length:
        return False
    if len(message) > max_length:
        return False
    return True

