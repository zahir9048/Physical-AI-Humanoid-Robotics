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

        return relevant_chunks