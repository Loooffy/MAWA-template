# LLM Agent Web App Template

一個完整的 LLM Agent 前後端 Web 應用程式模板，採用 Monorepo 架構，讓開發者能快速建立支援 AI Agent 的應用程式。

## 專案架構

本專案包含三個核心模組：

- **Agent 套件** (`agent/`)：基於 LlamaIndex 的獨立可重用 Python 套件，提供 `BaseAgent` 基礎類別與對話記憶管理
- **後端** (`backend/`)：FastAPI 應用，管理 User State、World State，並整合 Agent 功能
- **前端** (`frontend/`)：React + TypeScript + TailwindCSS 應用，提供現代化的使用者介面

## 核心特色

- **清晰的 State 管理**：分離 Agent State、User State 和 World State，透過 `StateAccessor` 提供統一存取介面
- **靈活的資料持久化**：支援 SQLite（開發）與 PostgreSQL（生產），實作儲存抽象層便於切換
- **完整的開發工具鏈**：使用 `uv` 管理 Python 依賴，Vite 作為前端建置工具，Alembic 管理資料庫遷移

## 快速開始

詳細的安裝與使用說明請參考各子目錄的 README 檔案。

## 技術棧

- **Agent**: LlamaIndex, Ollama
- **後端**: FastAPI, SQLAlchemy, Alembic, uv
- **前端**: React, TypeScript, Vite, TailwindCSS

