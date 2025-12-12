from typing import List, Optional
from qdrant_client import models
from src.core.database import qdrant_client
from src.core.config import settings
from src.services.embedding_service import embedding_service

class TextbookChunk:
    def __init__(self, id: str, content: str, title: str, chapter: str, section: str, url: str, source_file: str, position: int, metadata: dict = None, score: float = None):
        self.id = id
        self.content = content
        self.title = title
        self.chapter = chapter
        self.section = section
        self.url = url
        self.source_file = source_file
        self.position = position
        self.metadata = metadata or {}
        self.score = score  # Similarity score from vector search

class QdrantService:
    def __init__(self):
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self.client = qdrant_client

    async def search_chunks(self, query: str, top_k: int = 5) -> List[TextbookChunk]:
        """
        Search for relevant textbook chunks based on the query
        """
        # Create embedding for the query
        query_embedding = embedding_service.create_embedding_sync(query)

        # Search in Qdrant
        print(f"DEBUG: Searching Qdrant for query: '{query}' with top_k: {top_k}")
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )
        print(f"DEBUG: Qdrant search returned {len(search_results)} results")

        # Convert results to TextbookChunk objects
        chunks = []
        for result in search_results:
            payload = result.payload
            # Qdrant returns scores (higher is better for cosine similarity, typically 0-1 range)
            score = result.score if hasattr(result, 'score') else None
            chunk = TextbookChunk(
                id=str(result.id),
                content=payload.get("content", ""),
                title=payload.get("title", ""),
                chapter=payload.get("chapter", ""),
                section=payload.get("section", ""),
                url=payload.get("url", ""),
                source_file=payload.get("source_file", ""),
                position=payload.get("position", 0),
                metadata=payload.get("metadata", {}),
                score=score
            )
            chunks.append(chunk)

        return chunks

    async def add_chunk(self, chunk: TextbookChunk) -> bool:
        """
        Add a textbook chunk to the Qdrant collection
        """
        try:
            # Create embedding for the chunk content
            embedding = embedding_service.create_embedding_sync(chunk.content)

            print(f"DEBUG: Adding chunk {chunk.id} to Qdrant")
            # Upsert the chunk to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=chunk.id,
                        vector=embedding,
                        payload={
                            "content": chunk.content,
                            "title": chunk.title,
                            "chapter": chunk.chapter,
                            "section": chunk.section,
                            "url": chunk.url,
                            "source_file": chunk.source_file,
                            "position": chunk.position,
                            "metadata": chunk.metadata
                        }
                    )
                ]
            )
            print(f"DEBUG: Successfully added chunk {chunk.id}")
            return True
        except Exception as e:
            print(f"Error adding chunk to Qdrant: {str(e)}")
            return False

    async def batch_add_chunks(self, chunks: List[TextbookChunk]) -> bool:
        """
        Add multiple textbook chunks to the Qdrant collection
        """
        try:
            points = []
            for chunk in chunks:
                # Create embedding for the chunk content
                embedding = embedding_service.create_embedding_sync(chunk.content)

                point = models.PointStruct(
                    id=chunk.id,
                    vector=embedding,
                    payload={
                        "content": chunk.content,
                        "title": chunk.title,
                        "chapter": chunk.chapter,
                        "section": chunk.section,
                        "url": chunk.url,
                        "source_file": chunk.source_file,
                        "position": chunk.position,
                        "metadata": chunk.metadata
                    }
                )
                points.append(point)

            # Upsert all points to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return True
        except Exception as e:
            print(f"Error adding chunks to Qdrant: {str(e)}")
            return False