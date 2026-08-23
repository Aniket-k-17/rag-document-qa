import sys
import os

# Ensure the root project directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm import get_llm
from src.config import GROQ_MODEL

def test_groq_integration():
    print(f"Testing Groq LLM Integration (Model: {GROQ_MODEL})...")
    
    try:
        # 1. Load the model
        llm = get_llm()
        
        # 2. Ask a simple non-RAG question just to verify the API works
        question = "What is 2 + 2? Please answer in one word."
        print(f"\nSending test prompt to Groq: '{question}'")
        
        # invoke() is the modern LangChain standard for chatting
        response = llm.invoke(question)
        
        print(f"\nSuccess! Groq responded: {response.content.strip()}")
        print("Your API key is valid and the LLM wrapper is working perfectly.")
        
    except ValueError as ve:
        print(f"\nConfiguration Error: {ve}")
        print("Please open your .env file and paste a valid Groq API key.")
    except Exception as e:
        print(f"\nAPI Connection Error: {e}")
        print("Make sure your API key is correct and you have an internet connection.")

if __name__ == "__main__":
    test_groq_integration()
