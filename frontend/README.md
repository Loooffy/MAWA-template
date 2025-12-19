# Frontend - LLM Agent Web App

這是 LLM Agent Web App 的前端應用程式，使用 React + TypeScript + Vite + TailwindCSS 建置。

## 技術棧

- **React 18**: UI 框架
- **TypeScript**: 型別安全
- **Vite**: 建置工具和開發伺服器
- **TailwindCSS**: 樣式框架
- **Axios**: HTTP 客戶端

## 安裝

使用 npm、yarn 或 pnpm 安裝依賴：

```bash
# 使用 npm
npm install

# 使用 yarn
yarn install

# 使用 pnpm
pnpm install
```

## 開發

啟動開發伺服器：

```bash
npm run dev
# 或
yarn dev
# 或
pnpm dev
```

應用程式將在 `http://localhost:3000` 啟動。

## 建置

建置生產版本：

```bash
npm run build
# 或
yarn build
# 或
pnpm build
```

建置產物將位於 `dist` 目錄。

## 預覽建置結果

預覽生產建置：

```bash
npm run preview
# 或
yarn preview
# 或
pnpm preview
```

## 環境變數

### 設定環境變數

在專案根目錄建立 `.env` 檔案（或 `.env.local`）來設定環境變數。可以參考 `.env.example` 檔案：

```bash
# 複製範例檔案
cp .env.example .env
```

### 可用的環境變數

```env
# 後端 API 基礎 URL
# 在開發環境中，Vite proxy 會將 /api/* 轉發到此 URL
# 在生產環境中，前端會直接使用此 URL
VITE_BACKEND_URL=http://localhost:8000

# 開發環境是否直接使用後端 URL（不使用 proxy）
# 設為 'true' 時，開發環境將直接連線到 VITE_BACKEND_URL，不使用 proxy
# 預設為 false（使用 proxy）
VITE_USE_DIRECT_URL=false
```

- `VITE_BACKEND_URL`: 後端 API 的基礎 URL（預設：`http://localhost:8000`）
- `VITE_USE_DIRECT_URL`: 開發環境是否直接使用後端 URL，不使用 proxy（預設：`false`）

### 開發環境 vs 生產環境

**開發環境（`npm run dev`）**：
- 預設使用 proxy：前端使用 `/api` 作為 base URL，Vite proxy 會將請求轉發到 `VITE_BACKEND_URL`
- 如果設定 `VITE_USE_DIRECT_URL=true`：前端直接連線到 `VITE_BACKEND_URL`

**生產環境（`npm run build`）**：
- 前端直接使用 `VITE_BACKEND_URL` 作為 API base URL
- 必須確保生產環境的 `.env` 檔案包含正確的後端 URL

### 注意事項

- Vite 要求環境變數必須以 `VITE_` 開頭才能在客戶端程式碼中使用
- `.env` 檔案不應該提交到版本控制系統（已加入 `.gitignore`）
- 不同環境可以使用不同的檔案：
  - `.env` - 所有環境
  - `.env.local` - 所有環境，但會被 git 忽略
  - `.env.development` - 僅開發環境
  - `.env.production` - 僅生產環境

## API 整合

前端透過 `src/api.ts` 中的 API 客戶端與後端通訊：

- **User State API**: 管理使用者狀態的 CRUD 操作
- **World State API**: 管理世界狀態的 CRUD 操作
- **Agent API**: 與 LLM Agent 互動（聊天和完成提示）

## 專案結構

```
frontend/
├── src/
│   ├── api.ts          # API 客戶端函數
│   ├── App.tsx         # 主應用程式組件
│   ├── main.tsx        # 應用程式入口
│   ├── types.ts        # TypeScript 型別定義
│   └── index.css       # TailwindCSS 樣式
├── index.html          # HTML 入口檔案
├── package.json        # 專案配置和依賴
├── tsconfig.json       # TypeScript 配置
├── vite.config.ts      # Vite 配置
├── tailwind.config.js  # TailwindCSS 配置
└── postcss.config.js   # PostCSS 配置
```

## 開發伺服器 Proxy

Vite 開發伺服器預設配置了 proxy，會將 `/api/*` 的請求轉發到後端。這樣在開發時可以避免 CORS 問題。

proxy 設定在 `vite.config.ts` 中，會從環境變數 `VITE_BACKEND_URL` 讀取後端 URL。

**使用 proxy（預設）**：
- 前端 API 請求使用 `/api` 作為 base URL
- Vite 自動將 `/api/*` 轉發到 `VITE_BACKEND_URL`
- 避免 CORS 問題

**不使用 proxy**：
- 設定 `VITE_USE_DIRECT_URL=true` 在 `.env` 檔案中
- 前端直接連線到 `VITE_BACKEND_URL`
- 需要確保後端有正確的 CORS 設定

## 功能說明

### 與 Agent 對話

在主畫面可以：
- 設定 Session ID 和 User ID
- 輸入訊息與 Agent 進行對話
- 查看對話歷史記錄

### State 管理

可以透過按鈕建立：
- **User State**: 建立使用者狀態
- **World State**: 建立世界狀態

（完整的 CRUD 操作可透過 API 客戶端實作）

