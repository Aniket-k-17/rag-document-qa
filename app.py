import streamlit as st
import os

# Set page config before any other Streamlit commands
st.set_page_config(page_title="RAG Document Q&A", page_icon="📚", layout="wide")

from src.rag_pipeline import answer_question
from src.config import GEMINI_MODEL, EMBEDDING_MODEL_NAME

def main():
    st.title("📚 RAG Document Q&A System")
    st.markdown("Ask questions about the uploaded Atman Cloud Consultancy documents. "
                "The system retrieves relevant paragraphs and uses Gemini to answer.")

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("System Configuration")
        st.info(f"**Embedding Model:**\n{EMBEDDING_MODEL_NAME}")
        st.info(f"**LLM:**\n{GEMINI_MODEL}")
        st.info("**Vector Database:**\nFAISS (Local)")
        
        # We can loosely verify if index exists
        if os.path.exists("vectorstore/index.faiss"):
            st.success("Vector Store Status: Indexed & Ready ✅")
        else:
            st.error("Vector Store Status: Missing ❌\nPlease run `python scripts/build_index.py` first.")

    # --- MAIN INTERFACE ---
    question = st.text_input("Enter your question:")
    
    if st.button("Ask"):
        if not question.strip():
            st.warning("Please enter a question.")
            return
            
        if not os.path.exists("vectorstore/index.faiss"):
            st.error("The vector index has not been built yet. Please run the build_index.py script.")
            return

        with st.spinner("Searching documents and generating answer..."):
            try:
                result = answer_question(question)
                
                # --- DISPLAY ANSWER ---
                st.subheader("Answer")
                st.write(result["answer"])
                
                # --- DISPLAY SOURCES ---
                sources = result.get("sources", [])
                
                if sources:
                    st.subheader(f"Sources ({len(sources)})")
                    
                    for i, src in enumerate(sources):
                        with st.expander(f"[{i+1}] {src['source']} - Page {src['page']}"):
                            st.caption(f"**Chunk ID:** {src['chunk_id']}")
                            st.write(src['content'])
                else:
                    if result["answer"] != "I couldn't find enough relevant information in the provided documents to answer this question.":
                        st.info("No explicit sources were returned.")
                        
            except ValueError as ve:
                st.error(f"Configuration Error: {ve}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
