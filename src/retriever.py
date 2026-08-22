import logging
from src.vector_store import get_vector_store
from src.config import TOP_K

logger = logging.getLogger(__name__)

def retrieve_relevant_chunks(question: str, top_k: int = TOP_K):
    """
    Performs semantic search on the vector store using the user's question.
    Returns a list of tuples: (LangChain Document, distance_score).
    Note: Since FAISS uses L2 distance by default, a LOWER score means HIGHER similarity.
    """
    vector_store = get_vector_store()
    
    if not vector_store:
        logger.error("Vector store not found. Please run the build_index script first.")
        return []
        
    logger.info(f"Retrieving top {top_k} chunks for question: '{question}'")
    
    # We use similarity_search_with_score so we get the relevance metric.
    # This is critical for preventing hallucinations later if the score is too bad.
    results = vector_store.similarity_search_with_score(question, k=top_k)
    
    return results
