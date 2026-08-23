import logging
from src.retriever import retrieve_relevant_chunks
from src.llm import get_llm
from src.prompt import get_rag_prompt

logger = logging.getLogger(__name__)

# FAISS L2 distance threshold. 
# Above this threshold, we consider the text irrelevant.
# 1.5 is a standard starting point for all-MiniLM-L6-v2.
SIMILARITY_THRESHOLD = 1.5 

def answer_question(question: str) -> dict:
    """
    The main RAG pipeline:
    1. Retrieve relevant chunks.
    2. Filter out chunks that aren't relevant enough (hallucination prevention).
    3. Construct the prompt.
    4. Generate the answer with Groq.
    5. Return the answer and the exact sources used.
    """
    logger.info(f"Processing question: {question}")
    
    # 1. Retrieve raw chunks
    raw_results = retrieve_relevant_chunks(question)
    
    # 2. Filter by similarity threshold
    valid_chunks = []
    for doc, score in raw_results:
        # In FAISS L2 distance, closer to 0 is better.
        if score <= SIMILARITY_THRESHOLD:
            valid_chunks.append(doc)
        else:
            logger.info(f"Ignored chunk due to poor similarity score: {score:.4f}")

    # If no valid chunks remain, refuse to answer immediately without asking the LLM.
    if not valid_chunks:
        return {
            "answer": "I couldn't find enough relevant information in the provided documents to answer this question.",
            "sources": []
        }
        
    # 3. Construct context string and track sources
    context_parts = []
    sources = []
    
    for doc in valid_chunks:
        context_parts.append(doc.page_content)
        # We explicitly preserve metadata to send back to the UI
        sources.append({
            "source": doc.metadata.get("source"),
            "page": doc.metadata.get("page"),
            "chunk_id": doc.metadata.get("chunk_id"),
            "content": doc.page_content
        })
        
    context_text = "\n\n---\n\n".join(context_parts)
    
    # 4. Generate Answer using Groq
    llm = get_llm()
    prompt_template = get_rag_prompt()
    
    # Format the prompt
    prompt = prompt_template.format(context=context_text, question=question)
    
    logger.info("Sending context and prompt to Groq...")
    response = llm.invoke(prompt)
    
    # 5. Return structured result
    return {
        "answer": response.content.strip(),
        "sources": sources
    }
