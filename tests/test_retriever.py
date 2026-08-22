import sys
import os

# Ensure the root project directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.retriever import retrieve_relevant_chunks

def test_retrieval():
    # A clear, specific question that should exist in the employee handbook
    question = "How many days of paid time off (PTO) do employees get?"
    print(f"User Question: '{question}'\n")
    
    results = retrieve_relevant_chunks(question)
    
    if not results:
        print("No results returned. Ensure you have run 'python scripts/build_index.py' first.")
        return
        
    print(f"Retrieved Top {len(results)} Relevant Chunks:")
    print("=" * 60)
    
    for i, (doc, score) in enumerate(results):
        metadata = doc.metadata
        
        print(f"Rank: {i + 1}")
        # In FAISS L2 distance, closer to 0 is better.
        print(f"Similarity Distance: {score:.4f} (Lower is more similar)")
        print(f"Source Document: {metadata.get('source')} | Page: {metadata.get('page')}")
        print(f"Chunk ID: {metadata.get('chunk_id')}")
        
        # Display the actual text we retrieved
        preview = doc.page_content.replace('\n', ' ')
        if len(preview) > 200:
            preview = preview[:200] + "..."
            
        print(f"Content: {preview}")
        print("-" * 60)

if __name__ == "__main__":
    test_retrieval()
