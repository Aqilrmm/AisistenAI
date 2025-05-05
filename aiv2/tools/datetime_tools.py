#################################################
# tools/datetime_tools.py
#################################################
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_datetime(_: str = "") -> str:
    """
    Fungsi untuk mendapatkan waktu dan tanggal saat ini.
    Argumen diabaikan karena tidak dibutuhkan.
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
print(get_datetime())