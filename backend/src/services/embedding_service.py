import openai
import cohere
import httpx
from typing import List
from src.core.config import settings
# from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    def __init__(self):
        self.provider = settings.EMBEDDING_PROVIDER

        if self.provider == "openai":
            openai.api_key = settings.OPENAI_API_KEY
        elif self.provider == "cohere":
            self.cohere_client = cohere.Client(api_key=settings.COHERE_API_KEY)
        elif self.provider == "local":
            # For local sentence transformer models
            # For local sentence transformer models
            from sentence_transformers import SentenceTransformer
            self.local_model = SentenceTransformer('all-MiniLM-L6-v2')
        # For ollama, no initialization needed

    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for a list of texts using the configured provider
        """
        try:
            if self.provider == "openai":
                response = await openai.embeddings.acreate(
                    input=texts,
                    model=settings.EMBEDDING_MODEL
                )
                embeddings = [data.embedding for data in response.data]
            elif self.provider == "cohere":
                response = self.cohere_client.embed(
                    texts=texts,
                    model=settings.COHERE_EMBEDDING_MODEL,
                    input_type="search_document"
                )
                embeddings = response.embeddings
            elif self.provider == "ollama":
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{settings.OLLAMA_URL}/api/embeddings",
                        json={
                            "model": settings.OLLAMA_EMBEDDING_MODEL,
                            "prompt": texts[0] if len(texts) == 1 else " ".join(texts)
                        },
                        timeout=30.0
                    )
                    result = response.json()
                    # Ollama returns single embedding, repeat for all texts if needed
                    embedding = result["embedding"]
                    embeddings = [embedding for _ in texts]
            elif self.provider == "local":
                # Use local sentence transformer
                embeddings = self.local_model.encode(texts).tolist()
            else:
                raise ValueError(f"Unsupported embedding provider: {self.provider}")

            return embeddings
        except Exception as e:
            raise Exception(f"Error creating embeddings: {str(e)}")

    def create_embedding_sync(self, text: str) -> List[float]:
        """
        Create embedding for a single text synchronously
        """
        try:
            if self.provider == "openai":
                response = openai.embeddings.create(
                    input=[text],
                    model=settings.EMBEDDING_MODEL
                )
                return response.data[0].embedding
            elif self.provider == "cohere":
                response = self.cohere_client.embed(
                    texts=[text],
                    model=settings.COHERE_EMBEDDING_MODEL,
                    input_type="search_document"
                )
                return response.embeddings[0]
            elif self.provider == "local":
                embedding = self.local_model.encode([text])[0].tolist()
                return embedding
            else:
                # For ollama, we'd need to make a sync call
                import requests
                response = requests.post(
                    f"{settings.OLLAMA_URL}/api/embeddings",
                    json={
                        "model": settings.OLLAMA_EMBEDDING_MODEL,
                        "prompt": text
                    }
                )
                result = response.json()
                return result["embedding"]
        except Exception as e:
            raise Exception(f"Error creating embedding: {str(e)}")

# Global instance
embedding_service = EmbeddingService()