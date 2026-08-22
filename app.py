import streamlit as st
import os

# Set page config before any other Streamlit commands
st.set_page_config(page_title="RAG Document Q&A", page_icon="📚", layout="wide")

from src.rag_pipeline import answer_question
from src.vector_store import get_vector_store
from src.config import GEMINI_MODEL, EMBEDDING_MODEL_NAME

def main():
    st.title("RAG Document Q&A")
    st.markdown("Ask questions about the provided company documents.")

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("System")
        st.markdown(f"- **LLM:** {GEMINI_MODEL}")
        st.markdown(f"- **Embeddings:** {EMBEDDING_MODEL_NAME}")
        st.markdown("- **Vector Store:** FAISS")
        
        st.divider()
        st.header("Status")
        if os.path.exists("vectorstore/index.faiss"):
            st.success("Index ready")
            # Cheaply get chunk count without breaking anything
            try:
                vs = get_vector_store()
                if vs and hasattr(vs, "index"):
                    st.caption(f"**Indexed Chunks:** {vs.index.ntotal}")
            except Exception:
                pass
        else:
            st.error("Index missing. Please run scripts/build_index.py")

    # --- SAMPLE QUESTIONS ---
    if "question_input" not in st.session_state:
        st.session_state["question_input"] = ""
    if "run_query" not in st.session_state:
        st.session_state["run_query"] = False

    def run_sample(q):
        st.session_state["question_input"] = q
        st.session_state["run_query"] = True

    st.markdown("**Sample Questions:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("What is the employee PTO policy?", on_click=run_sample, args=("What is the employee PTO policy?",), use_container_width=True)
    with col2:
        st.button("What is the guaranteed SLA uptime?", on_click=run_sample, args=("What is the guaranteed SLA uptime?",), use_container_width=True)
    with col3:
        st.button("What auth method does the API use?", on_click=run_sample, args=("What authentication method does the API use?",), use_container_width=True)

    # --- MAIN INTERFACE ---
    question = st.text_input("Question input", key="question_input")
    
    ask_clicked = st.button("Ask", type="primary")
    
    if ask_clicked or st.session_state.run_query:
        # Reset the trigger so it doesn't run again on next arbitrary interaction
        st.session_state.run_query = False
        
        if not question.strip():
            st.warning("Please enter a question.")
            st.stop()
            
        if not os.path.exists("vectorstore/index.faiss"):
            st.error("The vector index has not been built yet. Please run scripts/build_index.py.")
            st.stop()

        with st.spinner("Searching documents and generating answer..."):
            try:
                result = answer_question(question)
                
                # --- DISPLAY ANSWER ---
                st.subheader("Answer")
                st.write(result["answer"])
                
                # --- DISPLAY SOURCES ---
                sources = result.get("sources", [])
                
                if sources:
                    st.subheader("Sources")
                    
                    for src in sources:
                        with st.expander(f"{src['source']} - Page {src['page']}"):
                            st.caption(f"**Chunk ID:** {src['chunk_id']}")
                            st.write(src['content'])
                else:
                    if result["answer"] != "I couldn't find enough relevant information in the provided documents to answer this question.":
                        st.info("No explicit sources were returned.")
                        
            except ValueError as ve:
                st.error(f"Configuration Error: {ve}")
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    st.error("Gemini API quota has been reached. Please wait a moment and try again.")
                else:
                    st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
