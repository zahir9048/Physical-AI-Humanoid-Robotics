# Deploying Backend to Hugging Face Spaces (Docker)

This guide provides step-by-step instructions for deploying your FastAPI backend to Hugging Face Spaces using the Docker SDK.

## Prerequisites

- A Hugging Face account (sign up at https://huggingface.co)
- Git installed on your machine
- Your backend code ready to deploy
- Access to required services:
  - Qdrant vector database (cloud or self-hosted)
  - PostgreSQL database (e.g., Neon, Supabase, or other provider)
  - API keys for your chosen LLM provider (Cohere or OpenAI)

## Step 1: Create a New Hugging Face Space

1. Go to https://huggingface.co/new-space
2. Fill in the details:
   - **Owner**: Your username or organization
   - **Space name**: Choose a descriptive name (e.g., `physical-ai-chatbot-api`)
   - **License**: MIT (or your preferred license)
   - **SDK**: Select **Docker**
   - **Space hardware**: Start with **CPU basic** (free tier)
   - **Visibility**: Public or Private (your choice)
3. Click **Create Space**

## Step 2: Prepare Your Backend Code

Your backend already has the necessary files:
- ✅ `app.py` - Entry point for Hugging Face Spaces
- ✅ `Dockerfile` - Docker configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `README.md` - Space documentation
- ✅ `ENV_TEMPLATE.txt` - Environment variables reference

## Step 3: Clone Your Space Repository

```bash
# Clone the Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME
```

## Step 4: Copy Backend Files

```bash
# Copy all backend files to the Space directory
# Adjust the path to your backend directory
cp -r /path/to/physical-ai-textbook/backend/* .

# Or on Windows:
# xcopy /E /I C:\path\to\physical-ai-textbook\backend\* .
```

**Files to include:**
- `app.py`
- `Dockerfile`
- `requirements.txt`
- `README.md`
- `src/` directory (all source code)
- `alembic/` directory (database migrations)
- `alembic.ini`

**Files to exclude:**
- `.env` (never commit secrets!)
- `venv/` or `__pycache__/` (virtual environments and cache)
- `tests/` (optional, but can include if you want)

## Step 5: Configure Environment Secrets

1. Go to your Space on Hugging Face: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`
2. Click on **Settings** (gear icon)
3. Scroll to **Repository secrets**
4. Add the following secrets (click **New secret** for each):

### Required Secrets

| Secret Name | Example Value | Description |
|-------------|---------------|-------------|
| `EMBEDDING_PROVIDER` | `cohere` | Embedding model provider |
| `LLM_PROVIDER` | `cohere` | Language model provider |
| `QDRANT_URL` | `https://xyz.qdrant.io` | Your Qdrant instance URL |
| `QDRANT_API_KEY` | `your-qdrant-key` | Qdrant API key |
| `QDRANT_COLLECTION_NAME` | `physical_ai_docs` | Collection name |
| `NEON_DATABASE_URL` | `postgresql://user:pass@host/db` | PostgreSQL connection string |

### Provider-Specific Secrets

**If using Cohere:**
- `COHERE_API_KEY`: Your Cohere API key
- `COHERE_EMBEDDING_MODEL`: `embed-english-v3.0`
- `COHERE_MODEL`: `command-r-plus`

**If using OpenAI:**
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: `gpt-4-turbo-preview`

> **Note**: Refer to `ENV_TEMPLATE.txt` for the complete list of variables.

## Step 6: Push Your Code

```bash
# Add all files
git add .

# Commit
git commit -m "Initial deployment of Physical AI Chatbot API"

# Push to Hugging Face
git push
```

## Step 7: Monitor the Build

1. Go to your Space page
2. The build will start automatically
3. Click on **Logs** to see the build progress
4. Wait for the build to complete (5-10 minutes on first deployment)
5. Look for "Running on http://0.0.0.0:7860" in the logs

## Step 8: Test Your Deployment

Once the build is complete:

1. **Access the API documentation**:
   - Visit: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/docs`
   - You should see the Swagger UI with all endpoints

2. **Test the health endpoint**:
   ```bash
   curl https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/api/health
   ```
   Expected response: `{"status": "healthy"}`

3. **Test a chat request**:
   - Use the Swagger UI `/docs` page
   - Try the `POST /api/chat` endpoint
   - Send a test question about physical AI

## Step 9: Update Your Frontend

Update your Docusaurus frontend to use the deployed backend:

1. Open your frontend configuration file (likely in `src/` or `frontend/`)
2. Update the API base URL:

```javascript
// Before
const API_BASE_URL = "http://localhost:8000/api";

// After
const API_BASE_URL = "https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/api";
```

3. Test the integration by opening your Docusaurus site and trying the chatbot

## Troubleshooting

### Build Fails

**Problem**: Docker build fails with dependency errors

**Solution**:
- Check `requirements.txt` for incompatible versions
- Review build logs for specific error messages
- Try removing version pins for problematic packages

### Space Shows "Runtime Error"

**Problem**: Space builds but shows runtime error

**Solution**:
- Verify all Secrets are configured correctly (check for typos)
- Ensure Qdrant and PostgreSQL are accessible from Hugging Face servers
- Check application logs in the Space's Logs tab
- Verify your Qdrant collection exists and has data

### Slow Response Times

**Problem**: API responds very slowly

**Solution**:
- Upgrade to CPU/GPU upgrade tier (paid)
- Use smaller/faster models
- Optimize your Qdrant queries
- Consider caching frequently asked questions

### CORS Errors from Frontend

**Problem**: Frontend can't connect due to CORS

**Solution**:
- Check that `allow_origins=["*"]` is set in `src/api/main.py`
- Or update to specific domain: `allow_origins=["https://your-docusaurus-site.com"]`

### Database Connection Fails

**Problem**: Can't connect to PostgreSQL

**Solution**:
- Verify `NEON_DATABASE_URL` is correct
- Check that your database allows connections from Hugging Face IPs
- Run database migrations if needed

## Upgrading Your Space

### To Better Hardware

1. Go to Space Settings
2. Under **Space hardware**, select a paid tier:
   - **CPU upgrade** ($0.03/hour) - Better for most use cases
   - **GPU** (various tiers) - If using local embeddings/models

### To Update Code

```bash
# Make your changes locally
# Then commit and push
git add .
git commit -m "Update: description of changes"
git push
```

The Space will automatically rebuild and redeploy.

## Cost Considerations

- **Free tier**: Limited to 2 vCPU, 16GB RAM, may have cold starts
- **CPU upgrade**: $0.03/hour (~$22/month if always running)
- **GPU tiers**: More expensive, only needed for local model inference

## Alternative: Using Docker Compose Locally

If you prefer to test locally before deploying:

```bash
cd backend
docker-compose up --build
```

This will start the backend on `http://localhost:8000`.

## Next Steps

1. ✅ Deploy backend to Hugging Face Spaces
2. ✅ Configure all environment secrets
3. ✅ Test API endpoints
4. ✅ Update frontend to use deployed backend
5. 📝 Monitor usage and performance
6. 📝 Set up monitoring/alerting (optional)
7. 📝 Configure custom domain (optional)

## Additional Resources

- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Docker SDK Guide](https://huggingface.co/docs/hub/spaces-sdks-docker)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)

## Support

If you encounter issues:
1. Check the Space logs for error messages
2. Review this troubleshooting guide
3. Consult the Hugging Face community forums
4. Open an issue on your project's GitHub repository
