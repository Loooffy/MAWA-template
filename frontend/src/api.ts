import axios from 'axios';
import type {
  UserState,
  UserStateCreate,
  UserStateUpdate,
  WorldState,
  WorldStateCreate,
  WorldStateUpdate,
  AgentChatRequest,
  AgentChatResponse,
  AgentCompleteRequest,
  AgentCompleteResponse,
} from './types';

// API 基礎 URL 配置
// 開發環境：使用 proxy（/api）或直接使用環境變數中的 URL
// 生產環境：使用環境變數中的 URL
const getApiBaseUrl = (): string => {
  // 如果在開發環境且指定了 VITE_BACKEND_URL，則直接使用（不使用 proxy）
  if (import.meta.env.DEV && import.meta.env.VITE_BACKEND_URL && import.meta.env.VITE_USE_DIRECT_URL === 'true') {
    return import.meta.env.VITE_BACKEND_URL;
  }
  // 生產環境使用環境變數中的 URL
  if (import.meta.env.PROD) {
    return import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
  }
  // 開發環境預設使用 proxy
  return '/api';
};

const API_BASE_URL = getApiBaseUrl();

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// User State API
export const userStateApi = {
  // 列出所有 User State
  list: async (): Promise<UserState[]> => {
    const response = await apiClient.get<UserState[]>('/users');
    return response.data;
  },

  // 取得特定 User State
  get: async (user_id: string): Promise<UserState> => {
    const response = await apiClient.get<UserState>(`/users/${user_id}`);
    return response.data;
  },

  // 建立 User State
  create: async (data: UserStateCreate): Promise<UserState> => {
    const response = await apiClient.post<UserState>('/users', data);
    return response.data;
  },

  // 更新 User State
  update: async (user_id: string, data: UserStateUpdate): Promise<UserState> => {
    const response = await apiClient.put<UserState>(`/users/${user_id}`, data);
    return response.data;
  },

  // 刪除 User State
  delete: async (user_id: string): Promise<void> => {
    await apiClient.delete(`/users/${user_id}`);
  },
};

// World State API
export const worldStateApi = {
  // 列出所有 World State
  list: async (): Promise<WorldState[]> => {
    const response = await apiClient.get<WorldState[]>('/world');
    return response.data;
  },

  // 取得特定 World State
  get: async (key: string): Promise<WorldState> => {
    const response = await apiClient.get<WorldState>(`/world/${key}`);
    return response.data;
  },

  // 建立 World State
  create: async (data: WorldStateCreate): Promise<WorldState> => {
    const response = await apiClient.post<WorldState>('/world', data);
    return response.data;
  },

  // 更新 World State
  update: async (key: string, data: WorldStateUpdate): Promise<WorldState> => {
    const response = await apiClient.put<WorldState>(`/world/${key}`, data);
    return response.data;
  },

  // 刪除 World State
  delete: async (key: string): Promise<void> => {
    await apiClient.delete(`/world/${key}`);
  },
};

// Agent API
export const agentApi = {
  // 與 Agent 聊天
  chat: async (request: AgentChatRequest): Promise<AgentChatResponse> => {
    const response = await apiClient.post<AgentChatResponse>('/agent/chat', request);
    return response.data;
  },

  // 完成提示（非對話模式）
  complete: async (request: AgentCompleteRequest): Promise<AgentCompleteResponse> => {
    const response = await apiClient.post<AgentCompleteResponse>('/agent/complete', request);
    return response.data;
  },
};

