import sys
import os

# Ensure the root project directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pdf_loader import load_pdfs_from_directory

def test_ingestion():
    print("Testing PDF Ingestion...")
    documents = load_pdfs_from_directory()
    
    print(f"\nTotal document objects (pages) extracted: {len(documents)}")
    print("-" * 50)
    
    if not documents:
        print("No documents were extracted. Please check the data/pdfs directory.")
        return
        
    print("Preview of the first 5 pages:\n")
    for i, doc in enumerate(documents[:5]):
        metadata = doc.metadata
        # Create a single-line preview of the text
        content_preview = doc.page_content[:150].replace('\n', ' ').strip() + "..."
        
        print(f"File: {metadata['source']} | Page: {metadata['page']}")
        print(f"Preview: {content_preview}")
        print("-" * 50)
        
    if len(documents) > 5:
        print(f"... and {len(documents) - 5} more pages.")

if __name__ == "__main__":
    test_ingestion()
