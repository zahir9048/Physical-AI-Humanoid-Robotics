---
id: 0003
title: RAG Chatbot Planning
stage: plan
date: 2025-12-09
surface: agent
model: Claude Sonnet 4.5
feature: rag-chatbot
branch: 002-rag-chatbot
user: zahir
command: /sp.plan
labels: ["planning", "architecture", "specification", "rag", "chatbot"]
links:
  spec: specs/002-rag-chatbot/spec.md
  plan: specs/002-rag-chatbot/plan.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-rag-chatbot/plan.md
 - specs/002-rag-chatbot/research.md
 - specs/002-rag-chatbot/data-model.md
 - specs/002-rag-chatbot/quickstart.md
 - specs/002-rag-chatbot/contracts/chat-api.yaml
 - .specify/memory/constitution.md
tests:
 - constitution check passed
 - api contracts defined
 - data models specified
---

## Prompt

We are building this RAG chatbot system with the following technical stack and architecture:

BACKEND STACK:
- FastAPI (latest version) for REST API
- Python 3.11+
- OpenAI Agents SDK (latest) for conversational AI
- OpenAI embeddings (text-embedding-3-small or ada-002)
- Qdrant Cloud Free Tier for vector database
- Neon Serverless Postgres for relational data
- Pydantic for data validation
- python-dotenv for environment management

FRONTEND STACK:
- React 18+ for chatbot widget
- TypeScript for type safety
- Docusaurus plugin/custom component for integration
- Tailwind CSS for styling (if not using Docusaurus styles)
- Web Speech API for voice input
- EventSource or WebSocket for streaming responses

ARCHITECTURE:

1. Document Processing Pipeline (One-time setup):
   - Python script to parse all MDX/MD files from Docusaurus docs/
   - Chunk by sections (headers) with 500-1000 token chunks
   - Chunk overlap: 100 tokens
   - Generate embeddings using OpenAI
   - Upload to Qdrant with metadata (chapter, section, url, title)

2. Backend API Structure (FastAPI):
   - /api/chat/query - Main chat endpoint (POST)
   - /api/chat/stream - Streaming response endpoint (SSE)
   - /api/chat/history - Get conversation history (GET)
   - /api/feedback - Submit feedback (POST)
   - /api/health - Health check (GET)

3. RAG Flow:
   - Receive query + optional selected text
   - Generate query embedding
   - Query Qdrant for top 5-10 relevant chunks
   - Assemble context: selected text (if any) + retrieved chunks
   - Create system prompt with domain knowledge
   - Use OpenAI Agents SDK to generate response
   - Stream response back to frontend
   - Save conversation to Postgres

4. Frontend Widget Structure:
   - ChatWidget.tsx - Main container component
   - ChatMessage.tsx - Individual message component
   - ChatInput.tsx - Input field with voice support
   - TextSelectionHandler.tsx - Handles text selection on pages
   - ChatAPI.ts - API client for backend
   - Embedded via Docusaurus custom component or plugin

5. Text Selection Feature:
   - Add event listener on all article/markdown content
   - On mouseup, check if text is selected
   - Show floating "Ask AI" button near selection
   - Pass selected text + page URL to chatbot
   - Automatically open chatbot with pre-filled context

DEPLOYMENT:

1. Backend:
   - Dockerize FastAPI application
   - Deploy to Render or Railway (free tier)
   - Environment variables: OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, NEON_DATABASE_URL
   - Enable CORS for Docusaurus domain

2. Frontend:
   - Build as part of Docusaurus build process
   - Chatbot widget bundled with Docusaurus
   - Deploy together to GitHub Pages

3. Databases:
   - Qdrant: Create collection via Python SDK
   - Neon: Set up Postgres with tables for conversations, messages, feedback
   - Run initial data ingestion script to populate Qdrant

CONFIGURATION:
- Use environment variables for all API keys
- Configurable parameters: chunk_size, top_k, temperature
- Separate config for development and production
- CORS whitelist for allowed origins

SPECIFIC IMPLEMENTATION NOTES:
1. Use OpenAI Agents SDK's streaming API for real-time responses
2. Implement exponential backoff for OpenAI rate limits
3. Cache common queries to reduce OpenAI API calls
4. Use Qdrant's filtering for chapter-specific searches
5. Implement proper error handling with user-friendly messages
6. Add loading states and skeleton loaders in UI
7. Test with sample queries before full deployment

## Response snapshot

Successfully completed the implementation planning for the RAG chatbot system. The following artifacts were created:

1. **Implementation Plan** (plan.md): Comprehensive architecture plan with technical context, constitution check, and project structure
2. **Research** (research.md): Technical decisions and best practices for key implementation choices
3. **Data Model** (data-model.md): Detailed entity relationships and database schema
4. **Quickstart Guide** (quickstart.md): Setup and deployment instructions
5. **API Contracts** (contracts/chat-api.yaml): OpenAPI specification for the backend API

The plan includes:
- Web application architecture with separate backend (FastAPI) and frontend (React) components
- Detailed directory structure for both backend and frontend
- Data models for conversations, messages, feedback, and textbook chunks
- API contract with full OpenAPI specification
- Security and performance considerations
- Deployment strategy using free tiers of Qdrant and Neon Postgres

The agent context was updated with the new technologies, and all constitution checks passed.

## Outcome

- ✅ Impact: Comprehensive implementation plan created with all necessary artifacts
- 🧪 Tests: Constitution checks passed, API contracts defined
- 📁 Files: Multiple planning artifacts created (plan, research, data model, contracts)
- 🔁 Next prompts: Ready for task generation with `/sp.tasks`
- 🧠 Reflection: Plan addresses all technical requirements while maintaining compliance with project constitution

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All planning artifacts created successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate tasks with /sp.tasks