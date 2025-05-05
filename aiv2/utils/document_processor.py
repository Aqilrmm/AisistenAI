#################################################
# utils/document_processor.py
#################################################
import os
import logging
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from ..config import OLLAMA_MODEL, OLLAMA_BASE_URL, DOCUMENT_PATH, CHUNK_SIZE, CHUNK_OVERLAP

logger = logging.getLogger(__name__)

def load_documents():
    """
    Load dan proses dokumen untuk retrieval
    """
    try:
        if not os.path.exists(DOCUMENT_PATH):
            with open(DOCUMENT_PATH, "w") as f:
                f.write("Ini adalah dokumen contoh. Silakan ganti dengan konten yang sebenarnya.")
            logger.info(f"Created sample document at {DOCUMENT_PATH}")
        
        loader = TextLoader(DOCUMENT_PATH)
        documents = loader.load()
        
        text_splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        texts = text_splitter.split_documents(documents)
        
        embeddings = OllamaEmbeddings(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
        db = Chroma.from_documents(texts, embeddings)
        
        return db.as_retriever()
    except Exception as e:
        logger.error(f"Error loading documents: {e}")
        # Create a fallback retriever that returns this error message
        class FallbackRetriever:
            def get_relevant_documents(self, query):
                return []
        return FallbackRetriever()
