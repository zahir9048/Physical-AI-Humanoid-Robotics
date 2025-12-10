// Types for the RAG Chatbot frontend

export interface ChatRequest {
  query: string;
  conversation_id?: string;
  selected_text?: string;
  page_url?: string;
}

export interface Citation {
  title: string;
  url: string;
  chapter: string;
  section: string;
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  citations: Citation[];
  sources: string[];
}

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  source_chunks?: string[];
}

export interface ConversationHistory {
  conversation_id: string;
  messages: Message[];
}

export interface FeedbackRequest {
  message_id: string;
  rating: -1 | 0 | 1; // dislike, neutral, like
  comment?: string;
}

export interface FeedbackResponse {
  success: boolean;
  message: string;
}

export interface HealthResponse {
  status: 'healthy' | 'degraded' | 'unavailable';
  timestamp: string;
  details: {
    db_status?: string;
    qdrant_status?: string;
    [key: string]: any;
  };
}