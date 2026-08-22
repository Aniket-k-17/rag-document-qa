import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

logger = logging.getLogger(__name__)

def split_documents(documents: list[Document], chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> list[Document]:
    """
    Splits a list of LangChain Document objects into smaller chunks.
    Preserves original metadata and adds a deterministic chunk_id.
    """
    if not documents:
        logger.warning("No documents provided to split_documents.")
        return []

    # Using RecursiveCharacterTextSplitter because it tries to split on paragraphs, 
    # then sentences, then words, preserving semantic meaning as much as possible.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = []
    
    # We will manually split and assign chunk IDs per document page
    for doc in documents:
        # Split the text of a single page
        doc_chunks = text_splitter.split_text(doc.page_content)
        
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", 0)
        
        for i, chunk_text in enumerate(doc_chunks):
            # Create a deterministic chunk_id like: Employee_Handbook.pdf_p1_c0
            chunk_id = f"{source}_p{page}_c{i}"
            
            # Copy original metadata and add chunk_id
            chunk_metadata = doc.metadata.copy()
            chunk_metadata["chunk_id"] = chunk_id
            
            chunk_doc = Document(page_content=chunk_text, metadata=chunk_metadata)
            chunks.append(chunk_doc)
            
    logger.info(f"Split {len(documents)} pages into {len(chunks)} chunks.")
    return chunks
