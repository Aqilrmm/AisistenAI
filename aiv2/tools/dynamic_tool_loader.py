#################################################
# tools/dynamic_tool_loader.py
#################################################
import logging
import importlib
from typing import List, Dict, Any, Callable, Optional
from langchain.agents import Tool
from pydantic import BaseModel
from ..config import ENABLED_TOOLS

logger = logging.getLogger(__name__)

class ToolRegistry:
    """
    Registry untuk menyimpan dan mengelola tool
    """
    def __init__(self):
        self.tools = {}
        self.tool_functions = {}
        
    def register_tool(self, name: str, func: Callable, description: str, args_schema: Optional[BaseModel] = None) -> None:
        """
        Mendaftarkan tool baru
        """
        self.tool_functions[name] = func
        self.tools[name] = Tool(
            name=name,
            func=func,
            description=description,
            args_schema=args_schema
        )
        logger.info(f"Registered tool: {name}")
        
    def get_tool(self, name: str) -> Tool:
        """
        Mendapatkan tool berdasarkan nama
        """
        return self.tools.get(name)
        
    def get_all_tools(self) -> List[Tool]:
        """
        Mendapatkan semua tool yang sudah terdaftar
        """
        return list(self.tools.values())
        
    def get_enabled_tools(self, enabled_tools: List[str]) -> List[Tool]:
        """
        Mendapatkan tools yang diaktifkan
        """
        return [self.tools[name] for name in enabled_tools if name in self.tools]

# Inisialisasi registry
tool_registry = ToolRegistry()

def load_default_tools():
    """
    Mendaftarkan tools default
    """
    from .datetime_tools import get_datetime
    from ..utils.document_processor import load_documents
    from langchain.chains import RetrievalQA
    from langchain_ollama import OllamaLLM
    from ..config import OLLAMA_MODEL, OLLAMA_BASE_URL
    from .joke_fetcher import fetch_random_joke
    from pydantic import BaseModel


    # Contoh args_schema untuk tool dengan input
    class MathInputSchema(BaseModel):
        angka1: float
        angka2: float

    tool_registry.register_tool(
        name="JokeFetcher",
        func=fetch_random_joke,
        description=(
            "Mengambil lelucon acak dari Official Joke API. "
            "Cukup gunakan tool ini tanpa memasukkan input apapun. "
            "Hasil yang didapat perlu kamu kelola atau format kalimatnya menggunakan bahasa indonesia dan kalimatnya perlu kamu kembangkan "
            "terlebih dahulu sebelum ditampilkan ke pengguna."
        ),
        args_schema=None  # Tidak memerlukan input
    )

    
    tool_registry.register_tool(
        name="DateTime",
        func=get_datetime,
        description="Gunakan ini untuk mendapatkan informasi tanggal dan waktu saat ini.",
        args_schema=None  # Tidak memerlukan input
    )
    
    retriever = load_documents()
    llm = OllamaLLM(
        model=OLLAMA_MODEL, 
        base_url=OLLAMA_BASE_URL,
        temperature=0.7
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, 
        retriever=retriever,
        chain_type="stuff"
    )
    
    tool_registry.register_tool(
        name="DokumenQA",
        func=qa_chain.run,
        description="Gunakan ini untuk menjawab pertanyaan berdasarkan dokumen yang telah disediakan. Gunakan ketika user bertanya tentang informasi yang mungkin ada di dalam dokumen.",
        args_schema=None  # None Berarti tidak ada input yang diperlukan
    )
    
    return tool_registry

def get_enabled_tools() -> List[Tool]:
    """
    Mendapatkan daftar tools yang diaktifkan
    """
    if not tool_registry.tools:
        load_default_tools()
    
    return tool_registry.get_enabled_tools(ENABLED_TOOLS)
