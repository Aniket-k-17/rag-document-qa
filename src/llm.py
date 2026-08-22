import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)

def get_llm():
    """
    Initializes and returns the Google Gemini LLM instance using the modern 
    langchain-google-genai package.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        logger.error("GEMINI_API_KEY is not set or is invalid in the environment variables.")
        raise ValueError("GEMINI_API_KEY must be configured in your .env file to use the LLM.")
        
    try:
        # ChatGoogleGenerativeAI is the modern standard for Gemini integration.
        # We set temperature=0 to ensure the model is highly deterministic 
        # and factual, which is critical for preventing RAG hallucinations.
        llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GEMINI_API_KEY,
            temperature=0,
            max_retries=2
        )
        return llm
    except Exception as e:
        logger.error(f"Failed to initialize Gemini LLM: {e}")
        raise
