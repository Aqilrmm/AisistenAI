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
