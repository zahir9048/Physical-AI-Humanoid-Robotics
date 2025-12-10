# Quickstart: RAG Chatbot for Physical AI & Humanoid Robotics Textbook

## Prerequisites
- Python 3.11+
- Node.js 18+ (for Docusaurus)
- OpenAI API key
- Qdrant Cloud account
- Neon Serverless Postgres account

## Setup

### 1. Clone and Install Dependencies
```bash
# Navigate to the project root
cd /path/to/physical-ai-textbook

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies (if separate)
cd ../frontend
npm install
```

### 2. Environment Configuration
Create `.env` file in the backend directory:
```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
NEON_DATABASE_URL=your_neon_database_url
QDRANT_COLLECTION_NAME=physical-ai-textbook
```

### 3. Database Setup
```bash
# Run the setup scripts
python scripts/setup_postgres.py
python scripts/setup_qdrant.py
```

### 4. Document Ingestion
```bash
# Ingest textbook content into vector database
python scripts/ingest_documents.py
```

### 5. Backend Service
```bash
# Start the backend service
cd backend
uvicorn src.api.main:app --reload --port 8000
```

### 6. Frontend Integration
```bash
# Build the chatbot component and integrate with Docusaurus
cd frontend
npm run build

# The chatbot widget will be integrated into the Docusaurus site
cd ../ # back to project root
npm run start # to start the Docusaurus site with chatbot
```

## API Endpoints

### Chat Endpoints
- `POST /api/chat/query` - Submit a query and get response
- `GET /api/chat/stream` - Streamed response endpoint
- `GET /api/chat/history/{conversation_id}` - Get conversation history
- `POST /api/feedback` - Submit feedback on a response
- `GET /api/health` - Health check

### Example Request
```bash
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain ROS 2 nodes",
    "conversation_id": "uuid-here",
    "selected_text": "A ROS 2 node is..."
  }'
```

## Frontend Integration

The chatbot widget is designed to be embedded in Docusaurus pages. It will:
1. Appear as a floating button in the bottom-right corner
2. Show a chat interface when clicked
3. Handle text selection with a floating "Ask AI" button
4. Maintain conversation history in browser session

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
- Deploy to Render or Railway (free tier)
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