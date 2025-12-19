---
name: LLM Agent Enhanced Web App
overview: 建立一個完整的前後端 web app template，後端使用 FastAPI + uv + LlamaIndex Agent，前端使用 Vite + React + TypeScript + TailwindCSS。

# 從零建立 LLM Agent 前後端 Web App Template

## 專案目標

建立一個可重複使用的 template，用於快速建立支援 LLM Agent 的前後端 web 應用程式。本 template 提供完整的基礎架構，讓開發者可以專注於業務邏輯實作，而無需從零開始建立基礎設施。

### 核心目標

1. **提供可重用的 Agent 基礎架構**：
   - 將 Agent 功能獨立為可重用的 Python 套件（`llm-agent`）
   - 使用 LlamaIndex 作為 Agent 框架，提供統一的 API 和豐富的功能
   - 提供 `BaseAgent` 基礎類別，讓使用者可以快速擴展自己的 Agent
   - 整合 LlamaIndex 的 Memory 管理，自動處理對話歷史

2. **清晰的 State 管理架構**：
   - 採用混合式架構，將不同類型的 State 分離管理
   - **Agent State**：由 Agent 套件內部管理，包含對話上下文、tool result、workflow context 等
   - **User State 和 World State**：由 Backend 管理，透過 API 提供 CRUD 操作
   - **StateAccessor**：提供統一介面，讓 Agent 透過 Tool 存取外部 State
   - 職責分離，易於測試、維護和擴展

3. **靈活的資料持久化方案**：
   - 實作儲存抽象層（`StorageInterface`），支援多種儲存方式
   - 開發環境使用 SQLite，生產環境使用 PostgreSQL
   - 可選的記憶體儲存，便於測試和開發
   - 使用 Alembic 管理資料庫遷移
   - 易於切換不同的儲存實作，無需修改業務邏輯

4. **完整的 Monorepo 架構**：
   - Agent 套件獨立，可在多個專案中重用
   - Backend 和 Frontend 分離，各自獨立開發和部署
   - 清晰的模組邊界，降低耦合度
   - 統一的開發和部署流程

### 架構選擇的理由

- **Monorepo + 獨立 Agent 套件**：
  - 保持 Agent 邏輯的獨立性和可重用性
  - 便於單獨測試和維護 Agent 功能
  - 可在不同專案中重用 Agent 套件

- **LlamaIndex 作為 Agent 框架**：
  - 提供統一的 Agent API 和豐富的功能（Memory、Tools、RAG 等）
  - 支援多種 LLM 後端（Ollama、OpenAI 等）
  - 活躍的社群和持續的更新

- **混合式 State 管理架構**：
  - 職責分離：Agent State 和業務 State 各自管理
  - 易於測試：各 State 可獨立測試
  - 擴展性強：可根據需求擴展不同的 State
  - 符合 Agent 設計模式：透過 Tool 存取外部 State

- **Database 抽象層**：
  - 開發和生產環境使用不同的資料庫，無需修改程式碼
  - 易於測試：可使用記憶體儲存進行單元測試
  - 未來可擴展支援其他儲存方式（Redis、MongoDB 等）

### 適用場景

- 需要整合 LLM Agent 的 web 應用程式
- 需要管理多種 State（Agent、User、World）的應用
- 需要靈活的資料持久化方案的專案
- 希望快速建立基礎架構，專注於業務邏輯開發的團隊

## 專案結構

```
template-project/
├── agent/                        # 獨立的 Agent 套件
│   ├── llm_agent/                # Agent 套件主體
│   │   ├── __init__.py
│   │   ├── agent.py              # 核心 Agent 基礎類別（LlamaIndex）
│   │   ├── config.py             # Agent 配置管理
│   │   ├── prompts.py            # Prompt 模板管理基礎框架
│   │   ├── tools.py              # Agent 工具定義框架（可選）
│   │   ├── utils.py              # 通用工具函數
│   │   ├── schemas.py            # Agent 基礎資料模型
│   │   └── state/                # Agent State 管理
│   │       ├── __init__.py
│   │       ├── agent_state.py    # Agent State 管理器
│   │       └── memory.py         # Memory 管理（整合 LlamaIndex）
│   ├── pyproject.toml            # Agent 套件的配置
│   ├── uv.lock                   # Agent 的依賴鎖定
│   └── README.md                 # Agent 說明文件
│
├── backend/                      # Backend 套件
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI 應用程式入口
│   │   ├── schemas.py            # API 層的資料模型
│   │   ├── db/                   # Database 抽象層
│   │   │   ├── __init__.py
│   │   │   ├── base.py           # SQLAlchemy Base 和 Engine
│   │   │   ├── session.py        # Session 管理
│   │   │   ├── models/           # SQLAlchemy Models
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user_state.py # User State Model
│   │   │   │   └── world_state.py # World State Model
│   │   │   └── storage/          # 儲存抽象層
│   │   │       ├── __init__.py
│   │   │       ├── interface.py  # 儲存介面定義
│   │   │       ├── memory.py     # 記憶體儲存（開發用）
│   │   │       ├── sqlite.py     # SQLite 儲存實作
│   │   │       └── postgresql.py # PostgreSQL 儲存實作
│   │   ├── state/                # State 管理
│   │   │   ├── __init__.py
│   │   │   ├── user_state/       # User State 管理
│   │   │   │   ├── __init__.py
│   │   │   │   ├── manager.py   # User State 管理器
│   │   │   │   └── schemas.py   # User State 資料模型
│   │   │   ├── world_state/      # World State 管理
│   │   │   │   ├── __init__.py
│   │   │   │   ├── manager.py   # World State 管理器
│   │   │   │   └── schemas.py   # World State 資料模型
│   │   │   └── state_accessor.py # 提供 Agent 存取的統一介面
│   │   └── api/                  # API 路由
│   │       ├── __init__.py
│   │       ├── user_routes.py    # User State API 路由
│   │       ├── world_routes.py   # World State API 路由
│   │       └── agent_routes.py   # Agent 互動 API 路由
│   ├── alembic/                  # 資料庫遷移
│   │   ├── versions/
│   │   └── env.py
│   ├── alembic.ini                # Alembic 配置
│   ├── pyproject.toml            # Backend 配置（依賴 agent 套件）
│   ├── uv.lock                   # Backend 的依賴鎖定
│   └── README.md                 # 後端說明文件
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx              # React 應用程式入口
│   │   ├── App.tsx                # 主應用程式組件
│   │   ├── index.css              # TailwindCSS 入口
│   │   ├── components/           # React 組件目錄
│   │   ├── types.ts               # TypeScript 型別定義
│   │   └── api.ts                 # API 客戶端
│   ├── index.html                 # HTML 入口檔案
│   ├── package.json               # npm 依賴配置
│   ├── tsconfig.json              # TypeScript 配置
│   ├── vite.config.ts             # Vite 配置
│   ├── tailwind.config.js         # TailwindCSS 配置
│   ├── postcss.config.js          # PostCSS 配置
│   └── README.md                  # 前端說明文件
│
└── README.md                      # 專案總說明文件
```

## Agent 套件實作

### 1. Agent 套件初始化與依賴管理

- 建立 `agent/pyproject.toml`：
  - 專案名稱：`llm-agent`
  - Python 版本：`>=3.10`
  - 依賴套件：
    - `llama-index>=0.10.0`
    - `llama-index-llms-ollama>=0.1.0`
    - `pydantic>=2.7.0`

### 2. Agent 核心實作

- 建立 `agent/llm_agent/__init__.py`：
  - 匯出主要的類別和函數
  - 定義套件的公開 API

- 建立 `agent/llm_agent/agent.py`：
  - 實作 `BaseAgent` 抽象基礎類別
  - 提供 LlamaIndex 整合的基礎框架
  - 支援使用 `ReActAgent` 或直接使用 LLM
  - 初始化 Ollama LLM 連線的基礎方法
  - 提供可擴展的 `chat()` 和 `complete()` 方法介面
  - 實作通用的回應處理和錯誤處理框架

### 3. Agent 配置管理

- 建立 `agent/llm_agent/config.py`：
  - 定義 `AgentConfig` 類別（使用 Pydantic）
  - 從環境變數載入配置
  - 支援配置驗證和預設值
  - 提供可擴展的配置選項

### 4. Prompt 管理

- 建立 `agent/llm_agent/prompts.py`：
  - 提供 prompt 管理的基礎框架
  - 定義 prompt 模板的介面和工具函數
  - 可選：支援 Jinja2 模板整合（如果需要）
  - 使用者可根據需求擴展自己的 prompt 模板

### 5. Agent 工具（可選）

- 建立 `agent/llm_agent/tools.py`：
  - 提供 Agent 工具的基礎框架
  - 示範如何使用 LlamaIndex 的 `FunctionTool` 包裝工具
  - 提供工具註冊和管理的基礎方法
  - 使用者可根據需求擴展自己的工具

### 6. 工具函數

- 建立 `agent/llm_agent/utils.py`：
  - 提供通用的文字處理工具函數
  - 實作回應解析和驗證的基礎方法
  - 提供 JSON 解析、錯誤處理等通用功能
  - 使用者可根據需求擴展自己的工具函數

### 7. Agent 資料模型

- 建立 `agent/llm_agent/schemas.py`：
  - 定義 Agent 基礎的 Pydantic 模型
  - 提供通用的請求/回應資料結構框架
  - 使用者可根據需求擴展自己的資料模型

### 8. Agent State 管理

- 建立 `agent/llm_agent/state/__init__.py`
- 建立 `agent/llm_agent/state/agent_state.py`：
  - 實作 `AgentState` 類別，管理單一 session 的 Agent state
  - 管理對話上下文、tool result、角色人格和 backstory 等
  - 提供 workflow context 和 prompt context 的管理
- 建立 `agent/llm_agent/state/memory.py`：
  - 整合 LlamaIndex 的 `ChatMemoryBuffer`
  - 管理對話歷史和記憶
  - 提供 memory 的存取介面

### 9. Agent 配置與文件

- 建立 `agent/README.md`：
  - Agent 套件說明和架構概述
  - 安裝和使用方式
  - 配置選項說明
  - 如何擴展 BaseAgent 的範例
  - API 文件

## 後端實作

### 1. 專案初始化與依賴管理

- 建立 `backend/pyproject.toml`：
  - 專案名稱：`llm-agent-backend`
  - Python 版本：`>=3.10`
  - 依賴套件：
    - `fastapi>=0.115.0`
    - `uvicorn[standard]>=0.30.0`
    - `pydantic>=2.7.0`
    - `sqlalchemy>=2.0.0`
    - `alembic>=1.13.0`
    - `psycopg2-binary>=2.9.0`（PostgreSQL 支援）
    - `llm-agent @ {path = "../agent", editable = true}`（本地依賴）

### 2. FastAPI 應用程式結構

- 建立 `backend/app/__init__.py`（空檔案）
- 建立 `backend/app/main.py`：
  - 初始化 FastAPI 應用程式
  - 設定 CORS（允許前端連線）
  - 使用 FastAPI 的 `Depends` 注入 Agent 實例和 State Manager
  - 註冊 API 路由（user_routes, world_routes, agent_routes）
  - 整合 State Accessor 供 Agent 使用

### 3. Database 抽象層實作

- 建立 `backend/app/db/__init__.py`
- 建立 `backend/app/db/base.py`：
  - 定義 SQLAlchemy Base 和 Engine
  - 支援 SQLite（開發環境）和 PostgreSQL（生產環境）
  - 根據環境變數切換資料庫連線
- 建立 `backend/app/db/session.py`：
  - 實作 Session 管理
  - 提供 FastAPI 依賴注入的 Session 取得方法
- 建立 `backend/app/db/models/__init__.py`
- 建立 `backend/app/db/models/user_state.py`：
  - 定義 User State 的 SQLAlchemy Model
- 建立 `backend/app/db/models/world_state.py`：
  - 定義 World State 的 SQLAlchemy Model
- 建立 `backend/app/db/storage/__init__.py`
- 建立 `backend/app/db/storage/interface.py`：
  - 定義 `StorageInterface` 抽象類別
  - 提供 CRUD 方法介面（create, get, update, delete, list）
- 建立 `backend/app/db/storage/memory.py`：
  - 實作記憶體儲存（開發/測試用）
- 建立 `backend/app/db/storage/sqlite.py`：
  - 實作 SQLite 儲存（開發環境）
- 建立 `backend/app/db/storage/postgresql.py`：
  - 實作 PostgreSQL 儲存（生產環境）

### 4. 資料庫遷移設定

- 建立 `backend/alembic.ini`：
  - Alembic 配置檔案
- 建立 `backend/alembic/env.py`：
  - Alembic 環境設定
  - 整合 SQLAlchemy Base 和 Models
- 建立初始 migration：
  - 建立 User State 和 World State 的資料表

### 5. State 管理實作

- 建立 `backend/app/state/__init__.py`
- 建立 `backend/app/state/user_state/`：
  - `manager.py`：實作 `UserStateManager`，使用儲存介面進行 CRUD 操作
  - `schemas.py`：定義 User State 的 Pydantic 資料模型
- 建立 `backend/app/state/world_state/`：
  - `manager.py`：實作 `WorldStateManager`，使用儲存介面進行 CRUD 操作
  - `schemas.py`：定義 World State 的 Pydantic 資料模型
- 建立 `backend/app/state/state_accessor.py`：
  - 實作 `StateAccessor` 類別，提供 Agent 存取 User State 和 World State 的統一介面
  - 透過依賴注入或單例模式提供給 Agent 使用

### 6. API 路由實作

- 建立 `backend/app/api/__init__.py`
- 建立 `backend/app/api/user_routes.py`：
  - 定義 User State 的 CRUD API 路由
  - 供前端直接操作 User State
- 建立 `backend/app/api/world_routes.py`：
  - 定義 World State 的 CRUD API 路由
  - 供前端直接操作 World State
- 建立 `backend/app/api/agent_routes.py`：
  - 定義 Agent 互動的 API 路由
  - 整合 Agent 套件和 State Accessor

### 5. 資料模型定義

- 建立 `backend/app/schemas.py`：
  - 使用 Pydantic 定義 API 請求/回應模型
  - 定義通用的請求/回應資料結構
  - 可以從 `llm_agent.schemas` 匯入共享的模型

### 6. 後端配置與文件

- 建立 `backend/README.md`：
  - 安裝說明（使用 uv）
  - 環境變數配置
  - 執行方式
  - API 文件連結
  - 說明如何依賴 agent 套件

## 前端實作

### 1. 專案初始化與依賴管理

- 建立 `frontend/package.json`：
  - 專案名稱：`llm-agent-frontend`
  - 依賴套件：
    - `react>=18.0.0`
    - `react-dom>=18.0.0`
  - 開發依賴：
    - `typescript>=5.0.0`
    - `vite>=5.0.0`
    - `@vitejs/plugin-react>=4.0.0`
    - `tailwindcss>=3.4.0`
    - `postcss>=8.4.0`
    - `autoprefixer>=10.4.0`
    - `@types/react>=18.0.0`
    - `@types/react-dom>=18.0.0`

### 2. Vite 配置

- 建立 `frontend/vite.config.ts`：
  - 設定 React 插件
  - 設定開發伺服器（port、proxy）
  - 設定路徑別名（@ 指向 src）

### 3. TypeScript 配置

- 建立 `frontend/tsconfig.json`：
  - 設定編譯選項
  - 設定路徑別名
  - 設定 JSX 模式

### 4. TailwindCSS 配置

- 建立 `frontend/tailwind.config.js`：
  - 設定 content paths（掃描所有 React 組件）
  - 設定主題（可選）
- 建立 `frontend/postcss.config.js`：
  - 設定 TailwindCSS 和 Autoprefixer 插件
- 建立 `frontend/src/index.css`：
  - 引入 TailwindCSS directives

### 5. React 應用程式結構

- 建立 `frontend/index.html`：
  - 基本 HTML 結構
  - 引入 main.tsx
- 建立 `frontend/src/main.tsx`：
  - React 應用程式入口
  - 引入 index.css
- 建立 `frontend/src/App.tsx`：
  - 主應用程式組件
  - 基本 UI 結構（使用 TailwindCSS）
- 建立 `frontend/src/types.ts`：
  - TypeScript 型別定義
- 建立 `frontend/src/api.ts`：
  - API 客戶端函數
  - 使用 axios

### 6. 範例組件

- 建立 `frontend/src/components/` 目錄
- 建立基本範例組件（可選，如 `ExampleComponent.tsx`）

### 7. 前端配置與文件

- 建立 `frontend/README.md`：
  - 安裝說明（使用 npm/yarn/pnpm）
  - 執行方式
  - 環境變數配置

## 專案根目錄

- 建立 `README.md`：
  - 專案總覽
  - 快速開始指南
  - 前後端分別的啟動說明
  - 技術棧說明

## State 管理架構

### State 分類與職責

1. **Agent State**（Agent 套件管理）：
   - 對話上下文（conversation history）
   - Tool result（工具執行結果）
   - 角色人格和 backstory
   - Workflow context（工作流程間的狀態傳遞）
   - Prompt context（用於合成 prompt 的上下文）

2. **User State**（Backend 管理）：
   - 使用者相關的資料和狀態
   - 透過前端 API 進行 CRUD 操作
   - Agent 可透過 Tool 存取以調整回應內容

3. **World State**（Backend 管理）：
   - 應用程式中的世界/環境狀態
   - 透過前端 API 進行 CRUD 操作
   - Agent 可透過 Tool 讀取和修改

### State 互動方式

- **前端 → User State**：透過 API 直接進行 CRUD 操作
- **前端 → World State**：透過 API 直接進行 CRUD 操作
- **前端 → Agent**：透過文字輸入與 Agent 互動
- **Agent → World State**：透過 Tool 讀取和修改
- **Agent → User State**：透過 Tool 讀取以調整回應
- **Agent → Agent State**：內部管理，用於合成 prompt 和 workflow

### State 管理實作

採用**混合式架構（方案 E）**：

- User State 和 World State 各自獨立管理，由 Backend 的 State Manager 負責
- Agent State 由 Agent 套件內部管理
- `StateAccessor` 提供統一介面供 Agent 透過 Tool 存取外部 State
- 前端透過 API 直接操作 User State 和 World State

## 實作細節

### Agent 套件關鍵實作

1. **LlamaIndex 整合**：

   - 使用 `llama-index-llms-ollama` 整合 Ollama
   - 可選擇使用 `ReActAgent` 或直接使用 LLM
   - 支援非同步操作（`achat`、`acomplete`）
   - 實作錯誤處理和重試機制

2. **Agent 配置**：

   - 使用 Pydantic 管理配置
   - 支援環境變數載入
   - 可配置模型名稱、URL、timeout 等

3. **Agent State 管理**：

   - 使用 `AgentStateManager` 管理各 session 的 Agent state
   - 整合 LlamaIndex 的 `ChatMemoryBuffer` 管理對話歷史
   - 提供 workflow context 和 prompt context 的管理介面
   - 支援自定義 context 的添加和存取

4. **Prompt 管理**：

   - 在 `prompts.py` 中提供 prompt 管理的基礎框架
   - 可選：支援 Jinja2 模板（如果需要動態生成）
   - 保持 prompt 的可維護性和可測試性
   - 使用者可根據需求擴展自己的 prompt 模板

5. **工具函數**：

   - 提供通用的工具函數框架
   - 保持 Agent 核心邏輯的簡潔性
   - 方便單元測試和擴展
   - 使用者可根據需求添加自己的工具函數

6. **State Access Tools**：

   - 在 `tools.py` 中提供存取外部 State 的工具框架
   - 透過 `StateAccessor` 存取 User State 和 World State
   - 使用 LlamaIndex 的 `FunctionTool` 包裝工具

### 後端關鍵實作

1. **Database 抽象層**：

   - 使用 SQLAlchemy 作為 ORM
   - 實作 `StorageInterface` 抽象介面
   - 支援多種儲存實作：記憶體、SQLite、PostgreSQL
   - 根據環境變數自動選擇儲存方式
   - 開發環境預設使用 SQLite，生產環境使用 PostgreSQL
   - 使用 Alembic 管理資料庫遷移

2. **State 管理**：

   - `UserStateManager` 和 `WorldStateManager` 使用儲存介面進行操作
   - 提供 CRUD 操作介面
   - 支援 session 或 user 層級的狀態隔離
   - 透過儲存抽象層實現持久化
   - 易於切換不同的儲存實作（記憶體/資料庫）

3. **State Accessor**：

   - 提供統一介面供 Agent 存取 User State 和 World State
   - 透過依賴注入或單例模式提供給 Agent
   - 實作權限控制和資料驗證

4. **Agent 依賴注入**：

   - 使用 FastAPI 的 `Depends` 注入 Agent 實例和 State Accessor
   - 可以選擇單例模式或每次請求創建新實例
   - 支援配置的靈活傳遞

5. **API 路由設計**：

   - User State 和 World State 各自有獨立的 API 路由
   - Agent 互動有專門的 API 路由
   - 保持 API 層的簡潔，只負責請求/回應處理
   - 實作適當的錯誤處理和回應格式

6. **FastAPI 設定**：

   - 設定適當的 CORS 政策
   - 提供 API 文件（自動生成）
   - 實作基本的健康檢查端點
   - 可選：實作 State 和 Agent 健康檢查端點

### 前端關鍵實作

1. **TailwindCSS 整合**：

   - 使用標準安裝流程
   - 配置 content paths 包含所有 `.tsx`、`.ts`、`.jsx`、`.js` 檔案
   - 確保開發和生產環境都能正確編譯

2. **TypeScript 設定**：

   - 啟用嚴格模式
   - 設定適當的模組解析
   - 配置路徑別名

3. **Vite 設定**：

   - 設定開發伺服器 proxy 指向後端
   - 配置適當的構建選項

## 環境變數配置

### Agent 套件

- `OLLAMA_BASE_URL`：Ollama API 基礎 URL（預設：`http://localhost:11434`）
- `OLLAMA_MODEL`：使用的模型名稱（預設：可設定，如 `gemma3:12b`）
- `AGENT_TIMEOUT`：請求超時時間（秒，預設：`60.0`）
- `AGENT_VERBOSE`：是否啟用詳細日誌（預設：`false`）
- `USE_AGENT_MODE`：是否使用 ReActAgent 模式（預設：`false`，直接使用 LLM）

### 後端

- `BACKEND_PORT`：後端服務端口（預設：`8000`）
- `DATABASE_URL`：資料庫連線 URL
  - 開發環境（SQLite）：`sqlite:///./app.db`（預設）
  - 生產環境（PostgreSQL）：`postgresql://user:password@localhost/dbname`
- `STORAGE_TYPE`：儲存類型（`memory`、`sqlite`、`postgresql`，預設：根據 DATABASE_URL 自動判斷）
- 後端會將 Agent 相關的環境變數傳遞給 Agent 套件

### 前端

- `VITE_BACKEND_URL`：後端 API URL（預設：`http://localhost:8000`）

## 驗證點

### Agent 套件

1. Agent 套件可以成功安裝（使用 `uv pip install -e agent/`）
2. Agent 可以成功初始化並連接到 Ollama
3. Agent 基礎類別可以成功實例化
4. Agent 可以成功執行基本的 chat 和 complete 操作
5. Agent 的工具函數和配置管理正常工作
6. 使用者可以成功擴展 BaseAgent 建立自己的 Agent

### 後端

1. 後端可以成功安裝並依賴 Agent 套件
2. 資料庫連線可以正常建立（SQLite/PostgreSQL）
3. Alembic 遷移可以正常執行
4. 後端可以成功啟動並提供 API 文件
5. 後端可以成功注入 Agent 實例和 State Manager
6. 後端可以成功呼叫 Agent 的方法
7. 儲存抽象層可以正常切換（記憶體/SQLite/PostgreSQL）
8. User State Manager 可以正常進行 CRUD 操作（透過儲存介面）
9. World State Manager 可以正常進行 CRUD 操作（透過儲存介面）
10. State Accessor 可以正常提供給 Agent 使用
11. 後端 API 路由（user, world, agent）正常工作
12. 資料持久化功能正常（資料可以正確儲存和讀取）

### 前端

1. 前端可以成功啟動開發伺服器
2. 前端可以正確編譯 TailwindCSS 樣式
3. 前端可以成功呼叫後端 API
4. 前端可以成功操作 User State 和 World State
5. 前後端可以正常協作

### State 管理測試

1. Agent State 可以正常管理對話上下文和 memory
2. User State 可以透過 API 正常進行 CRUD 操作
3. World State 可以透過 API 正常進行 CRUD 操作
4. Agent 可以透過 Tool 正常存取 User State 和 World State
5. State Accessor 可以正確提供統一介面
6. 多個 session 的 state 可以正確隔離

### 整合測試

1. 完整的端到端流程：前端 → 後端 → Agent → Ollama → 回應
2. 前端操作 State → 後端更新 → Agent 透過 Tool 讀取 → 合成 prompt
3. Agent 透過 Tool 修改 State → 後端更新 → 前端同步
4. 錯誤處理機制正常工作
5. 環境變數配置正確傳遞
6. Agent 擴展性測試：使用者可以成功繼承 BaseAgent 並實作自己的方法

todos:
  - id: agent-pyproject
    content: 建立 agent/pyproject.toml，配置 uv 專案和 LlamaIndex 相關依賴
    status: pending
  - id: agent-init
    content: 建立 agent/llm_agent/__init__.py，定義套件公開 API
    status: pending
  - id: agent-schemas
    content: 建立 agent/llm_agent/schemas.py，定義 Agent 基礎資料模型框架
    status: pending
  - id: agent-config
    content: 建立 agent/llm_agent/config.py，實作 Agent 配置管理
    status: pending
  - id: agent-prompts
    content: 建立 agent/llm_agent/prompts.py，提供 prompt 管理基礎框架
    status: pending
  - id: agent-utils
    content: 建立 agent/llm_agent/utils.py，提供通用工具函數框架
    status: pending
  - id: agent-tools
    content: 建立 agent/llm_agent/tools.py，提供 Agent 工具定義框架（可選）
    status: pending
  - id: agent-state-memory
    content: 建立 agent/llm_agent/state/memory.py，整合 LlamaIndex Memory
    status: pending
  - id: agent-state-manager
    content: 建立 agent/llm_agent/state/agent_state.py，實作 Agent State 管理
    status: pending
    dependencies:
      - agent-state-memory
  - id: agent-core
    content: 建立 agent/llm_agent/agent.py，實作 BaseAgent 基礎類別
    status: pending
    dependencies:
      - agent-config
      - agent-prompts
      - agent-schemas
      - agent-utils
      - agent-state-manager
  - id: agent-readme
    content: 建立 agent/README.md 說明文件
    status: pending
  - id: backend-pyproject
    content: 建立 backend/pyproject.toml，配置 uv 專案和依賴 agent 套件
    status: pending
    dependencies:
      - agent-pyproject
  - id: backend-init
    content: 建立 backend/app/__init__.py
    status: pending
  - id: backend-db-base
    content: 建立 backend/app/db/base.py，定義 SQLAlchemy Base 和 Engine
    status: pending
  - id: backend-db-session
    content: 建立 backend/app/db/session.py，實作 Session 管理
    status: pending
  - id: backend-db-storage-interface
    content: 建立 backend/app/db/storage/interface.py，定義儲存抽象介面
    status: pending
  - id: backend-db-storage-memory
    content: 建立 backend/app/db/storage/memory.py，實作記憶體儲存
    status: pending
    dependencies:
      - backend-db-storage-interface
  - id: backend-db-storage-sqlite
    content: 建立 backend/app/db/storage/sqlite.py，實作 SQLite 儲存
    status: pending
    dependencies:
      - backend-db-storage-interface
      - backend-db-base
  - id: backend-db-storage-postgresql
    content: 建立 backend/app/db/storage/postgresql.py，實作 PostgreSQL 儲存
    status: pending
    dependencies:
      - backend-db-storage-interface
      - backend-db-base
  - id: backend-db-models-user
    content: 建立 backend/app/db/models/user_state.py，定義 User State Model
    status: pending
    dependencies:
      - backend-db-base
  - id: backend-db-models-world
    content: 建立 backend/app/db/models/world_state.py，定義 World State Model
    status: pending
    dependencies:
      - backend-db-base
  - id: backend-alembic-config
    content: 建立 backend/alembic.ini 和 alembic/env.py，設定資料庫遷移
    status: pending
    dependencies:
      - backend-db-base
      - backend-db-models-user
      - backend-db-models-world
  - id: backend-alembic-initial
    content: 建立初始 Alembic migration，建立 User State 和 World State 資料表
    status: pending
    dependencies:
      - backend-alembic-config
  - id: backend-user-state-schemas
    content: 建立 backend/app/state/user_state/schemas.py，定義 User State 資料模型
    status: pending
  - id: backend-user-state-manager
    content: 建立 backend/app/state/user_state/manager.py，實作 UserStateManager，整合儲存介面
    status: pending
    dependencies:
      - backend-user-state-schemas
      - backend-db-storage-interface
  - id: backend-world-state-schemas
    content: 建立 backend/app/state/world_state/schemas.py，定義 World State 資料模型
    status: pending
  - id: backend-world-state-manager
    content: 建立 backend/app/state/world_state/manager.py，實作 WorldStateManager，整合儲存介面
    status: pending
    dependencies:
      - backend-world-state-schemas
      - backend-db-storage-interface
  - id: backend-state-accessor
    content: 建立 backend/app/state/state_accessor.py，實作 StateAccessor 統一介面
    status: pending
    dependencies:
      - backend-user-state-manager
      - backend-world-state-manager
  - id: backend-schemas
    content: 建立 backend/app/schemas.py，定義 API 層的 Pydantic 資料模型
    status: pending
  - id: backend-user-routes
    content: 建立 backend/app/api/user_routes.py，定義 User State API 路由
    status: pending
    dependencies:
      - backend-user-state-manager
  - id: backend-world-routes
    content: 建立 backend/app/api/world_routes.py，定義 World State API 路由
    status: pending
    dependencies:
      - backend-world-state-manager
  - id: backend-agent-routes
    content: 建立 backend/app/api/agent_routes.py，定義 Agent 互動 API 路由
    status: pending
    dependencies:
      - agent-core
      - backend-state-accessor
  - id: backend-main
    content: 建立 backend/app/main.py，實作 FastAPI 應用程式並註冊所有路由，初始化資料庫連線
    status: pending
    dependencies:
      - backend-user-routes
      - backend-world-routes
      - backend-agent-routes
      - backend-db-base
      - backend-db-session
  - id: backend-readme
    content: 建立 backend/README.md 說明文件
    status: pending
  - id: frontend-package
    content: 建立 frontend/package.json，配置所有依賴（包括 TailwindCSS）
    status: pending
  - id: frontend-tsconfig
    content: 建立 frontend/tsconfig.json TypeScript 配置
    status: pending
  - id: frontend-vite-config
    content: 建立 frontend/vite.config.ts Vite 配置
    status: pending
  - id: frontend-tailwind-config
    content: 建立 frontend/tailwind.config.js TailwindCSS 配置
    status: pending
  - id: frontend-postcss-config
    content: 建立 frontend/postcss.config.js PostCSS 配置
    status: pending
  - id: frontend-index-css
    content: 建立 frontend/src/index.css，引入 TailwindCSS directives
    status: pending
  - id: frontend-index-html
    content: 建立 frontend/index.html HTML 入口檔案
    status: pending
  - id: frontend-types
    content: 建立 frontend/src/types.ts TypeScript 型別定義
    status: pending
  - id: frontend-api
    content: 建立 frontend/src/api.ts API 客戶端
    status: pending
    dependencies:
      - frontend-types
  - id: frontend-main
    content: 建立 frontend/src/main.tsx React 應用程式入口
    status: pending
    dependencies:
      - frontend-index-css
  - id: frontend-app
    content: 建立 frontend/src/App.tsx 主應用程式組件
    status: pending
    dependencies:
      - frontend-api
      - frontend-types
  - id: frontend-readme
    content: 建立 frontend/README.md 說明文件
    status: pending
  - id: root-readme
    content: 建立專案根目錄 README.md 總說明文件
    status: pending
---