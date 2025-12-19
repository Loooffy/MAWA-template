// User State 相關型別
export interface UserState {
  id: string;
  user_id: string;
  data: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface UserStateCreate {
  user_id: string;
  data: Record<string, unknown>;
}

export interface UserStateUpdate {
  data?: Record<string, unknown>;
}

// World State 相關型別
export interface WorldState {
  id: string;
  key: string;
  data: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface WorldStateCreate {
  key: string;
  data: Record<string, unknown>;
}

export interface WorldStateUpdate {
  key?: string;
  data?: Record<string, unknown>;
}

// Agent 相關型別
export interface AgentChatRequest {
  session_id: string;
  message: string;
  user_id?: string;
}

export interface AgentChatResponse {
  response: string;
  session_id: string;
}

export interface AgentCompleteRequest {
  session_id: string;
  prompt: string;
  user_id?: string;
}

export interface AgentCompleteResponse {
  response: string;
  session_id: string;
}

