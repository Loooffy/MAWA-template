import { useState } from 'react';
import { agentApi, userStateApi, worldStateApi } from './api';
import type { AgentChatRequest, UserStateCreate, WorldStateCreate } from './types';

function App() {
  const [message, setMessage] = useState('');
  const [sessionId, setSessionId] = useState('default-session');
  const [userId, setUserId] = useState('default-user');
  const [chatHistory, setChatHistory] = useState<Array<{ role: 'user' | 'agent'; content: string }>>([]);
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;
    setMessage('');
    setChatHistory(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const request: AgentChatRequest = {
        session_id: sessionId,
        message: userMessage,
        user_id: userId,
      };
      const response = await agentApi.chat(request);
      setChatHistory(prev => [...prev, { role: 'agent', content: response.response }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setChatHistory(prev => [...prev, { role: 'agent', content: '錯誤：無法連接到後端服務。' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUserState = async () => {
    try {
      const data: UserStateCreate = {
        user_id: userId,
        data: { created_at: new Date().toISOString() },
      };
      await userStateApi.create(data);
      alert('User State 建立成功！');
    } catch (error) {
      console.error('Error creating user state:', error);
      alert('建立 User State 失敗');
    }
  };

  const handleCreateWorldState = async () => {
    try {
      const data: WorldStateCreate = {
        key: 'example-key',
        data: { created_at: new Date().toISOString() },
      };
      await worldStateApi.create(data);
      alert('World State 建立成功！');
    } catch (error) {
      console.error('Error creating world state:', error);
      alert('建立 World State 失敗');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">LLM Agent Web App</h1>

        {/* 設定區域 */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">設定</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Session ID
              </label>
              <input
                type="text"
                value={sessionId}
                onChange={(e) => setSessionId(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                User ID
              </label>
              <input
                type="text"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <div className="mt-4 flex gap-2">
            <button
              onClick={handleCreateUserState}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              建立 User State
            </button>
            <button
              onClick={handleCreateWorldState}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              建立 World State
            </button>
          </div>
        </div>

        {/* 聊天區域 */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">與 Agent 對話</h2>

          {/* 聊天歷史 */}
          <div className="h-96 overflow-y-auto mb-4 border border-gray-200 rounded-md p-4 bg-gray-50">
            {chatHistory.length === 0 ? (
              <div className="text-gray-500 text-center mt-8">
                開始與 Agent 對話吧！
              </div>
            ) : (
              <div className="space-y-4">
                {chatHistory.map((item, index) => (
                  <div
                    key={index}
                    className={`flex ${item.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                        item.role === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-white text-gray-800 border border-gray-300'
                      }`}
                    >
                      <div className="text-sm font-medium mb-1">
                        {item.role === 'user' ? '您' : 'Agent'}
                      </div>
                      <div className="whitespace-pre-wrap">{item.content}</div>
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="flex justify-start">
                    <div className="bg-white text-gray-800 border border-gray-300 px-4 py-2 rounded-lg">
                      <div className="text-sm font-medium mb-1">Agent</div>
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* 輸入區域 */}
          <div className="flex gap-2">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="輸入訊息..."
              disabled={loading}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
            />
            <button
              onClick={handleSendMessage}
              disabled={loading || !message.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              傳送
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

