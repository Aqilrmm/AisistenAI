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
