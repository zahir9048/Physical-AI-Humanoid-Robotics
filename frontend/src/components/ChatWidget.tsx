import React, { useState, useEffect, useRef } from 'react';
import { Message, ChatRequest } from '../services/types';
import ChatAPI from '../services/ChatAPI';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { MessageCircle, X, Bot, User } from 'lucide-react';

interface ChatWidgetProps {
  initialSelectedText?: string;
  initialPageUrl?: string;
}

const ChatWidget: React.FC<ChatWidgetProps> = ({ initialSelectedText = '', initialPageUrl = '' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string>('');
  const [selectedText, setSelectedText] = useState(initialSelectedText);
  const [pageUrl, setPageUrl] = useState(initialPageUrl);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Scroll to bottom of messages when they change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (query: string) => {
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
      const chatRequest: ChatRequest = {
        query,
        conversation_id: conversationId || undefined,
        selected_text: selectedText || undefined,
        page_url: pageUrl || undefined,
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

      setMessages(prev => [...prev, assistantMessage]);

      // Clear selected text after the query is processed
      setSelectedText('');
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the chat
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    setConversationId('');
  };

  const handleLoadHistory = async () => {
    if (!conversationId) return;

    try {
      const history = await ChatAPI.getConversationHistory(conversationId);
      if (history) {
        // Convert the API response to our internal message format
        const convertedMessages = history.messages.map(msg => ({
          id: msg.id,
          role: msg.role,
          content: msg.content,
          timestamp: msg.timestamp,
          source_chunks: msg.source_chunks
        }));
        setMessages(convertedMessages);
      }
    } catch (error) {
      console.error('Error loading conversation history:', error);
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      {/* Floating chat button */}
      {!isOpen && (
        <button
          onClick={toggleChat}
          className="fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 transition-colors z-50"
          aria-label="Open chat"
        >
          <MessageCircle size={24} />
        </button>
      )}

      {/* Chat widget */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-full max-w-md h-[70vh] flex flex-col bg-white rounded-lg shadow-xl border border-gray-200 z-50">
          {/* Header */}
          <div className="bg-blue-600 text-white p-4 rounded-t-lg flex justify-between items-center">
            <h2 className="font-semibold">Physical AI Assistant</h2>
            <div className="flex space-x-2">
              <button
                onClick={handleLoadHistory}
                className="text-white hover:bg-blue-700 p-1 rounded text-sm"
                title="Load conversation history"
                disabled={!conversationId}
              >
                Load
              </button>
              <button
                onClick={handleClearChat}
                className="text-white hover:bg-blue-700 p-1 rounded text-sm"
                title="Clear chat"
              >
                Clear
              </button>
              <button
                onClick={toggleChat}
                className="text-white hover:bg-blue-700 p-1 rounded"
                aria-label="Close chat"
              >
                <X size={20} />
              </button>
            </div>
          </div>

          {/* Messages container */}
          <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-gray-500">
                <Bot className="mb-2" size={32} />
                <p>Ask me anything about the Physical AI & Humanoid Robotics textbook!</p>
                {selectedText && (
                  <p className="mt-2 text-sm text-blue-600">
                    Selected text: "{selectedText.substring(0, 50)}..."
                  </p>
                )}
              </div>
            ) : (
              <>
                {messages.map((message) => (
                  <ChatMessage
                    key={message.id}
                    message={message}
                    avatar={message.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                  />
                ))}
                {isLoading && (
                  <div className="flex items-start mb-4">
                    <div className="bg-blue-100 rounded-full p-2 mr-3">
                      <Bot size={16} className="text-blue-600" />
                    </div>
                    <div className="bg-gray-200 rounded-lg p-3">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-100"></div>
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-200"></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          {/* Input area */}
          <div className="p-4 border-t border-gray-200 bg-white">
            <ChatInput
              onSendMessage={handleSendMessage}
              disabled={isLoading}
              placeholder="Ask about the textbook content..."
            />
          </div>
        </div>
      )}
    </>
  );
};

export default ChatWidget;