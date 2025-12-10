import re
from typing import List, Tuple
from src.core.config import settings

class TextSplitter:
    def __init__(self, chunk_size: int = None, overlap_size: int = None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.overlap_size = overlap_size or settings.OVERLAP_SIZE

    def split_text(self, text: str) -> List[str]:
        """
        Split text into chunks based on the specified chunk size with overlap
        """
        if not text:
            return []

        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        chunks = []

        current_chunk = ""
        for paragraph in paragraphs:
            # If adding the paragraph would exceed the chunk size
            if len(current_chunk) + len(paragraph) > self.chunk_size:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())

                # Start a new chunk with some overlap from the previous one
                if self.overlap_size > 0:
                    # Add overlap from the end of the current chunk
                    overlap_start = max(0, len(current_chunk) - self.overlap_size)
                    current_chunk = current_chunk[overlap_start:] + paragraph
                else:
                    current_chunk = paragraph
            else:
                current_chunk += "\n\n" + paragraph

        # Add the last chunk if it has content
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # If we still have chunks that are too large, split them by sentences
        final_chunks = []
        for chunk in chunks:
            if len(chunk) <= self.chunk_size:
                final_chunks.append(chunk)
            else:
                # Split large chunk by sentences
                sentence_chunks = self._split_by_sentences(chunk)
                final_chunks.extend(sentence_chunks)

        return final_chunks

    def _split_by_sentences(self, text: str) -> List[str]:
        """
        Split text by sentences while respecting the chunk size
        """
        # Split text into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())

                # If the sentence itself is too long, split it by length
                if len(sentence) > self.chunk_size:
                    sub_chunks = self._split_long_sentence(sentence)
                    chunks.extend(sub_chunks[:-1])  # Add all but the last sub-chunk
                    current_chunk = sub_chunks[-1] if sub_chunks else ""  # Start new chunk with the last sub-chunk
                else:
                    current_chunk = sentence

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def _split_long_sentence(self, sentence: str) -> List[str]:
        """
        Split a sentence that is too long into smaller chunks
        """
        if len(sentence) <= self.chunk_size:
            return [sentence]

        chunks = []
        for i in range(0, len(sentence), self.chunk_size):
            chunk = sentence[i:i + self.chunk_size]
            chunks.append(chunk)

        return chunks

# Global instance
text_splitter = TextSplitter()