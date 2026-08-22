import sys
import os

# Ensure the root project directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pdf_loader import load_pdfs_from_directory
from src.chunker import split_documents
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

def test_chunking():
    print("Step 1: Loading PDFs...")
    documents = load_pdfs_from_directory()
    
    if not documents:
        print("No documents found. Aborting test.")
        return
        
    print(f"\nStep 2: Splitting {len(documents)} pages into chunks...")
    print(f"Configuration -> chunk_size: {CHUNK_SIZE}, chunk_overlap: {CHUNK_OVERLAP}")
    
    chunks = split_documents(documents)
    
    print(f"\nTotal chunks generated: {len(chunks)}")
    print("-" * 50)
    
    print("Preview of the first 3 chunks:\n")
    for i, chunk in enumerate(chunks[:3]):
        metadata = chunk.metadata
        # Display short preview
        content_preview = chunk.page_content[:150].replace('\n', ' ').strip() + "..."
        
        print(f"Chunk ID: {metadata['chunk_id']}")
        print(f"Source: {metadata['source']} | Page: {metadata['page']}")
        print(f"Length: {len(chunk.page_content)} characters")
        print(f"Preview: {content_preview}")
        print("-" * 50)
        
    if len(chunks) > 3:
        print(f"... and {len(chunks) - 3} more chunks.")

if __name__ == "__main__":
    test_chunking()
