from typing import List, Optional
from src.services.qdrant_service import QdrantService, TextbookChunk
from src.core.config import settings

class RetrievalService:
    def __init__(self):
        self.qdrant_service = QdrantService()

    async def retrieve_relevant_chunks(
        self,
        query: str,
        selected_text: Optional[str] = None
    ) -> List[TextbookChunk]:
        """
        Retrieve relevant textbook chunks based on the query and optionally selected text
        Filters out low-relevance results based on similarity score
        """
        # If selected text is provided, use it as additional context
        search_text = query
        if selected_text:
            search_text = f"{query} Context: {selected_text}"

        # Retrieve relevant chunks from Qdrant
        relevant_chunks = await self.qdrant_service.search_chunks(
            query=search_text,
            top_k=5  # Get top 5 most relevant chunks
        )

        # Filter by similarity threshold (cosine similarity, typically 0-1, higher is better)
        # Only keep chunks with score > 0.3 (adjust threshold as needed)
        SIMILARITY_THRESHOLD = 0.3
        filtered_chunks = [
            chunk for chunk in relevant_chunks 
            if chunk.score is None or chunk.score >= SIMILARITY_THRESHOLD
        ]
        print("\nDEBUG: Filtered chunks:")
        for i, chunk in enumerate(filtered_chunks):
            print(f"\n--- Filtered Chunk {i+1} ---")
            print(f"Score: {chunk.score}")
            print(f"Text:\n{chunk.text if hasattr(chunk, 'text') else chunk.content}")
            print("--------------------")
        return filtered_chunks