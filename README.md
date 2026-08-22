# RAG Document Q&A System

## 1. Project Overview
This project is a Retrieval-Augmented Generation (RAG) system built for Atman Cloud Consultancy. It allows users to upload a collection of PDF documents and ask natural language questions about them. The system strictly grounds its answers in the provided documents to ensure factual accuracy.

## 2. Problem Statement
Large Language Models (LLMs) are powerful but prone to hallucination, and they lack knowledge of proprietary corporate documents. This project solves that by converting private PDFs into a searchable vector database, extracting relevant paragraphs, and forcing the LLM to read *only* those paragraphs when answering a user's question.

## 3. Architecture
The system follows a standard offline-ingestion and online-retrieval RAG pipeline:
1. **Ingestion**: Read PDFs $\rightarrow$ Extract Text $\rightarrow$ Chunk Text $\rightarrow$ Generate Embeddings $\rightarrow$ Save to FAISS.
2. **Retrieval**: User Question $\rightarrow$ Question Embedding $\rightarrow$ FAISS Similarity Search $\rightarrow$ Top K Chunks.
3. **Generation**: Top K Chunks + Strict Prompt $\rightarrow$ Gemini LLM $\rightarrow$ Grounded Answer + Source Attribution.

## 4. Project Structure
```text
rag-document-qa/
├── app.py                     # Streamlit frontend
├── requirements.txt           # Python dependencies
├── .env                       # API keys (not checked into git)
├── data/pdfs/                 # Raw PDF files
├── src/                       # Core application logic
│   ├── config.py              # Centralized configuration
│   ├── pdf_loader.py          # PyMuPDF ingestion
│   ├── chunker.py             # LangChain text splitting
│   ├── embeddings.py          # HuggingFace local embeddings
│   ├── vector_store.py        # FAISS database logic
│   ├── retriever.py           # Semantic search logic
│   ├── llm.py                 # Gemini LLM wrapper
│   ├── prompt.py              # Hallucination-prevention prompt
│   └── rag_pipeline.py        # Main Q&A pipeline
├── scripts/
│   └── build_index.py         # Script to ingest all PDFs to FAISS
└── vectorstore/               # Persisted FAISS database
```

## 5. Technology Choices
- **Language**: Python (Industry standard for AI/ML).
- **Framework**: LangChain (Provides excellent wrappers for chunking and prompt templating without being overly restrictive).
- **LLM**: Google Gemini (`Gemini 2.5 Flash`) via `langchain-google-genai`. Chosen for its generous free tier, speed, and high reasoning capabilities.
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`. Chosen because it is small, fast, completely free, and runs entirely locally on CPU while maintaining high accuracy for English text.
- **Vector Database**: FAISS (Facebook AI Similarity Search). Chosen because it runs purely in-memory and saves to local disk, requiring no complex Docker setups or third-party cloud accounts.
- **UI**: Streamlit. Allows for rapid prototyping of a clean, interactive web application using pure Python.

## 6. PDF Ingestion Approach
I used **PyMuPDF (`pymupdf`)** because it is significantly faster and more accurate at preserving basic text layouts (like columns and tables) than older libraries like PyPDF2. Extraction is done page-by-page so we can permanently attach the correct page number metadata to the text.

## 7. Chunking Strategy
I used `RecursiveCharacterTextSplitter` with a `chunk_size` of 700 characters and a `chunk_overlap` of 100 characters. 
- **Size**: 700 characters is roughly 1-2 paragraphs. If chunks are too large, the semantic embedding gets "diluted". If they are too small, the LLM loses context.
- **Overlap**: 100 characters ensures that if a critical sentence is split across two chunks, the context is still preserved at the boundaries.

## 8. Source Attribution
When a page is chunked, the application strictly preserves the source filename, page number, and generates a deterministic `chunk_id`. This metadata travels with the text into the vector database. When the LLM answers, the frontend explicitly displays this metadata so the user can verify the answer manually.

## 9. Hallucination Handling
Hallucinations are prevented in two ways:
1. **Similarity Threshold**: In `rag_pipeline.py`, we check the FAISS L2 distance score. If a user asks "What is the weather in Pune?", the vector search will return text, but the distance score will be very high (poor match). We intercept this in Python and refuse to answer before ever contacting the LLM.
2. **Strict Prompting**: In `prompt.py`, the LLM is explicitly instructed with rules like "NEVER invent information" and is given an exact phrase to output if the context is insufficient.

## 10. Setup Instructions
1. Clone the repository and navigate into it.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment (Windows: `venv\Scripts\activate`, Mac/Linux: `source venv/bin/activate`).
4. Install dependencies: `pip install -r requirements.txt`
5. Rename `.env.example` to `.env` and insert your `GEMINI_API_KEY`.
6. Place your PDFs inside `data/pdfs/`.

## 11. How to run
**Step 1: Build the Vector Index**
You only need to do this once, or whenever you add new PDFs.
```bash
python scripts/build_index.py
```

**Step 2: Run the Web App**
```bash
streamlit run app.py
```

## 12. Limitations & Future Improvements
- **Tables and Images**: Standard text extraction struggles with complex tables and ignores images. Future improvements could involve OCR or multimodal models (like sending the raw PDF image to Gemini Vision).
- **Scalability**: FAISS is in-memory. If we scale to millions of documents, we would need to migrate to a dedicated vector database like Pinecone, Milvus, or pgvector.
- **Evaluation**: We currently rely on manual testing. A future improvement would be implementing RAGAS or TruLens for automated retrieval and generation evaluation.

## 13. AI Tools Used
Google Gemini AI was used to assist in writing standard boilerplate code, brainstorming chunking sizes, and formatting this README. All architecture, logic, and design decisions were carefully structured and reviewed by a human engineer.
