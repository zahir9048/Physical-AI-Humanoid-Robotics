import { Message } from '../services/types';

const CHAT_HISTORY_KEY = 'rag-chatbot-history';

export const saveChatHistory = (conversationId: string, messages: Message[]): void => {
  try {
    const history = getStoredHistory();
    history[conversationId] = {
      messages,
      timestamp: new Date().toISOString(),
    };
    localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(history));
  } catch (error) {
    console.error('Error saving chat history:', error);
  }
};

export const getChatHistory = (conversationId: string): Message[] | null => {
  try {
    const history = getStoredHistory();
    const conversation = history[conversationId];
    return conversation ? conversation.messages : null;
  } catch (error) {
    console.error('Error getting chat history:', error);
    return null;
  }
};

export const getAllStoredConversations = (): string[] => {
  try {
    const history = getStoredHistory();
    return Object.keys(history);
  } catch (error) {
    console.error('Error getting stored conversations:', error);
    return [];
  }
};

export const clearChatHistory = (conversationId: string): void => {
  try {
    const history = getStoredHistory();
    delete history[conversationId];
    localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(history));
  } catch (error) {
    console.error('Error clearing chat history:', error);
  }
};

export const clearAllChatHistory = (): void => {
  try {
    localStorage.removeItem(CHAT_HISTORY_KEY);
  } catch (error) {
    console.error('Error clearing all chat history:', error);
  }
};

interface StoredConversation {
  messages: Message[];
  timestamp: string;
}

interface StoredHistory {
  [conversationId: string]: StoredConversation;
}

const getStoredHistory = (): StoredHistory => {
  try {
    const stored = localStorage.getItem(CHAT_HISTORY_KEY);
    return stored ? JSON.parse(stored) : {};
  } catch (error) {
    console.error('Error parsing stored history:', error);
    return {};
  }
};