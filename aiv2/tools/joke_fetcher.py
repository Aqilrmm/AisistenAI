# tools/joke_fetcher.py
import logging
import requests

logger = logging.getLogger(__name__)

def fetch_random_joke(none: str = None) -> dict:
    """
    Mengambil lelucon acak dari API dan mengembalikannya dalam format dictionary.
    """
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        response.raise_for_status()
        joke = response.json()
        return joke  # Kembalikan setup dan punchline sebagai dictionary
    except Exception as e:
        logger.error(f"Error fetching joke: {e}")
        return {"setup": "Terjadi kesalahan", "punchline": f"Kesalahan: {e}"}