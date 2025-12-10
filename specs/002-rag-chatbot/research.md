# Research: RAG Chatbot for Physical AI & Humanoid Robotics Textbook

## Overview
This research document addresses technical decisions and best practices for implementing the RAG chatbot system based on the provided architecture and requirements.

## Decision: OpenAI Embedding Model Selection
**Rationale**: Choosing between text-embedding-3-small and text-ada-002 for textbook content indexing.
**Decision**: Use text-embedding-3-small due to better performance on technical content and lower cost per token compared to ada-002. The 3-small model has 1536 dimensions which provides good balance between accuracy and cost.
**Alternatives considered**:
- text-embedding-ada-002 (1536 dimensions, older model)
- text-embedding-3-large (3072 dimensions, higher cost)

## Decision: Textbook Content Chunking Strategy
**Rationale**: How to split textbook content for optimal retrieval in the RAG system.
**Decision**: Chunk by document structure (sections/chapters) with 500-1000 token chunks and 100-token overlap as specified in clarifications. This approach maintains semantic coherence while allowing for cross-section context retrieval.
**Alternatives considered**:
- Fixed-length token chunks (may split concepts)
- Sentence-level chunks (too granular for textbook content)
- Full document chunks (too broad for precise retrieval)

## Decision: Frontend Integration Approach
**Rationale**: How to embed the chatbot widget into the Docusaurus site.
**Decision**: Custom React component embedded in pages rather than a Docusaurus plugin. This provides more flexibility for UI/UX and easier maintenance.
**Alternatives considered**:
- Docusaurus plugin (more complex build integration)
- Standalone widget loaded via script (less integrated feel)

## Decision: Text Selection Implementation
**Rationale**: How to implement the text selection feature for contextual Q&A.
**Decision**: JavaScript event listeners on MDX content elements that show a floating "Ask AI" button when text is selected. This provides a non-intrusive user experience.
**Alternatives considered**:
- Global document listeners (potential conflicts)
- CSS-only approach (limited functionality)

## Decision: Streaming Response Implementation
**Rationale**: How to provide real-time responses to users.
**Decision**: Server-Sent Events (SSE) via FastAPI for streaming responses from OpenAI to frontend. This provides a clean, efficient streaming mechanism with good browser support.
**Alternatives considered**:
- WebSocket connections (more complex setup)
- Chunked HTTP responses (less standardized)

## Decision: Rate Limiting Strategy
**Rationale**: How to handle API rate limits and prevent abuse.
**Decision**: Implement rate limiting with HTTP 429 status codes and JSON error responses as specified in clarifications. Use exponential backoff for OpenAI API calls.
**Alternatives considered**:
- No rate limiting (security risk)
- Soft rate limiting (reduced performance)

## Decision: Caching Strategy
**Rationale**: How to reduce OpenAI API calls and improve response times.
**Decision**: Implement caching for common queries using a simple in-memory cache on the backend. Cache responses for frequently asked questions to reduce API costs.
**Alternatives considered**:
- No caching (higher API costs)
- Distributed cache (unnecessary complexity for initial implementation)

## Decision: Database Schema Design
**Rationale**: How to structure data in Neon Postgres for conversations and feedback.
**Decision**: Three main tables - conversations (id, created_at), messages (id, conversation_id, role, content, timestamp), feedback (id, message_id, rating, comment). This supports anonymous sessions with temporary data.
**Alternatives considered**:
- Single table approach (less normalized)
- No feedback table (loses valuable user input)

## Best Practices: Error Handling
**Rationale**: How to handle various error conditions gracefully.
**Decision**: Implement comprehensive error handling with user-friendly messages, proper logging, and graceful degradation. Use HTTP status codes appropriately (429 for rate limits, 500+ for server errors).
**Alternatives considered**:
- Generic error messages (poor UX)
- No error handling (system instability)

## Best Practices: Security
**Rationale**: How to ensure secure handling of API keys and user data.
**Decision**: Store API keys in environment variables, validate all inputs, implement proper CORS policies, and maintain anonymous sessions without storing PII.
**Alternatives considered**:
- Hardcoded API keys (security risk)
- Storing user data without consent (privacy issues)