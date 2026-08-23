import logging
import functools
from langchain_groq import ChatGroq
from src.config import GROQ_API_KEY, GROQ_MODEL

logger = logging.getLogger(__name__)

@functools.lru_cache(maxsize=1)
def get_llm():
    """
    Initializes and returns the Groq LLM instance using the modern 
    langchain-groq package.
    """
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        logger.error("GROQ_API_KEY is not set or is invalid in the environment variables.")
        raise ValueError("GROQ_API_KEY must be configured in your .env file to use the LLM.")
        
    try:
        # ChatGroq is the modern standard for Groq integration.
        # Temperature 0 is used for more consistent responses. 
        # Grounding is handled by restricting generation to retrieved document context.
        llm = ChatGroq(
            model=GROQ_MODEL,
            api_key=GROQ_API_KEY,
            temperature=0,
            max_retries=2
        )
        return llm
    except Exception as e:
        logger.error(f"Failed to initialize Groq LLM: {e}")
        raise
