import os
import logging
import functools
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from src.config import VECTOR_STORE_DIR
from src.embeddings import get_embedding_model

logger = logging.getLogger(__name__)

@functools.lru_cache(maxsize=1)
def get_vector_store():
    """
    Loads the existing FAISS vector store from disk.
    Returns None if the vector store does not exist yet.
    """
    index_path = os.path.join(VECTOR_STORE_DIR, "index.faiss")
    
    if not os.path.exists(index_path):
        return None
        
    try:
        logger.info("Loading existing vector store from disk...")
        embeddings = get_embedding_model()
        # allow_dangerous_deserialization=True is required by FAISS because 
        # it uses pickle under the hood, but this is safe since we created the file locally.
        vector_store = FAISS.load_local(
            folder_path=VECTOR_STORE_DIR, 
            embeddings=embeddings, 
            allow_dangerous_deserialization=True
        )
        return vector_store
    except Exception as e:
        logger.error(f"Error loading vector store: {e}")
        return None

def build_and_save_vector_store(chunks: list[Document]):
    """
    Takes a list of document chunks, embeds them, and saves the FAISS index to disk.
    """
    logger.info(f"Building FAISS vector store for {len(chunks)} chunks...")
    embeddings = get_embedding_model()
    
    # Create the FAISS index from the chunks
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # Save it to disk so we don't have to rebuild it every time
    vector_store.save_local(VECTOR_STORE_DIR)
    logger.info(f"Vector store successfully saved to {VECTOR_STORE_DIR}")
    
    return vector_store
