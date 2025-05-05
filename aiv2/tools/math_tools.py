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
