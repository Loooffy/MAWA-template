# LLM Agent Backend

後端應用程式，使用 FastAPI 提供 API 服務，管理 User State、World State，並整合 LLM Agent。

## 架構概述

本後端採用以下架構：

- **FastAPI**：現代化的 Python Web 框架
- **SQLAlchemy**：ORM 資料庫抽象層
- **Alembic**：資料庫遷移工具
- **儲存抽象層**：支援記憶體、SQLite、PostgreSQL 多種儲存方式
- **State 管理**：User State 和 World State 的獨立管理
- **State Accessor**：提供統一介面供 Agent 存取外部 State

## 安裝

### 使用 uv

```bash
# 安裝依賴
uv pip install -e .

# 或使用 uv sync（如果使用 uv 專案管理）
uv sync
```

### 使用 pip

```bash
pip install -e .
```

## 環境變數配置

### 使用 .env 檔案（推薦）

在 `backend` 目錄下建立 `.env` 檔案，複製 `.env.example` 並根據需求修改：

```bash
# 複製範本檔案
cp .env.example .env

# 編輯 .env 檔案
nano .env  # 或使用你喜歡的編輯器
```

`.env` 檔案範例：

```bash
# Backend Configuration

# 後端服務端口
BACKEND_PORT=8000

# 資料庫連線 URL
# SQLite（開發環境）
DATABASE_URL=sqlite:///./app.db

# PostgreSQL（生產環境）
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# 儲存類型（可選，會根據 DATABASE_URL 自動判斷）
# Options: memory, sqlite, postgresql
# STORAGE_TYPE=sqlite

# Agent Configuration (passed to agent package)
# Ollama base URL
OLLAMA_BASE_URL=http://localhost:11434

# Ollama model name
# OLLAMA_MODEL=gemma2:12b

# Agent timeout in seconds
AGENT_TIMEOUT=60.0

# Use ReActAgent mode (true/false)
USE_AGENT_MODE=false

# Agent verbose logging (true/false)
AGENT_VERBOSE=false
```

### 環境變數說明

#### 後端配置

- `BACKEND_PORT`：後端服務端口（預設：`8000`）

#### 資料庫配置

- `DATABASE_URL`：資料庫連線 URL
  - SQLite（開發環境）：`sqlite:///./app.db`
  - PostgreSQL（生產環境）：`postgresql://user:password@localhost:5432/dbname`
- `STORAGE_TYPE`：儲存類型（可選，會根據 `DATABASE_URL` 自動判斷）
  - 選項：`memory`、`sqlite`、`postgresql`

#### Agent 相關環境變數

後端會將以下環境變數傳遞給 Agent 套件：

- `OLLAMA_BASE_URL`：Ollama API 基礎 URL（預設：`http://localhost:11434`）
- `OLLAMA_MODEL`：使用的模型名稱（可選）
- `AGENT_TIMEOUT`：請求超時時間（秒，預設：`60.0`）
- `USE_AGENT_MODE`：是否使用 ReActAgent 模式（預設：`false`）
- `AGENT_VERBOSE`：是否啟用詳細日誌（預設：`false`）

### 注意事項

- `.env` 檔案包含敏感資訊，不應該提交到版本控制系統
- 使用 `.env.example` 作為範本，團隊成員可以根據此範本建立自己的 `.env` 檔案
- 如果沒有 `.env` 檔案，應用程式會使用環境變數的預設值

## 資料庫遷移

### 初始化資料庫

```bash
# 建立初始 migration
alembic revision --autogenerate -m "Initial migration"

# 執行遷移
alembic upgrade head
```

### 建立新的 Migration

```bash
# 自動生成 migration
alembic revision --autogenerate -m "Description of changes"

# 手動建立 migration
alembic revision -m "Description of changes"
```

### 執行遷移

```bash
# 升級到最新版本
alembic upgrade head

# 降級一個版本
alembic downgrade -1

# 升級到特定版本
alembic upgrade <revision>
```

## 執行方式

### 開發模式

```bash
# 使用 uvicorn
uvicorn app.main:app --reload --port 8000

# 或直接執行
python -m app.main
```

### 生產模式

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API 文件

啟動服務後，可以訪問以下 URL 查看 API 文件：

- Swagger UI：http://localhost:8000/docs
- ReDoc：http://localhost:8000/redoc

## API 端點

### 健康檢查

- `GET /`：根端點，返回健康狀態
- `GET /health`：健康檢查端點

### User State API

- `POST /api/user-states`：建立 User State
- `GET /api/user-states/{state_id}`：取得 User State
- `GET /api/user-states/user/{user_id}`：列出使用者的所有 User State
- `PUT /api/user-states/{state_id}`：更新 User State
- `DELETE /api/user-states/{state_id}`：刪除 User State

### World State API

- `POST /api/world-states`：建立 World State
- `GET /api/world-states`：列出所有 World State
- `GET /api/world-states/{state_id}`：取得 World State
- `GET /api/world-states/key/{key}`：根據 key 取得 World State
- `PUT /api/world-states/{state_id}`：更新 World State
- `PUT /api/world-states/key/{key}`：根據 key 更新 World State
- `DELETE /api/world-states/{state_id}`：刪除 World State

### Agent API

- `POST /api/agent/chat`：與 Agent 對話
- `GET /api/agent/health`：Agent 健康檢查

## 儲存抽象層

後端支援三種儲存方式：

1. **Memory Storage**：記憶體儲存，用於開發和測試
2. **SQLite Storage**：SQLite 資料庫，用於開發環境
3. **PostgreSQL Storage**：PostgreSQL 資料庫，用於生產環境

儲存方式會根據 `DATABASE_URL` 環境變數自動判斷，也可以透過 `STORAGE_TYPE` 環境變數手動指定。

## State 管理

### User State

User State 用於儲存使用者相關的狀態資料。每個 User State 包含：
- `id`：唯一識別碼
- `user_id`：使用者 ID
- `key`：狀態鍵值
- `value`：狀態值（可選）

### World State

World State 用於儲存應用程式中的世界/環境狀態。每個 World State 包含：
- `id`：唯一識別碼
- `key`：狀態鍵值（唯一）
- `value`：狀態值（可選）

### State Accessor

`StateAccessor` 提供統一介面供 Agent 透過 Tool 存取 User State 和 World State。主要方法：

- `get_user_state(user_id, key)`：取得 User State
- `get_user_states(user_id)`：取得使用者的所有 User State
- `set_user_state(user_id, key, value)`：設定 User State
- `get_world_state(key)`：取得 World State
- `get_world_states()`：取得所有 World State
- `set_world_state(key, value)`：設定 World State

## 依賴 Agent 套件

後端依賴 `llm-agent` 套件（位於 `../agent` 目錄）。確保 Agent 套件已正確安裝：

```bash
# 在 agent 目錄中
cd ../agent
uv pip install -e .

# 回到 backend 目錄
cd ../backend
uv pip install -e .
```

## 開發

### 專案結構

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 應用程式入口
│   ├── schemas.py           # API 層的資料模型
│   ├── db/                  # Database 抽象層
│   │   ├── base.py          # SQLAlchemy Base 和 Engine
│   │   ├── session.py       # Session 管理
│   │   ├── models/          # SQLAlchemy Models
│   │   └── storage/         # 儲存抽象層
│   ├── state/               # State 管理
│   │   ├── user_state/      # User State 管理
│   │   ├── world_state/     # World State 管理
│   │   └── state_accessor.py # State Accessor
│   └── api/                 # API 路由
│       ├── user_routes.py   # User State API 路由
│       ├── world_routes.py  # World State API 路由
│       └── agent_routes.py # Agent 互動 API 路由
├── alembic/                 # 資料庫遷移
│   ├── versions/
│   └── env.py
├── alembic.ini              # Alembic 配置
├── pyproject.toml           # 專案配置
└── README.md                # 本文件
```

## 測試

（待實作測試）

## 授權

（待補充）

