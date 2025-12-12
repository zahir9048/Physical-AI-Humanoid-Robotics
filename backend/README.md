---
title: Physical AI Chatbot API
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# Physical AI & Humanoid Robotics Chatbot API

A FastAPI-based RAG (Retrieval-Augmented Generation) chatbot API for the Physical AI & Humanoid Robotics textbook. This backend provides intelligent question-answering capabilities using vector search and large language models.

## Features

- 🔍 **Vector Search**: Uses Qdrant for semantic document retrieval
- 🤖 **Multiple LLM Providers**: Supports OpenAI and Cohere
- 💾 **Chat History**: PostgreSQL-based conversation persistence
- 👍 **Feedback System**: Track and improve response quality
- 🚀 **FastAPI**: High-performance async API with automatic documentation

## API Endpoints

Once deployed, you can access:

- **Swagger UI**: `https://your-space-name.hf.space/docs`
- **Health Check**: `GET /api/health`
- **Chat**: `POST /api/chat`
- **Chat History**: `GET /api/conversations/{conversation_id}`
- **Feedback**: `POST /api/feedback`

## Configuration

This Space requires the following environment variables to be configured as **Secrets** in the Space settings:

### Required Secrets

| Variable | Description | Example |
|----------|-------------|---------|
| `EMBEDDING_PROVIDER` | Embedding model provider | `cohere` or `openai` |
| `LLM_PROVIDER` | Language model provider | `cohere` or `openai` |
| `QDRANT_URL` | Qdrant vector database URL | `https://your-cluster.qdrant.io` |
| `QDRANT_API_KEY` | Qdrant API key | `your-api-key` |
| `QDRANT_COLLECTION_NAME` | Collection name in Qdrant | `physical_ai_docs` |
| `NEON_DATABASE_URL` | PostgreSQL database URL | `postgresql://user:pass@host/db` |

### Provider-Specific Secrets

**If using Cohere:**
- `COHERE_API_KEY`: Your Cohere API key
- `COHERE_EMBEDDING_MODEL`: e.g., `embed-english-v3.0`
- `COHERE_MODEL`: e.g., `command-r-plus`

**If using OpenAI:**
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: e.g., `gpt-4-turbo-preview`

## Deployment Steps

1. **Create a new Space** on Hugging Face:
   - Go to https://huggingface.co/new-space
   - Choose **Docker** as the SDK
   - Select **CPU** (or upgrade to GPU if needed)

2. **Clone and push your code**:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   cd YOUR_SPACE_NAME
   
   # Copy backend files
   cp -r /path/to/your/backend/* .
   
   git add .
   git commit -m "Initial deployment"
   git push
   ```

3. **Configure Secrets**:
   - Go to your Space settings
   - Add all required environment variables as Secrets
   - Restart the Space

4. **Wait for build**:
   - The Space will build the Docker image
   - This may take 5-10 minutes on first deployment
   - Check the build logs for any errors

5. **Test the API**:
   - Visit `https://your-space-name.hf.space/docs`
   - Try the `/api/health` endpoint
   - Test a chat request

## Frontend Integration

Update your Docusaurus frontend to use the deployed backend:

```javascript
// In your frontend config
const API_BASE_URL = "https://your-space-name.hf.space/api";
```

## Performance Considerations

- **Cold Starts**: First request may be slow due to model loading
- **Rate Limits**: Free tier has usage limits
- **Upgrade Options**: Consider upgrading to CPU/GPU upgrade for better performance

## Troubleshooting

### Build Failures
- Check that all dependencies in `requirements.txt` are compatible
- Review build logs in the Space's "Logs" tab

### Runtime Errors
- Verify all Secrets are configured correctly
- Check that Qdrant and PostgreSQL are accessible
- Review application logs in the Space

### Slow Performance
- Consider upgrading to a paid tier
- Optimize model selection (smaller models = faster responses)
- Enable caching for frequently asked questions

## Local Development

To run locally:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with your variables
cp ENV_TEMPLATE.txt .env
# Edit .env with your actual values

# Run the server
python app.py
```

## License

MIT License - see LICENSE file for details

## Support

For issues or questions:
- Check the [documentation](https://your-docusaurus-site.com)
- Open an issue on GitHub
- Contact the maintainers
