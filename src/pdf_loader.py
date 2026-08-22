import os
import pymupdf  # PyMuPDF
import logging
from langchain_core.documents import Document
from src.config import DATA_DIR

# Set up basic logging to not silently ignore errors
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def load_pdfs_from_directory(directory_path: str = DATA_DIR) -> list[Document]:
    """
    Loads all PDF files from a directory, extracts text page by page,
    and returns a list of LangChain Document objects with metadata.
    """
    documents = []
    
    if not os.path.exists(directory_path):
        logger.error(f"Directory does not exist: {directory_path}")
        return documents

    for filename in os.listdir(directory_path):
        if not filename.lower().endswith(".pdf"):
            continue
            
        file_path = os.path.join(directory_path, filename)
        logger.info(f"Processing: {filename}")
        
        try:
            # Open PDF with PyMuPDF
            doc = pymupdf.open(file_path)
            
            if doc.page_count == 0:
                logger.warning(f"File {filename} has no pages.")
                continue

            extracted_text_found = False

            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                # 'text' extracts layout-preserved text reasonably well
                text = page.get_text("text").strip()
                
                # Check for empty or image-only pages without text
                if not text:
                    logger.warning(f"No extractable text found on page {page_num + 1} of {filename}.")
                    continue
                
                extracted_text_found = True
                
                # Create LangChain Document
                # We store the source filename and 1-indexed page number
                metadata = {
                    "source": filename,
                    "page": page_num + 1 
                }
                
                langchain_doc = Document(page_content=text, metadata=metadata)
                documents.append(langchain_doc)
                
            if not extracted_text_found:
                logger.warning(f"Could not extract any text from {filename}. It might be a scanned image.")

            doc.close()
            
        except Exception as e:
            logger.error(f"Failed to process {filename}. Error: {str(e)}")
            
    logger.info(f"Successfully loaded {len(documents)} pages with text.")
    return documents
