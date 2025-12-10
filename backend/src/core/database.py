from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from qdrant_client import QdrantClient
from src.core.config import settings


# Postgres Database setup
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Qdrant client setup
if settings.QDRANT_API_KEY:
    qdrant_client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY
    )
else:
    qdrant_client = QdrantClient(host="localhost", port=6333)

def get_db():
    db = SessionLocal()
    print(db)
    try:
        yield db
    finally:
        db.close()

def get_qdrant_client():
    return qdrant_client

# Initialize Qdrant collection if it doesn't exist
def init_qdrant_collection():
    try:
        # Check if collection exists
        qdrant_client.get_collection(settings.QDRANT_COLLECTION_NAME)
        print(f"Qdrant collection '{settings.QDRANT_COLLECTION_NAME}' already exists")
    except:
        # Create collection if it doesn't exist
        qdrant_client.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config={
                "size": 1024,  # Cohere embedding dimension (embed-multilingual-v3.0)
                "distance": "Cosine"
            }
        )
        print(f"Created Qdrant collection '{settings.QDRANT_COLLECTION_NAME}'")

# Initialize Qdrant collection on startup
