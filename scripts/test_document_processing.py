#!/usr/bin/env python3
"""
Test script for document processing functionality
"""
import os
import sys
from pathlib import Path

# Add the backend/src directory to the path so we can import our modules
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_src_dir = os.path.join(script_dir, 'backend', 'src')
sys.path.insert(0, backend_src_dir)

from utils.document_parser import parse_document_file
from utils.text_splitter import text_splitter

def test_document_processing():
    """
    Test document processing with a sample document
    """
    print("Testing document processing...")

    # Find a sample document from the docs directory
    docs_dir = Path('../docs')
    sample_docs = list(docs_dir.rglob('*.mdx')) + list(docs_dir.rglob('*.md'))

    if not sample_docs:
        print("No sample documents found in docs directory")
        return False

    sample_doc = sample_docs[0]
    print(f"Testing with document: {sample_doc}")

    try:
        # Parse the document
        parsed_doc = parse_document_file(sample_doc)
        print(f"Document title: {parsed_doc['title']}")
        print(f"Number of headings: {len(parsed_doc['headings'])}")
        print(f"Number of sections: {len(parsed_doc['section_structure'])}")
        print(f"Metadata: {parsed_doc['metadata']}")

        # Test text splitting
        content = parsed_doc['content']
        chunks = text_splitter.split_text(content)
        print(f"Number of content chunks: {len(chunks)}")

        # Print first chunk as sample
        if chunks:
            print(f"First chunk preview: {chunks[0][:100]}...")

        print("Document processing test completed successfully!")
        return True

    except Exception as e:
        print(f"Error during document processing test: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_document_processing()
    if not success:
        print("Document processing test failed!")
        sys.exit(1)
    else:
        print("All tests passed!")