import axios, { AxiosResponse } from 'axios';
import {
  ChatRequest,
  ChatResponse,
  ConversationHistory,
  FeedbackRequest,
  FeedbackResponse,
  HealthResponse
} from './types';

const API_BASE_URL = 'http://localhost:8000/api';

class ChatAPI {
  private api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  public setBaseUrl(url: string) {
    this.api.defaults.baseURL = url;
  }

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
}

export default new ChatAPI();
