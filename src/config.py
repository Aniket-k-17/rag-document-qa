import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration Settings ---

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "pdfs")
VECTOR_STORE_DIR = os.path.join(BASE_DIR, "vectorstore")

# Ensure necessary directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

# API Keys and Models
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

# Chunking Configuration
CHUNK_SIZE = 700
CHUNK_OVERLAP = 100

# Retrieval Configuration
TOP_K = 3

# Embedding Model
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
