import asyncio
import os
import uuid
import frontmatter
import re
from typing import List
from src.services.qdrant_service import QdrantService, TextbookChunk

DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))

def parse_markdown_files(root_dir: str) -> List[TextbookChunk]:
    chunks = []
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith(('.md', '.mdx')):
                continue
                
            file_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(file_path, root_dir)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    
                content = post.content
                metadata = post.metadata
                
                # Basic metadata extraction
                title = metadata.get('title', os.path.splitext(filename)[0])
                # Generate a URL-friendly slug if sidebar_label or id isn't present, 
                # roughly mimicking Docusaurus routing
                doc_id = metadata.get('id', os.path.splitext(filename)[0])
                
                # Construct a rough URL (this might need adjustment depending on docusaurus config)
                # Assuming file path corresponds to URL structure
                url_path = os.path.relpath(dirpath, root_dir).replace('\\', '/')
                if url_path == '.':
                    url = f"/docs/{doc_id}"
                else:
                    url = f"/docs/{url_path}/{doc_id}"

                # Simple chunking strategy: Split by headers
                # This is a naive implementation but works for typical markdown structures
                # We split by Secondary headers (##) as primary split points
                sections = re.split(r'(^##\s+.*$)', content, flags=re.MULTILINE)
                
                current_section_title = title
                current_section_content = sections[0]
                
                # Add the first preamble chunk if it has content
                if current_section_content.strip():
                     chunks.append(TextbookChunk(
                        id=str(uuid.uuid4()),
                        content=current_section_content.strip(),
                        title=title,
                        chapter=os.path.basename(dirpath) if os.path.basename(dirpath).startswith('module') else "General",
                        section="Intro",
                        url=url,
                        source_file=rel_path,
                        position=0,
                        metadata={**metadata, "section_title": "Introduction"}
                    ))

                # Process subsequent sections
                for i in range(1, len(sections), 2):
                    if i + 1 < len(sections):
                        header = sections[i].strip().lstrip('#').strip()
                        section_body = sections[i+1].strip()
                        
                        if section_body:
                            chunks.append(TextbookChunk(
                                id=str(uuid.uuid4()),
                                content=f"{header}\n\n{section_body}", # Include header in content for context
                                title=title,
                                chapter=os.path.basename(dirpath) if os.path.basename(dirpath).startswith('module') else "General",
                                section=header,
                                url=url,
                                source_file=rel_path,
                                position=i,
                                metadata={**metadata, "section_title": header}
                            ))
                            
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                
    return chunks

async def ingest_docs():
    qdrant_service = QdrantService()
    
    print(f"Scanning directory: {DOCS_DIR}")
    chunks = parse_markdown_files(DOCS_DIR)
    
    # Recreate collection to ensure correct vector size (1024 for Cohere)
    from src.core.database import qdrant_client
    from src.core.config import settings
    from qdrant_client import models
    
    print(f"Recreating Qdrant collection '{settings.QDRANT_COLLECTION_NAME}' with size 1024...")
    qdrant_client.recreate_collection(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE)
    )
    print("Collection recreated.")

    print(f"Found {len(chunks)} chunks. Starting ingestion...")
    
    # Process in batches of 50 to avoid hitting API limits or timeouts if any
    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"Ingesting batch {i//batch_size + 1} ({len(batch)} chunks)...")
        await qdrant_service.batch_add_chunks(batch)
    
    print("Ingestion complete!")

if __name__ == "__main__":
    asyncio.run(ingest_docs())
