import axios, { AxiosResponse } from 'axios';
import {
  ChatRequest,
  ChatResponse,
  ConversationHistory,
  FeedbackRequest,
  FeedbackResponse,
  HealthResponse
} from './types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

class ChatAPI {
  private api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  async chatQuery(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response: AxiosResponse<ChatResponse> = await this.api.post('/chat/query', request);
      return response.data;
    } catch (error) {
      console.error('Error in chat query:', error);
      throw error;
    }
  }

  async getConversationHistory(conversationId: string): Promise<ConversationHistory> {
    try {
      const response: AxiosResponse<ConversationHistory> = await this.api.get(`/chat/history/${conversationId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting conversation history:', error);
      throw error;
    }
  }

  async submitFeedback(request: FeedbackRequest): Promise<FeedbackResponse> {
    try {
      const response: AxiosResponse<FeedbackResponse> = await this.api.post('/feedback', request);
      return response.data;
    } catch (error) {
      console.error('Error submitting feedback:', error);
      throw error;
    }
  }

  async healthCheck(): Promise<HealthResponse> {
    try {
      const response: AxiosResponse<HealthResponse> = await this.api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error in health check:', error);
      throw error;
    }
  }

  // Method to establish a streaming connection
  streamChat(request: ChatRequest, onMessage: (data: string) => void, onError?: (error: any) => void) {
    const eventSource = new EventSource(`${API_BASE_URL.replace('/api', '')}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    eventSource.onmessage = (event) => {
      onMessage(event.data);
    };

    eventSource.onerror = (error) => {
      if (onError) {
        onError(error);
      }
      eventSource.close();
    };

    return eventSource;
  }
}

export default new ChatAPI();