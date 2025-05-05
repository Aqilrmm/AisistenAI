import re
import logging
import wikipedia
from ..config import TOOL_CONFIG

logger = logging.getLogger(__name__)

# Database tokoh terkenal Indonesia
def wikipedia_search(query: str) -> str:
    """
    Fungsi untuk mencari informasi di Wikipedia dengan penanganan khusus untuk tokoh terkenal
    """
    try:
        # Mengambil konfigurasi dari TOOL_CONFIG
        config = TOOL_CONFIG.get("WikipediaSearch", {})
        main_language = config.get("language", "id")
        fallback_language = config.get("fallback_language", "en")
        summary_length = config.get("summary_length", 500)
        
        # Membersihkan query dari kata tanya dan kata kunci umum
        clean_query = query.lower()
        patterns_to_remove = [
            r"apa itu", r"siapa", r"apakah", r"mengapa", r"bagaimana", 
            r"ceritakan tentang", r"jelaskan tentang", r"apa yang", r"tahu tentang"
        ]
        
        for pattern in patterns_to_remove:
            clean_query = re.sub(pattern, "", clean_query).strip()
            
        # Jika query terlalu pendek, gunakan query asli
        if len(clean_query) < 3:
            clean_query = query
        
        # Gunakan wikipedia untuk pencarian halaman
        wiki_wiki = wikipedia.Wikipedia(main_language)
        page = wiki_wiki.page(clean_query)

        # Jika halaman tidak ada, coba bahasa fallback
        if not page.exists():
            wiki_wiki_alt = wikipedia.Wikipedia(fallback_language)
            page = wiki_wiki_alt.page(clean_query)
        
        # Jika halaman masih tidak ditemukan, coba kapitalisasi pertama
        if not page.exists():
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
        
        # Jika halaman ditemukan, ambil ringkasan dan tampilkan
        return f"Dari Wikipedia (Bahasa {main_language.upper()}):\n{page.summary[:summary_length]}...\n\nUntuk informasi lebih lanjut: {page.fullurl}"

    except wikipedia.exceptions.RedirectError as e:
        logger.error(f"RedirectError: {e}")
        return f"Halaman yang Anda cari telah dialihkan ke halaman lain."
    except wikipedia.exceptions.DisambiguationError as e:
        logger.error(f"DisambiguationError: {e}")
        return f"Page yang Anda cari mengarah pada halaman disambiguasi, coba masukkan query lebih spesifik."
    except Exception as e:
        logger.error(f"Error in wikipedia_search function: {e}")
        return f"Terjadi kesalahan saat mencari di Wikipedia: {str(e)}"
def my_new_function(query: str) -> str:
       """
       Deskripsi fungsi tool baru
       """
       try:
           # Implementasi tool
           result = "Hasil dari tool baru"
           return result
       except Exception as e:
           logger.error(f"Error in my_new_function: {e}")
           return f"Terjadi kesalahan: {str(e)}"