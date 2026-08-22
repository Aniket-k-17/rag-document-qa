import logging
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import EMBEDDING_MODEL_NAME

logger = logging.getLogger(__name__)

def get_embedding_model():
    """
    Returns the embedding model used for vectorizing text.
    We use a local HuggingFace model so it runs on our machine for free.
    """
    try:
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
        # HuggingFaceEmbeddings will automatically download the model 
        # from HuggingFace on the first run and cache it locally.
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        return embeddings
    except Exception as e:
        logger.error(f"Failed to load embedding model: {e}")
        raise
