"""Proxy Management Service"""

import urllib.request
import json
import threading
from typing import List, Dict, Any, Optional, Tuple
from nova.core.database import Database
from nova.core.validators import ProxyValidator
from nova.models.proxy import Proxy
from nova.logger import get_logger
from nova.config import settings
from nova.constants import PROXY_LIVE, PROXY_DEAD, PROXY_CHECKING
from datetime import datetime
import time

logger = get_logger(__name__)


class ProxyService:
    """Service for managing proxies and proxy health checking"""

    def __init__(self):
        self.db = Database()
        self.validator = ProxyValidator()
        self._health_check_threads = {}

    def add_proxy(
        self,
        proxy: str,
        name: str = "",
        provider: str = "",
        country: str = "",
        tags: List[str] = None,
        notes: str = "",
    ) -> Tuple[bool, Optional[str]]:
        """Add new proxy"""
        # Validate proxy format
        is_valid, error = self.validator.validate_proxy_format(proxy)
        if not is_valid:
            logger.warning(f"Invalid proxy format: {error}")
            return False, error

        # Check if proxy already exists
        if self._proxy_exists(proxy):
            return False, "Proxy already exists in database"

        try:
            proxy_obj = Proxy(
                proxy=proxy,
                name=name or proxy,
                provider=provider,
                country=country,
                tags=tags or [],
                notes=notes,
            )

            if self.db.add_proxy(proxy):
                logger.info(f"Proxy added: {proxy}")
                return True, None
            else:
                return False, "Failed to save proxy to database"
        except Exception as e:
            logger.error(f"Failed to add proxy: {e}", exc_info=True)
            return False, str(e)

    def get_all_proxies(self) -> List[str]:
        """Get all proxies"""
        return self.db.get_proxies()

    def delete_proxy(self, proxy: str) -> Tuple[bool, Optional[str]]:
        """Delete proxy"""
        try:
            if self.db.delete_proxy(proxy):
                logger.info(f"Proxy deleted: {proxy}")
                return True, None
            else:
                return False, "Proxy not found"
        except Exception as e:
            logger.error(f"Failed to delete proxy: {e}", exc_info=True)
            return False, str(e)

    def check_proxy_health(
        self, proxy: str, timeout: int = None
    ) -> Tuple[bool, str]:
        """Check if proxy is alive
        
        Returns: (is_alive, status_message)
        """
        if timeout is None:
            timeout = settings.PROXY_TIMEOUT

        try:
            ip, port, user, pwd = self.validator.parse_proxy(proxy)
            proxy_url = f"http://{ip}:{port}"

            # Create proxy handler
            if user and pwd:
                import base64

                cred = f"{user}:{pwd}".encode("utf-8")
                auth_header = base64.b64encode(cred).decode()
                proxy_handler = urllib.request.ProxyHandler({"http": proxy_url})
                # Note: Full auth handling would require custom opener
            else:
                proxy_handler = urllib.request.ProxyHandler({"http": proxy_url})

            opener = urllib.request.build_opener(proxy_handler)
            req = urllib.request.Request(
                "http://ip-api.com/json/?fields=status,country,countryCode,query",
                headers={"User-Agent": "Mozilla/5.0"},
            )

            with opener.open(req, timeout=timeout) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                if res_data.get("status") == "success":
                    ip_addr = res_data.get("query")
                    country = res_data.get("countryCode", "XX")
                    return True, f"Live: {ip_addr} ({country})"
        except Exception as e:
            logger.debug(f"Proxy health check failed for {proxy}: {e}")

        return False, "Dead / Error"

    def check_all_proxies_health(self, concurrent: bool = True):
        """Check health of all proxies"""
        proxies = self.get_all_proxies()
        logger.info(f"Starting health check for {len(proxies)} proxies")

        if concurrent:
            threads = []
            for proxy in proxies:
                thread = threading.Thread(
                    target=self.check_proxy_health, args=(proxy,), daemon=True
                )
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join(timeout=settings.PROXY_TIMEOUT + 5)
        else:
            for proxy in proxies:
                self.check_proxy_health(proxy)

        logger.info("Proxy health check completed")

    def _proxy_exists(self, proxy: str) -> bool:
        """Check if proxy already exists"""
        return proxy in self.get_all_proxies()

    def get_statistics(self) -> Dict[str, Any]:
        """Get proxy statistics"""
        proxies = self.get_all_proxies()
        return {"total_proxies": len(proxies), "proxies": proxies}
