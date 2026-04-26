'use client';
import { useState, useEffect } from 'react';
import { chatService } from '@/lib/api';
import { ChatMessage, ChatInput, ChatHeader, TypingIndicator } from './';

// Helper to get user ID from JWT token
const getUserIdFromToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  const token = localStorage.getItem('token');
  if (!token) return null;

  try {
    const cleanToken = token.startsWith('"') ? JSON.parse(token) : token;
    const base64Url = cleanToken.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      window.atob(base64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join('')
    );
    const payload = JSON.parse(jsonPayload);
    return payload.sub || null;
  } catch {
    return null;
  }
};

export default function ChatWidget() {
  const [messages, setMessages] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [convId, setConvId] = useState<number | null>(null);
  const [userId, setUserId] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  // Hydration protection
  useEffect(() => {
    setMounted(true);
    const id = getUserIdFromToken();
    setUserId(id);
  }, []);

  const handleSend = async (text: string) => {
    // Validate user is authenticated
    if (!userId) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Please log in to use the chat feature.',
        created_at: new Date().toISOString()
      }]);
      return;
    }

    if (!text || !text.trim()) {
      return;
    }

    // Add user message optimistically
    const userMsg = {
      role: 'user',
      content: text.trim(),
      created_at: new Date().toISOString()
    };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      // Call API with userId, message, and optional conversationId
      const response = await chatService.sendMessage(
        userId,
        text.trim(),
        convId ?? undefined
      );

      // Validate response structure
      if (!response || !response.content) {
        throw new Error('Invalid response from server');
      }

      // Update conversation ID if new conversation
      if (!convId && response.conversation_id) {
        setConvId(response.conversation_id);
      }

      // Add assistant message
      const assistantMsg = {
        role: response.role || 'assistant',
        content: response.content,
        created_at: response.created_at || new Date().toISOString()
      };
      setMessages(prev => [...prev, assistantMsg]);
    } catch (error: any) {
      console.error('Chat error:', error);

      // Remove optimistic user message on error
      setMessages(prev => prev.slice(0, -1));

      // Show error message
      const errorMessage = error.message || 'Sorry, I encountered an error. Please try again.';
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: errorMessage,
        created_at: new Date().toISOString()
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleNewConversation = () => {
    setMessages([]);
    setConvId(null);
  };

  // Prevent hydration mismatch
  if (!mounted) {
    return null;
  }

  return (
    <div className="flex flex-col h-[600px] bg-white rounded-2xl shadow-xl overflow-hidden border border-purple-100">
      <ChatHeader
        conversationId={convId}
        onNewConversation={handleNewConversation}
      />
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50/30">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full text-gray-400 text-sm">
            Start a conversation...
          </div>
        )}
        {messages.map((m, i) => (
          <ChatMessage key={i} message={m} />
        ))}
        {loading && <TypingIndicator />}
      </div>
      <ChatInput onSend={handleSend} disabled={loading} />
    </div>
  );
}
