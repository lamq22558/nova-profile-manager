"""Logging Configuration"""

import logging
import logging.handlers
from pathlib import Path
from nova.config import settings

# Ensure log directory exists
settings.LOG_DIR.mkdir(parents=True, exist_ok=True)

# Create logger
logger = logging.getLogger("nova")
logger.setLevel(getattr(logging, settings.LOG_LEVEL))

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
console_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(console_formatter)

# File handler with rotation
file_handler = logging.handlers.RotatingFileHandler(
    settings.LOG_PATH,
    maxBytes=settings.LOG_MAX_SIZE,
    backupCount=settings.LOG_BACKUP_COUNT,
    encoding="utf-8"
)
file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Get or create a logger instance"""
    return logging.getLogger(f"nova.{name}")
