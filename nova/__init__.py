"""NOVA Profile Manager - Enterprise Antidetect Suite v9.0"""

__version__ = "9.0.0"
__author__ = "NOVA Development Team"
__email__ = "dev@novanet.com"

from nova.config import settings
from nova.logger import get_logger

logger = get_logger(__name__)

__all__ = ["settings", "logger", "__version__"]
