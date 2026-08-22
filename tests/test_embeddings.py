import sys
import os

# Ensure the root project directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.embeddings import get_embedding_model

def test_embedding_model():
    print("Step 1: Loading the embedding model...")
    print("(If this is the first time, it might take a moment to download the model weights.)\n")
    
    model = get_embedding_model()
    
    sample_text = "Atman Cloud Consultancy provides cloud infrastructure."
    print(f"Step 2: Generating embedding for the sentence:\n'{sample_text}'\n")
    
    # embed_query is used for single strings
    vector = model.embed_query(sample_text)
    
    print(f"Success! The model generated a dense vector of size: {len(vector)}")
    print("This means our sentence was converted into a list of 384 numbers.")
    print(f"Here are the first 5 numbers of the vector: {vector[:5]}")

if __name__ == "__main__":
    test_embedding_model()
