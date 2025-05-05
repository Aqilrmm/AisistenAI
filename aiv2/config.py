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
LLM_TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", 0))
LLM_STREAMING = os.environ.get("LLM_STREAMING", "False").lower() == "false"

# Daftar tools yang diaktifkan (untuk dynamic loading)
ENABLED_TOOLS = os.environ.get("ENABLED_TOOLS", "Perkalian,WikipediaSearch,DateTime,KonversiSatuan,Aritmatika,JokeFetcher").split(",")

# Konfigurasi dinamis untuk setiap tool
TOOL_CONFIG = {
    "WikipediaSearch": {
        "language": os.environ.get("WIKIPEDIA_LANGUAGE", "id"),
        "fallback_language": os.environ.get("WIKIPEDIA_FALLBACK_LANGUAGE", "en"),
        "summary_length": int(os.environ.get("WIKIPEDIA_SUMMARY_LENGTH", 500))
    }
}