"""Simple Logger"""
import logging
from nova.config import settings

logger = logging.getLogger("nova")
logger.setLevel(logging.INFO)

if not logger.handlers:
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)

def get_logger(name):
    return logging.getLogger(f"nova.{name}")
