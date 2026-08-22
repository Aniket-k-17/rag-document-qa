import sys
import os

# Ensure the root project directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pdf_loader import load_pdfs_from_directory
from src.chunker import split_documents
from src.vector_store import build_and_save_vector_store

def main():
    print("Starting vector store build process...")
    
    # 1. Load PDFs
    print("\nLoading PDFs...")
    documents = load_pdfs_from_directory()
    print(f"Loaded {len(documents)} pages.")
    
    if not documents:
        print("No documents found. Please place PDFs in data/pdfs/")
        return

    # 2. Split into chunks
    print("\nCreating chunks...")
    chunks = split_documents(documents)
    print(f"Created {len(chunks)} chunks.")
    
    # 3. Build and save vector store
    print("\nCreating embeddings and building FAISS index (this may take a minute)...")
    build_and_save_vector_store(chunks)
    
    print("\nIndex saved successfully!")

if __name__ == "__main__":
    main()
