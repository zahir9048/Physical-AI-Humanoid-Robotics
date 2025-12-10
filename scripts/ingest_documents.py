#!/usr/bin/env python3
"""
Script to ingest textbook documents into the vector database
"""
import os
import sys
import uuid
from pathlib import Path
import asyncio
import markdown
from typing import List

# Add the backend/src directory to the path so we can import our modules
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_src_dir = os.path.join(script_dir, '..', 'backend', 'src')
sys.path.insert(0, backend_src_dir)

from services.qdrant_service import QdrantService, TextbookChunk
from utils.text_splitter import text_splitter
from utils.document_parser import parse_document_file
from core.config import settings

def process_document(file_path: Path) -> List[TextbookChunk]:
    """
    Process a single document file and return a list of chunks
    """
    print(f"Processing document: {file_path}")

    # Parse the document to extract content and metadata
    parsed_doc = parse_document_file(file_path)

    title = parsed_doc['title']
    content = parsed_doc['content']
    metadata = parsed_doc['metadata']

    # Split content into chunks
    chunks = text_splitter.split_text(content)

    textbook_chunks = []
    for i, chunk_content in enumerate(chunks):
        chunk = TextbookChunk(
            id=str(uuid.uuid4()),
            content=chunk_content,
            title=title,
            chapter=file_path.parent.name or "unknown",
            section=file_path.stem,
            url=f"/{file_path.relative_to(Path('../docs')).as_posix()}" if 'docs' in str(file_path) else f"/{file_path.name}",
            source_file=file_path.name,
            position=i,
            metadata={
                "file_path": str(file_path),
                "chunk_index": i,
                "total_chunks": len(chunks),
                "original_title": title,
                **metadata  # Include any additional metadata from frontmatter
            }
        )
        textbook_chunks.append(chunk)

    return textbook_chunks

def find_document_files(docs_dir: str) -> List[Path]:
    """
    Find all document files in the specified directory
    """
    document_extensions = {'.md', '.mdx', '.txt', '.py', '.js', '.ts', '.tsx', '.json', '.yaml', '.yml'}
    document_files = []

    docs_path = Path(docs_dir)
    for file_path in docs_path.rglob('*'):
        if file_path.suffix.lower() in document_extensions:
            document_files.append(file_path)

    return document_files

async def ingest_documents():
    print("Starting document ingestion...")

    # Initialize Qdrant service
    qdrant_service = QdrantService()

    # Find all document files in the docs directory
    docs_dir = os.path.join(script_dir, '..', 'docs')
    document_files = find_document_files(docs_dir)

    print(f"Found {len(document_files)} document files to process")

    total_chunks = 0
    for file_path in document_files:
        try:
            # Process the document
            chunks = process_document(file_path)

            # Add chunks to Qdrant
            if chunks:
                success = await qdrant_service.batch_add_chunks(chunks)
                if success:
                    print(f"Successfully ingested {len(chunks)} chunks from {file_path.name}")
                    total_chunks += len(chunks)
                else:
                    print(f"Failed to ingest chunks from {file_path.name}")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

    print(f"Document ingestion completed! Total chunks ingested: {total_chunks}")

if __name__ == "__main__":
    asyncio.run(ingest_documents())