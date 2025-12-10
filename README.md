
# RAG Chatbot for Physical AI & Humanoid Robotics Textbook

This project implements a Retrieval-Augmented Generation (RAG) chatbot that allows students to ask questions about the Physical AI & Humanoid Robotics textbook and receive intelligent, contextually relevant responses.

## Architecture

The application consists of two main components:

1. **Backend**: FastAPI application that handles the RAG logic, conversation management, and API endpoints
2. **Frontend**: React-based chat widget that can be embedded in the Docusaurus textbook site

## Features

- **Smart Q&A**: Ask questions about textbook content and receive accurate responses
- **Text Selection**: Select text on any page and ask targeted questions about it
- **Citations**: Responses include citations to specific chapters/sections
- **Conversation History**: Maintain context across multiple turns
- **Feedback System**: Rate responses to improve the system
- **Streaming Responses**: Real-time response streaming for better UX

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- OpenAI API
- Qdrant Vector Database
- PostgreSQL (Neon Serverless)
- Pydantic
- SQLAlchemy

### Frontend
- React 18+
- TypeScript
- Tailwind CSS
- Axios
- React Markdown

## Setup

### Prerequisites

1. Python 3.11+
2. Node.js 18+
3. OpenAI API key
4. Qdrant Cloud account
5. Neon Serverless Postgres account

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory with your configuration:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_cluster_url
   QDRANT_API_KEY=your_qdrant_api_key
   NEON_DATABASE_URL=your_neon_database_url
   QDRANT_COLLECTION_NAME=physical-ai-textbook
   ```

5. Set up the databases:
   ```bash
   python scripts/setup_postgres.py
   python scripts/setup_qdrant.py
   ```

6. Ingest the textbook content:
   ```bash
   python scripts/ingest_documents.py
   ```

7. Start the backend server:
   ```bash
   uvicorn src.api.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the frontend directory:
   ```env
   REACT_APP_API_BASE_URL=http://localhost:8000/api
   ```

4. Start the development server:
   ```bash
   npm start
   ```

## API Endpoints

- `POST /api/chat/query` - Submit a query and get response
- `POST /api/chat/stream` - Streamed response endpoint
- `GET /api/chat/history/{conversation_id}` - Get conversation history
- `POST /api/feedback` - Submit feedback on a response
- `GET /api/health` - Health check

## Docusaurus Integration

To integrate the chatbot widget with your Docusaurus site:

1. Build the frontend:
   ```bash
   npm run build
   ```

2. The chatbot widget will be available as a React component that can be embedded in your Docusaurus pages.

## Testing

### Backend Tests
```bash
cd backend
pytest tests/unit/ -v
pytest tests/integration/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

### Backend
- Containerize with Docker
- Deploy to Render, Railway, or similar platform
- Set environment variables in deployment platform

### Frontend
- Build as part of Docusaurus static site
- Deploy to GitHub Pages or similar static hosting

## Troubleshooting

### Common Issues
1. **API Rate Limits**: Implement exponential backoff; check OpenAI quota
2. **Vector Search Issues**: Verify document ingestion completed successfully
3. **Database Connection**: Check environment variables and connection strings
4. **CORS Errors**: Ensure backend allows requests from frontend origin

## Development

The project follows a feature-driven development approach with the following structure:
- `specs/002-rag-chatbot/` - Feature specifications, plan, and tasks
- `backend/` - Backend source code
- `frontend/` - Frontend source code
- `scripts/` - Utility scripts for setup and data ingestion
