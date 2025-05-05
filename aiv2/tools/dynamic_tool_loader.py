#################################################
# tools/dynamic_tool_loader.py
#################################################
import logging
import importlib
from typing import List, Dict, Any, Callable
from langchain.agents import Tool
from ..config import ENABLED_TOOLS

logger = logging.getLogger(__name__)

class ToolRegistry:
    """
    Registry untuk menyimpan dan mengelola tool
    """
    def __init__(self):
        self.tools = {}
        self.tool_functions = {}
        
    def register_tool(self, name: str, func: Callable, description: str) -> None:
        """
        Mendaftarkan tool baru
        """
        self.tool_functions[name] = func
        self.tools[name] = Tool(
            name=name,
            func=func,
            description=description
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
    # Referensikan fungsi dari modul lain
    from .math_tools import perkalian, hitung_aritmatika
    from .knowledge_tools import wikipedia_search
    from .conversion_tools import konversi_satuan
    from .datetime_tools import get_datetime
    from ..utils.document_processor import load_documents
    from langchain.chains import RetrievalQA
    from langchain_ollama import OllamaLLM
    from ..config import OLLAMA_MODEL, OLLAMA_BASE_URL
    from .joke_fetcher import fetch_random_joke

    tool_registry.register_tool(
        name="JokeFetcher",
        func=fetch_random_joke,
        description=(
            "Mengambil lelucon acak dari Official Joke API. "
            "Cukup gunakan tool ini tanpa memasukkan input apapun. "
            "Hasil yang didapat perlu kamu kelola atau format kalimatnya menggunakan bahasa indonesia dan kalimatnya perlu kamu kembangkan "
            "terlebih dahulu sebelum ditampilkan ke pengguna."
        )
    )


    # Daftarkan tool matematika
    tool_registry.register_tool(
        name="Perkalian",
        func=perkalian,
        description="Gunakan ini untuk menghitung perkalian dua angka. Format: 'Hitung 3 dikali 1' atau '5 x 2'."
    )
    
    tool_registry.register_tool(
        name="Aritmatika",
        func=hitung_aritmatika,
        description="Gunakan ini untuk melakukan perhitungan aritmatika sederhana seperti penjumlahan, pengurangan, pembagian, dan perpangkatan."
    )
    
    # Daftarkan tool pencarian
    tool_registry.register_tool(
        name="WikipediaSearch",
        func=wikipedia_search,
        description="Gunakan ini untuk mencari informasi dari Wikipedia ketika user bertanya tentang orang (seperti Sukarno, Soekarno, Suharto), tempat, konsep, atau topik tertentu. Gunakan tool ini ketika user bertanya 'apakah kamu tahu tentang X' atau 'siapa X', ini adalah pertanyaan tentang informasi faktual."
    )
    
    # Daftarkan tool konversi
    tool_registry.register_tool(
        name="KonversiSatuan",
        func=konversi_satuan,
        description="Gunakan ini untuk mengkonversi satuan (panjang, berat, suhu). Format: '5 km ke m', '10 kg ke g', '30 celsius ke fahrenheit'."
    )
    
    # Daftarkan tool datetime
    tool_registry.register_tool(
        name="DateTime",
        func=get_datetime,
        description="Use this to get the current date and time information"
            "Simply use this tool without entering any input, Action this DateTime(). "
            "You need to manage the results or format the sentences using Indonesian language and develop the sentences "
            "first before displaying it to the user."     
    )
    
    # Daftarkan tool dokumen QA
    # Ini adalah contoh tool yang lebih kompleks yang membutuhkan inisialisasi khusus
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
        description="Gunakan ini untuk menjawab pertanyaan berdasarkan dokumen yang telah disediakan. Gunakan ketika user bertanya tentang informasi yang mungkin ada di dalam dokumen."
    )
    
    return tool_registry

def get_enabled_tools() -> List[Tool]:
    """
    Mendapatkan daftar tools yang diaktifkan
    """
    # Pastikan tools sudah dimuat
    if not tool_registry.tools:
        load_default_tools()
    
    return tool_registry.get_enabled_tools(ENABLED_TOOLS)
