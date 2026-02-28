import React, { useState, useRef, useEffect } from 'react';
import { api } from '../lib/api';
import { ChatMessage } from '../types';

export function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [language, setLanguage] = useState(() => localStorage.getItem('lastLanguage') || 'en');
  const [loading, setLoading] = useState(false);
  const [apiAvailable, setApiAvailable] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: input,
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await api.post('/chat', {
        message: input,
        language
      });

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.data.response || response.data.message,
        confidence: response.data.confidence,
        timestamp: Date.now()
      };

      setMessages(prev => [...prev, assistantMessage]);
      setApiAvailable(true);
    } catch (err: any) {
      if (err?.response?.status === 404) {
        setApiAvailable(false);
        const fallbackMessage: ChatMessage = {
          role: 'assistant',
          content: 'Chat backend is not connected yet. This feature will be available soon.',
          timestamp: Date.now()
        };
        setMessages(prev => [...prev, fallbackMessage]);
      } else {
        const errorMessage: ChatMessage = {
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
          timestamp: Date.now()
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-12rem)] flex flex-col">
      <div className="mb-4">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Copilot Chat</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Ask questions about your business data in natural language
        </p>
      </div>

      {/* Language Selector */}
      <div className="mb-4">
        <select
          value={language}
          onChange={e => setLanguage(e.target.value)}
          className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
        >
          <option value="en">English</option>
          <option value="hi">Hindi (हिंदी)</option>
          <option value="mr">Marathi (मराठी)</option>
        </select>
      </div>

      {/* Messages Area */}
      <div className="flex-1 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-y-auto p-4 space-y-4 mb-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-8">
            <div className="text-6xl mb-4">💬</div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              Start a conversation
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Ask me anything about your sales data, inventory, or business insights
            </p>
            <div className="grid grid-cols-1 gap-2 text-sm">
              <button
                onClick={() => setInput('Which products should I order this week?')}
                className="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg text-gray-700 dark:text-gray-300 transition-colors"
              >
                Which products should I order this week?
              </button>
              <button
                onClick={() => setInput('What are my top selling products?')}
                className="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg text-gray-700 dark:text-gray-300 transition-colors"
              >
                What are my top selling products?
              </button>
              <button
                onClick={() => setInput('Are there any demand spikes I should know about?')}
                className="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg text-gray-700 dark:text-gray-300 transition-colors"
              >
                Are there any demand spikes I should know about?
              </button>
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-4 ${
                    msg.role === 'user'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                  {msg.confidence !== undefined && (
                    <div className="mt-2 pt-2 border-t border-gray-300 dark:border-gray-600">
                      <p className="text-xs opacity-75">Confidence: {msg.confidence}%</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
                  <div className="flex gap-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Disclaimer */}
      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3 mb-4 border border-blue-200 dark:border-blue-800">
        <p className="text-sm text-blue-800 dark:text-blue-200">
          💡 AI suggestions are probabilistic. Please verify before acting.
        </p>
      </div>

      {/* Input Area */}
      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={apiAvailable ? "Ask me anything..." : "Chat backend not connected"}
          disabled={loading}
          className="flex-1 px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 disabled:opacity-50"
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-semibold px-6 py-3 rounded-lg transition-colors"
        >
          Send
        </button>
      </div>
    </div>
  );
}
