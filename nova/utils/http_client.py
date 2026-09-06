"""HTTP Client with Retry Logic"""

import requests
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from nova.logger import get_logger

logger = get_logger(__name__)


class HTTPClient:
    """HTTP Client with built-in retry logic and error handling"""

    def __init__(
        self,
        timeout: int = 30,
        retries: int = 3,
        backoff_factor: float = 0.5,
    ):
        self.session = requests.Session()
        self.timeout = timeout

        # Configure retry strategy
        retry_strategy = Retry(
            total=retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
            backoff_factor=backoff_factor,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(
        self, url: str, headers: Optional[Dict[str, str]] = None, **kwargs
    ) -> Optional[requests.Response]:
        """GET request"""
        try:
            return self.session.get(url, headers=headers, timeout=self.timeout, **kwargs)
        except requests.RequestException as e:
            logger.error(f"GET request failed: {url} - {e}")
            return None

    def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Optional[requests.Response]:
        """POST request"""
        try:
            return self.session.post(
                url, data=data, json=json, headers=headers, timeout=self.timeout, **kwargs
            )
        except requests.RequestException as e:
            logger.error(f"POST request failed: {url} - {e}")
            return None

    def close(self):
        """Close session"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
