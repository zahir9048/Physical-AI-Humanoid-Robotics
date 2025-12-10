import { useState, useEffect, useCallback } from 'react';
import { Message } from '../services/types';
import ChatAPI from '../services/ChatAPI';
import { getChatHistory, saveChatHistory, clearChatHistory } from '../utils/storage';

const useChat = (initialConversationId?: string) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(initialConversationId || null);

  // Load conversation history when conversationId changes
  useEffect(() => {
    if (conversationId) {
      const storedMessages = getChatHistory(conversationId);
      if (storedMessages) {
        setMessages(storedMessages);
      }
    } else {
      setMessages([]);
    }
  }, [conversationId]);

  const sendMessage = useCallback(async (query: string, selectedText?: string, pageUrl?: string) => {
    if (!query.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: query,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Prepare the chat request
      const chatRequest = {
        query,
        conversation_id: conversationId || undefined,
        selected_text: selectedText,
        page_url: pageUrl,
      };

      // Send the request to the backend
      const response = await ChatAPI.chatQuery(chatRequest);

      // Update conversation ID if it's the first message
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant message to the chat
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
        source_chunks: response.sources,
      };

      const newMessages = [...messages, userMessage, assistantMessage];
      setMessages(newMessages);

      // Save to local storage
      if (conversationId) {
        saveChatHistory(conversationId, newMessages);
      } else if (response.conversation_id) {
        saveChatHistory(response.conversation_id, newMessages);
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the chat
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date().toISOString(),
      };

      const newMessages = [...messages, userMessage, errorMessage];
      setMessages(newMessages);

      // Save to local storage
      if (conversationId) {
        saveChatHistory(conversationId, newMessages);
      }
    } finally {
      setIsLoading(false);
    }
  }, [conversationId, isLoading, messages]);

  const clearChat = useCallback(() => {
    setMessages([]);
    if (conversationId) {
      clearChatHistory(conversationId);
    }
  }, [conversationId]);

  return {
    messages,
    isLoading,
    conversationId,
    sendMessage,
    clearChat,
  };
};

export default useChat;