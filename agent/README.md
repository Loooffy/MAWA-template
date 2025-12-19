# LLM Agent 套件

可重用的 LLM Agent 套件，基於 LlamaIndex 框架，提供統一的 Agent API 和豐富的功能。

## 功能特色

- **基於 LlamaIndex**：使用成熟的 LlamaIndex 框架，支援多種 LLM 後端
- **Ollama 整合**：預設整合 Ollama，支援本地 LLM 部署
- **記憶管理**：整合 LlamaIndex 的 `ChatMemoryBuffer`，自動管理對話歷史
- **工具支援**：提供工具註冊和管理框架，可擴展 Agent 功能
- **State 管理**：完整的 Agent State 管理，包含對話上下文、tool result、workflow context 等
- **可擴展設計**：提供 `BaseAgent` 基礎類別，易於擴展和自訂

## 安裝

### 使用 uv（推薦）

```bash
# 在專案根目錄
uv sync

# 或安裝到環境中
cd agent
uv pip install -e .
```

### 使用 pip

```bash
cd agent
pip install -e .
```

## 快速開始

### 基本使用

```python
from llm_agent import BaseAgent, AgentConfig, AgentRequest

# 建立 Agent（使用預設配置）
agent = BaseAgent()

# 建立請求
request = AgentRequest(
    message="你好，請介紹一下你自己",
    session_id="session_123"
)

# 進行對話
response = agent.chat(request)
print(response.response)
```

### 使用自訂配置

```python
from llm_agent import BaseAgent, AgentConfig, AgentRequest

# 建立自訂配置
config = AgentConfig(
    ollama_model="llama3.2",
    ollama_base_url="http://localhost:11434",
    use_agent_mode=True,  # 使用 ReActAgent 模式
    agent_verbose=True,   # 啟用詳細日誌
)

# 建立 Agent
agent = BaseAgent(config=config)

# 進行對話
request = AgentRequest(message="請幫我完成一個任務")
response = agent.chat(request)
print(response.response)
```

### 非同步使用

```python
import asyncio
from llm_agent import BaseAgent, AgentRequest

async def main():
    agent = BaseAgent()
    request = AgentRequest(message="你好")
    response = await agent.achat(request)
    print(response.response)

asyncio.run(main())
```

### 註冊工具

```python
from llm_agent import BaseAgent, create_tool_from_function

# 定義工具函數
def get_weather(location: str) -> str:
    """取得指定地點的天氣資訊"""
    return f"{location} 的天氣是晴天，溫度 25 度"

# 建立工具
tool = create_tool_from_function(get_weather)

# 建立 Agent 並註冊工具
config = AgentConfig(use_agent_mode=True)  # 必須啟用 Agent 模式才能使用工具
agent = BaseAgent(config=config)
agent.register_tool(tool)

# 使用 Agent（Agent 可以自動呼叫工具）
request = AgentRequest(message="台北的天氣如何？")
response = agent.chat(request)
print(response.response)
```

### 管理 Agent State

```python
from llm_agent import BaseAgent, AgentState

# 建立自訂 State
state = AgentState(session_id="my_session")

# 建立 Agent 並使用自訂 State
agent = BaseAgent(state=state)

# 新增訊息到 State
state.add_message("user", "你好")
state.add_message("assistant", "你好！有什麼我可以幫助你的嗎？")

# 取得對話歷史
history = state.get_chat_history()
print(history)

# 設定 workflow context
state.set_workflow_context("current_task", "天氣查詢")
task = state.get_workflow_context("current_task")
print(task)

# 重置 State
state.reset(keep_session=True)  # 保留 session_id
```

## 配置選項

### 環境變數

Agent 配置可以透過環境變數設定：

```bash
# Ollama 配置
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llama3.2

# Agent 行為配置
export AGENT_TIMEOUT=60.0
export AGENT_VERBOSE=false
export USE_AGENT_MODE=false

# Memory 配置
export MEMORY_TOKEN_LIMIT=4096
```

### AgentConfig 參數

- `ollama_base_url` (str): Ollama API 基礎 URL（預設：`http://localhost:11434`）
- `ollama_model` (str): 使用的模型名稱（預設：`llama3.2`）
- `agent_timeout` (float): 請求超時時間（秒，預設：`60.0`）
- `agent_verbose` (bool): 是否啟用詳細日誌（預設：`False`）
- `use_agent_mode` (bool): 是否使用 ReActAgent 模式（預設：`False`，直接使用 LLM）
- `memory_token_limit` (Optional[int]): Memory token 限制（預設：`None`，無限制）

## 架構概述

### 核心組件

- **BaseAgent**：Agent 基礎類別，提供統一的 API
- **AgentConfig**：配置管理，從環境變數載入配置
- **AgentState**：State 管理器，管理對話上下文、tool result、workflow context
- **ChatMemory**：記憶管理器，封裝 LlamaIndex ChatMemoryBuffer
- **ToolRegistry**：工具註冊表，管理 Agent 可用的工具
- **PromptManager**：Prompt 管理器，提供常用的 prompt 模板

### State 管理

Agent State 包含以下部分：

- **對話歷史**：透過 `ChatMemory` 管理
- **工具執行結果**：記錄所有工具執行結果
- **Workflow Context**：工作流程相關的上下文資訊
- **Prompt Context**：Prompt 相關的上下文資訊
- **Metadata**：其他元資料

## 擴展 BaseAgent

您可以繼承 `BaseAgent` 並實作自己的方法：

```python
from llm_agent import BaseAgent, AgentRequest, AgentResponse

class MyCustomAgent(BaseAgent):
    """自訂 Agent"""
    
    def chat(self, request: AgentRequest) -> AgentResponse:
        # 在呼叫前進行預處理
        processed_message = self.preprocess_message(request.message)
        request.message = processed_message
        
        # 呼叫父類別方法
        response = super().chat(request)
        
        # 在回應後進行後處理
        response.response = self.postprocess_response(response.response)
        
        return response
    
    def preprocess_message(self, message: str) -> str:
        """預處理訊息"""
        # 實作您的預處理邏輯
        return message.upper()
    
    def postprocess_response(self, response: str) -> str:
        """後處理回應"""
        # 實作您的後處理邏輯
        return response.strip()
```

## API 文件

### BaseAgent

#### `__init__(config=None, tools=None, state=None)`

初始化 BaseAgent。

- `config` (Optional[AgentConfig]): Agent 配置
- `tools` (Optional[List]): Agent 工具列表
- `state` (Optional[AgentState]): Agent State 實例

#### `chat(request: AgentRequest) -> AgentResponse`

與 Agent 進行對話（同步版本）。

#### `achat(request: AgentRequest) -> AgentResponse`

與 Agent 進行對話（非同步版本）。

#### `complete(prompt: str, **kwargs) -> str`

完成文字（同步版本）。

#### `acomplete(prompt: str, **kwargs) -> str`

完成文字（非同步版本）。

#### `register_tool(tool) -> None`

註冊工具到 Agent。

#### `reset_state(keep_session=False) -> None`

重置 Agent State。

#### `get_state() -> Dict[str, Any]`

取得 Agent State 的字典表示。

### AgentState

#### `add_message(role: str, content: str) -> None`

新增訊息到對話歷史。

#### `get_chat_history(k=-1) -> List[Dict[str, str]]`

取得對話歷史。

#### `add_tool_result(tool_name: str, result: Any, success=True, error=None) -> None`

新增工具執行結果。

#### `set_workflow_context(key: str, value: Any) -> None`

設定 workflow context。

#### `get_workflow_context(key=None) -> Any`

取得 workflow context。

## 範例

更多範例請參考專案根目錄的範例檔案。

## 開發

### 安裝開發依賴

```bash
cd agent
uv sync --dev
```

### 執行測試

```bash
pytest
```

### 程式碼格式化

```bash
black .
ruff check .
```

## 授權

本專案採用 MIT 授權。

