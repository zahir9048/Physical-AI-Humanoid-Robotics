from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.api.routes import chat, history, feedback, health

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="RAG Chatbot API for Physical AI & Humanoid Robotics Textbook"
)

# CORS middleware for Docusaurus integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Docusaurus domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(chat.router, prefix=settings.API_V1_STR, tags=["chat"])
app.include_router(history.router, prefix=settings.API_V1_STR, tags=["history"])
app.include_router(feedback.router, prefix=settings.API_V1_STR, tags=["feedback"])
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["health"])

@app.on_event("startup")
async def startup_event():
    from src.core.database import init_qdrant_collection
    try:
        init_qdrant_collection()
    except Exception as e:
        print(f"Warning: Failed to initialize Qdrant collection: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)