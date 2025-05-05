# ai_assistant/
# ├── main.py                   # File utama untuk menjalankan aplikasi
# ├── config.py                 # Konfigurasi aplikasi
# ├── utils/
# │   ├── __init__.py           # Init untuk package utils
# │   ├── logging_setup.py      # Setup logging
# │   └── document_processor.py # Fungsi untuk memproses dokumen
# ├── tools/
# │   ├── __init__.py           # Init untuk package tools
# │   ├── math_tools.py         # Tools untuk matematika (perkalian, aritmatika)
# │   ├── knowledge_tools.py    # Tools untuk pencarian pengetahuan (Wikipedia)
# │   ├── conversion_tools.py   # Tools untuk konversi satuan
# │   ├── datetime_tools.py     # Tools untuk waktu dan tanggal
# │   └── dynamic_tool_loader.py # Loader tools dinamis
# └── agent/
#     ├── __init__.py           # Init untuk package agent
#     ├── agent_factory.py      # Factory untuk membuat agent
#     └── prompt_templates.py   # Template prompt untuk agent

#################################################
# config.py
#################################################
import os

# Konfigurasi umum
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:0.6b")
DOCUMENT_PATH = os.environ.get("DOCUMENT_PATH", "dokumen.txt")

# Konfigurasi pemrosesan dokumen
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", 100))

# Konfigurasi logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# Konfigurasi LLM
LLM_TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", 0.7))
LLM_STREAMING = os.environ.get("LLM_STREAMING", "True").lower() == "true"

# Daftar tools yang diaktifkan (untuk dynamic loading)
ENABLED_TOOLS = os.environ.get("ENABLED_TOOLS", "DokumenQA,Perkalian,WikipediaSearch,DateTime,KonversiSatuan,Aritmatika").split(",")

# Konfigurasi dinamis untuk setiap tool
TOOL_CONFIG = {
    "WikipediaSearch": {
        "language": os.environ.get("WIKIPEDIA_LANGUAGE", "id"),
        "fallback_language": os.environ.get("WIKIPEDIA_FALLBACK_LANGUAGE", "en"),
        "summary_length": int(os.environ.get("WIKIPEDIA_SUMMARY_LENGTH", 500))
    }
}

#################################################
# utils/logging_setup.py
#################################################
import logging
from ..config import LOG_LEVEL

def setup_logging():
    """
    Setup logging untuk aplikasi
    """
    log_level = getattr(logging, LOG_LEVEL.upper())
    logging.basicConfig(
        level=log_level, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

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

#################################################
# tools/math_tools.py
#################################################
import re
import logging

logger = logging.getLogger(__name__)

def perkalian(query: str) -> str:
    """
    Fungsi untuk menghitung perkalian dari query dalam bahasa natural
    """
    try:
        teks = query.lower()
        # Cari pola angka1 * angka2 dengan berbagai varian kata
        match = re.search(r"(\d+)\s*(?:x|kali|dikali|dikalikan dengan|×)?\s*(\d+)", teks)
        
        if match:
            a = int(match.group(1))
            b = int(match.group(2))
            hasil = a * b
            return f"{a} × {b} = {hasil}"
        else:
            # Cari pola 'berapa 5 x 3' atau 'hitung 4 kali 7'
            match = re.search(r"(?:berapa|hitung).*?(\d+)\s*(?:x|kali|dikali|dikalikan dengan|×)?\s*(\d+)", teks)
            if match:
                a = int(match.group(1))
                b = int(match.group(2))
                hasil = a * b
                return f"{a} × {b} = {hasil}"
            
            return "Maaf, aku tidak paham format perkalianmu. Coba misalnya '5 dikali 2' atau 'berapa 3 kali 4'."
    except Exception as e:
        logger.error(f"Error in perkalian function: {e}")
        return f"Terjadi kesalahan saat menghitung perkalian: {str(e)}"

def hitung_aritmatika(query: str) -> str:
    """
    Fungsi untuk melakukan perhitungan aritmatika sederhana
    """
    try:
        query = query.lower()
        
        # Deteksi operasi tambah
        match_tambah = re.search(r"(\d+(?:\.\d+)?)\s*(?:tambah|ditambah|plus|\+)\s*(\d+(?:\.\d+)?)", query)
        if match_tambah:
            a = float(match_tambah.group(1))
            b = float(match_tambah.group(2))
            hasil = a + b
            return f"{a} + {b} = {hasil}"
            
        # Deteksi operasi kurang
        match_kurang = re.search(r"(\d+(?:\.\d+)?)\s*(?:kurang|dikurang|minus|-)\s*(\d+(?:\.\d+)?)", query)
        if match_kurang:
            a = float(match_kurang.group(1))
            b = float(match_kurang.group(2))
            hasil = a - b
            return f"{a} - {b} = {hasil}"
            
        # Deteksi operasi kali (sudah ditangani di fungsi perkalian)
        
        # Deteksi operasi bagi
        match_bagi = re.search(r"(\d+(?:\.\d+)?)\s*(?:bagi|dibagi|dibagi dengan|\/|:)\s*(\d+(?:\.\d+)?)", query)
        if match_bagi:
            a = float(match_bagi.group(1))
            b = float(match_bagi.group(2))
            if b == 0:
                return "Tidak bisa melakukan pembagian dengan nol"
            hasil = a / b
            return f"{a} ÷ {b} = {hasil}"
            
        # Deteksi operasi pangkat
        match_pangkat = re.search(r"(\d+(?:\.\d+)?)\s*(?:pangkat|dipangkatkan|power|\^)\s*(\d+(?:\.\d+)?)", query)
        if match_pangkat:
            a = float(match_pangkat.group(1))
            b = float(match_pangkat.group(2))
            hasil = a ** b
            return f"{a} ^ {b} = {hasil}"
            
        return "Maaf, saya tidak dapat mengenali format perhitungan. Contoh format yang didukung: '5 tambah 3', '10 dikurang 2', '8 dibagi 4', '2 pangkat 3'"
    except Exception as e:
        logger.error(f"Error in hitung_aritmatika function: {e}")
        return f"Terjadi kesalahan saat melakukan perhitungan: {str(e)}"

#################################################
# tools/knowledge_tools.py
#################################################
import re
import logging
import wikipediaapi
from ..config import TOOL_CONFIG

logger = logging.getLogger(__name__)

# Database tokoh terkenal Indonesia
TOKOH_TERKENAL = {
    "sukarno": {
        "nama": "Sukarno",
        "info": "Sukarno (lahir di Surabaya, Jawa Timur, 6 Juni 1901 – meninggal di Jakarta, 21 Juni 1970) adalah Presiden pertama Republik Indonesia yang menjabat pada periode 1945–1967. Ia adalah seorang tokoh perjuangan yang memainkan peranan penting dalam memerdekakan bangsa Indonesia dari penjajahan Belanda. Ia adalah Proklamator Kemerdekaan Indonesia (bersama dengan Mohammad Hatta) yang terjadi pada tanggal 17 Agustus 1945. Sukarno adalah yang pertama kali mencetuskan konsep mengenai Pancasila sebagai dasar negara Indonesia dan ia sendiri yang menamainya.",
        "url": "https://id.wikipedia.org/wiki/Sukarno"
    },
    "soekarno": {
        "nama": "Sukarno",
        "info": "Sukarno (lahir di Surabaya, Jawa Timur, 6 Juni 1901 – meninggal di Jakarta, 21 Juni 1970) adalah Presiden pertama Republik Indonesia yang menjabat pada periode 1945–1967. Ia adalah seorang tokoh perjuangan yang memainkan peranan penting dalam memerdekakan bangsa Indonesia dari penjajahan Belanda. Ia adalah Proklamator Kemerdekaan Indonesia (bersama dengan Mohammad Hatta) yang terjadi pada tanggal 17 Agustus 1945. Sukarno adalah yang pertama kali mencetuskan konsep mengenai Pancasila sebagai dasar negara Indonesia dan ia sendiri yang menamainya.",
        "url": "https://id.wikipedia.org/wiki/Sukarno"
    },
    "bung karno": {
        "nama": "Sukarno",
        "info": "Sukarno (lahir di Surabaya, Jawa Timur, 6 Juni 1901 – meninggal di Jakarta, 21 Juni 1970) adalah Presiden pertama Republik Indonesia yang menjabat pada periode 1945–1967. Ia adalah seorang tokoh perjuangan yang memainkan peranan penting dalam memerdekakan bangsa Indonesia dari penjajahan Belanda. Ia adalah Proklamator Kemerdekaan Indonesia (bersama dengan Mohammad Hatta) yang terjadi pada tanggal 17 Agustus 1945. Sukarno adalah yang pertama kali mencetuskan konsep mengenai Pancasila sebagai dasar negara Indonesia dan ia sendiri yang menamainya.",
        "url": "https://id.wikipedia.org/wiki/Sukarno"
    },
    "suharto": {
        "nama": "Suharto",
        "info": "Jenderal Besar TNI (Purn.) H. M. Soeharto (lahir di Kemusuk, Yogyakarta, 8 Juni 1921 – meninggal di Jakarta, 27 Januari 2008) adalah Presiden kedua Indonesia yang menjabat dari tahun 1967 sampai 1998. Sebelumnya, Soeharto adalah seorang perwira tinggi militer yang bergabung dengan Tentara Nasional Indonesia (TNI) sejak zaman kemerdekaan.",
        "url": "https://id.wikipedia.org/wiki/Soeharto"
    },
    "soeharto": {
        "nama": "Suharto",
        "info": "Jenderal Besar TNI (Purn.) H. M. Soeharto (lahir di Kemusuk, Yogyakarta, 8 Juni 1921 – meninggal di Jakarta, 27 Januari 2008) adalah Presiden kedua Indonesia yang menjabat dari tahun 1967 sampai 1998. Sebelumnya, Soeharto adalah seorang perwira tinggi militer yang bergabung dengan Tentara Nasional Indonesia (TNI) sejak zaman kemerdekaan.",
        "url": "https://id.wikipedia.org/wiki/Soeharto"
    }
}

def wikipedia_search(query: str) -> str:
    """
    Fungsi untuk mencari informasi di Wikipedia dengan penanganan khusus untuk tokoh terkenal
    """
    try:
        config = TOOL_CONFIG.get("WikipediaSearch", {})
        main_language = config.get("language", "id")
        fallback_language = config.get("fallback_language", "en")
        summary_length = config.get("summary_length", 500)
        
        # Bersihkan query dari kata tanya dan kata kunci umum
        clean_query = query.lower()
        patterns_to_remove = [
            r"apa itu", r"siapa", r"apakah", r"mengapa", r"bagaimana", 
            r"ceritakan tentang", r"jelaskan tentang", r"apa yang", r"tahu tentang"
        ]
        
        for pattern in patterns_to_remove:
            clean_query = re.sub(pattern, "", clean_query).strip()
            
        # Periksa apakah query cocok dengan tokoh terkenal dalam dictionary
        for key, data in TOKOH_TERKENAL.items():
            if key in clean_query:
                return f"Dari Database Tokoh Terkenal:\n{data['info']}\n\nUntuk informasi lebih lanjut: {data['url']}"
        
        # Jika query terlalu pendek, gunakan query asli
        if len(clean_query) < 3:
            clean_query = query
        
        # Jika tidak ada di dictionary, coba cari di Wikipedia    
        wiki_wiki = wikipediaapi.Wikipedia(main_language)
        page = wiki_wiki.page(clean_query)
        
        if not page.exists():
            # Coba dengan bahasa alternatif jika tidak ditemukan
            wiki_wiki_alt = wikipediaapi.Wikipedia(fallback_language)
            page = wiki_wiki_alt.page(clean_query)
            
            if not page.exists():
                # Coba dengan kapitalisasi huruf pertama
                capitalized_query = clean_query.capitalize()
                page = wiki_wiki.page(capitalized_query)
                
                if not page.exists():
                    page = wiki_wiki_alt.page(capitalized_query)
                    
                    if not page.exists():
                        return f"Tidak ditemukan informasi untuk '{clean_query}' di Wikipedia."
                    else:
                        return f"Dari Wikipedia (Bahasa {fallback_language.upper()}):\n{page.summary[:summary_length]}...\n\nUntuk informasi lebih lanjut: {page.fullurl}"
                else:
                    return f"Dari Wikipedia (Bahasa {main_language.upper()}):\n{page.summary[:summary_length]}...\n\nUntuk informasi lebih lanjut: {page.fullurl}"
            else:
                return f"Dari Wikipedia (Bahasa {fallback_language.upper()}):\n{page.summary[:summary_length]}...\n\nUntuk informasi lebih lanjut: {page.fullurl}"
        
        # Ambil ringkasan halaman Wikipedia
        return f"Dari Wikipedia (Bahasa {main_language.upper()}):\n{page.summary[:summary_length]}...\n\nUntuk informasi lebih lanjut: {page.fullurl}"
    except Exception as e:
        logger.error(f"Error in wikipedia_search function: {e}")
        return f"Terjadi kesalahan saat mencari di Wikipedia: {str(e)}"

# Fungsi untuk mendaftarkan tokoh-tokoh terkenal baru secara dinamis
def register_tokoh_terkenal(key: str, nama: str, info: str, url: str):
    """
    Mendaftarkan tokoh terkenal baru ke database
    """
    TOKOH_TERKENAL[key.lower()] = {
        "nama": nama,
        "info": info,
        "url": url
    }
    logger.info(f"Added new tokoh terkenal: {nama}")
    return True

#################################################
# tools/conversion_tools.py
#################################################
import re
import logging

logger = logging.getLogger(__name__)

def konversi_satuan(query: str) -> str:
    """
    Fungsi untuk konversi satuan sederhana
    """
    try:
        query = query.lower()
        
        # Konversi panjang
        match_km_to_m = re.search(r"(\d+(?:\.\d+)?)\s*(?:km|kilometer|kilometre|kilo meter)(?:\s+(?:ke|to|dalam|in)\s+(?:m|meter))?", query)
        if match_km_to_m:
            value = float(match_km_to_m.group(1))
            result = value * 1000
            return f"{value} kilometer = {result} meter"
        
        match_m_to_km = re.search(r"(\d+(?:\.\d+)?)\s*(?:m|meter|metre)(?:\s+(?:ke|to|dalam|in)\s+(?:km|kilometer|kilometre|kilo meter))?", query)
        if match_m_to_km:
            value = float(match_m_to_km.group(1))
            result = value / 1000
            return f"{value} meter = {result} kilometer"
        
        # Konversi berat
        match_kg_to_g = re.search(r"(\d+(?:\.\d+)?)\s*(?:kg|kilogram|kilo gram|kilo)(?:\s+(?:ke|to|dalam|in)\s+(?:g|gram))?", query)
        if match_kg_to_g:
            value = float(match_kg_to_g.group(1))
            result = value * 1000
            return f"{value} kilogram = {result} gram"
        
        match_g_to_kg = re.search(r"(\d+(?:\.\d+)?)\s*(?:g|gram)(?:\s+(?:ke|to|dalam|in)\s+(?:kg|kilogram|kilo gram|kilo))?", query)
        if match_g_to_kg:
            value = float(match_g_to_kg.group(1))
            result = value / 1000
            return f"{value} gram = {result} kilogram"
        
        # Konversi suhu
        match_c_to_f = re.search(r"(\d+(?:\.\d+)?)\s*(?:c|celsius|°c)(?:\s+(?:ke|to|dalam|in)\s+(?:f|fahrenheit|°f))?", query)
        if match_c_to_f:
            value = float(match_c_to_f.group(1))
            result = (value * 9/5) + 32
            return f"{value}°C = {result}°F"
        
        match_f_to_c = re.search(r"(\d+(?:\.\d+)?)\s*(?:f|fahrenheit|°f)(?:\s+(?:ke|to|dalam|in)\s+(?:c|celsius|°c))?", query)
        if match_f_to_c:
            value = float(match_f_to_c.group(1))
            result = (value - 32) * 5/9
            return f"{value}°F = {result}°C"
        
        return "Maaf, saya tidak dapat mengenali format konversi. Contoh format yang didukung: '5 km ke m', '10 kg ke g', '30 celsius ke fahrenheit'"
    except Exception as e:
        logger.error(f"Error in konversi_satuan function: {e}")
        return f"Terjadi kesalahan saat melakukan konversi: {str(e)}"

#################################################
# tools/datetime_tools.py
#################################################
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_datetime() -> str:
    """
    Fungsi untuk mendapatkan waktu dan tanggal saat ini
    """
    try:
        now = datetime.now()
        hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][now.weekday()]
        bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                "Juli", "Agustus", "September", "Oktober", "November", "Desember"][now.month - 1]
        
        tanggal = f"{hari}, {now.day} {bulan} {now.year}"
        waktu = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
        
        return f"Saat ini adalah {tanggal}, pukul {waktu}"
    except Exception as e:
        logger.error(f"Error in get_datetime function: {e}")
        return f"Terjadi kesalahan saat mendapatkan waktu: {str(e)}"

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
        description="Gunakan ini untuk mendapatkan informasi tanggal dan waktu saat ini ketika user bertanya tentang hari ini, tanggal, jam sekarang, atau waktu saat ini."
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

#################################################
# agent/prompt_templates.py
#################################################
PREFIX_TEMPLATE = """Kamu adalah asisten AI cerdas yang membantu menjawab pertanyaan. 
Kamu berbicara dalam Bahasa Indonesia yang natural dan ramah.
Kamu memiliki akses ke tools berikut:"""

SUFFIX_TEMPLATE = """Mulai dengan memahami pertanyaan pengguna. Pikirkan dengan hati-hati tool mana yang paling tepat untuk menjawab.

INSTRUKSI PENTING:
1. Saat menggunakan tool, pastikan format Input Action benar dan gunakan format JSON yang valid.
2. Hindari membuat fakta palsu atau informasi salah tentang tokoh-tokoh terkenal.
3. Untuk pertanyaan tentang tokoh terkenal seperti Sukarno, Soekarno, Suharto, atau tokoh sejarah Indonesia lain, selalu gunakan WikipediaSearch.
4. Jangan mencoba menjawab pertanyaan tanpa menggunakan tool yang sesuai.
5. Jika pengguna bertanya "apakah kamu tahu tentang X", ini adalah pertanyaan tentang informasi faktual, bukan pertanyaan tentang apa yang kamu ketahui.

Gunakan pedoman berikut untuk memilih tool:
- Jika pertanyaan tentang fakta umum, tokoh, sejarah, atau konsep, gunakan WikipediaSearch.
- Jika pertanyaan tentang perhitungan perkalian, gunakan Perkalian.
- Jika pertanyaan tentang konten dalam dokumen, gunakan DokumenQA.
- Jika pertanyaan tentang waktu dan tanggal saat ini, gunakan DateTime.
- Jika pertanyaan tentang konversi satuan, gunakan KonversiSatuan.
- Jika pertanyaan tentang hitungan matematika (selain perkalian), gunakan Aritmatika.

Setelah mendapatkan hasil dari tool, tuliskan jawaban final dengan format yang rapi dan informatif. Berikan jawaban lengkap berdasarkan hasil tool, bukan hanya menyarankan penggunaan tool.

Pertanyaan Pengguna: {input}
{agent_scratchpad}"""

#################################################
# agent/agent_factory.py
#################################################
import logging
from typing import List, Optional
from langchain.agents import Tool, initialize_agent