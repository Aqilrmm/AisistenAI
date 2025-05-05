# tools/joke_fetcher.py
import logging
import requests

logger = logging.getLogger(__name__)

def fetch_random_joke(_: str = "") -> str:
    """
    Mengambil lelucon acak dari Official Joke API.
    Parameter input tidak digunakan tapi diterima agar kompatibel dengan pemanggilan tool.
    """
    try:
        url = "https://official-joke-api.appspot.com/random_joke"
        response = requests.get(url)
        data = response.json()

        setup = data.get("setup", "")
        punchline = data.get("punchline", "")

        if not setup or not punchline:
            return "Gagal mengambil lelucon."

        return f"{setup}\n{punchline}"
    except Exception as e:
        logger.error(f"Error in fetch_random_joke: {e}")
        return f"Terjadi kesalahan: {str(e)}"
