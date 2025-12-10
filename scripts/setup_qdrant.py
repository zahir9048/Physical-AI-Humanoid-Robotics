#!/usr/bin/env python3
"""
Setup script for Qdrant vector database
"""
import os
import sys
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Add the backend/src directory to the path so we can import our modules
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_src_dir = os.path.join(script_dir, '..', 'backend', 'src')
sys.path.insert(0, backend_src_dir)

from core.config import settings

def setup_qdrant():
    print("Setting up Qdrant vector database...")

    # Initialize Qdrant client
    if settings.QDRANT_API_KEY:
        client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )
    else:
        client = QdrantClient(host="localhost", port=6333)

    try:
        # Check if collection already exists
        collections = client.get_collections()
        collection_names = [collection.name for collection in collections.collections]

        if settings.QDRANT_COLLECTION_NAME in collection_names:
            print(f"Collection '{settings.QDRANT_COLLECTION_NAME}' already exists")
        else:
            # Create collection for textbook content
            client.create_collection(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=1536,  # OpenAI embedding dimension
                    distance=models.Distance.COSINE
                )
            )
            print(f"Created collection '{settings.QDRANT_COLLECTION_NAME}'")

        # Verify collection exists and get info
        collection_info = client.get_collection(settings.QDRANT_COLLECTION_NAME)
        print(f"Collection '{settings.QDRANT_COLLECTION_NAME}' is ready")
        print(f"Points in collection: {collection_info.points_count}")

    except Exception as e:
        print(f"Error setting up Qdrant: {str(e)}")
        return False

    print("Qdrant setup completed successfully!")
    return True

if __name__ == "__main__":
    setup_qdrant()