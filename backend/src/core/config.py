from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "RAG Chatbot API"

    # Provider Settings
    EMBEDDING_PROVIDER: str = os.getenv("EMBEDDING_PROVIDER", "cohere")  # openai, cohere, ollama, local
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "cohere")  # openai, cohere, ollama

    # OpenAI Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL")

    # Cohere Settings
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY")
    COHERE_EMBEDDING_MODEL: str = os.getenv("COHERE_EMBEDDING_MODEL")
    COHERE_MODEL: str = os.getenv("COHERE_MODEL")

    # Qdrant Settings
    QDRANT_URL: str = os.getenv("QDRANT_URL")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME")

    # Database Settings
    DATABASE_URL: str = os.getenv("NEON_DATABASE_URL")

    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    MAX_QUERY_LENGTH: int = 1000
    MAX_RESPONSE_LENGTH: int = 2000
    CHUNK_SIZE: int = 1000
    OVERLAP_SIZE: int = 100

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_WINDOW: int = 60  # seconds

settings = Settings()