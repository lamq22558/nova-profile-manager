"""Input Validators for Profiles and Proxies"""

import re
from typing import Tuple, Optional
from nova.logger import get_logger

logger = get_logger(__name__)


class ProfileValidator:
    """Validate profile data"""

    @staticmethod
    def validate_name(name: str) -> Tuple[bool, Optional[str]]:
        """Validate profile name"""
        if not name or not isinstance(name, str):
            return False, "Profile name must be a non-empty string"
        if len(name) > 255:
            return False, "Profile name must be less than 255 characters"
        if not re.match(r"^[a-zA-Z0-9_\-\u0080-\uFFFF ]+$", name):
            return False, "Profile name contains invalid characters"
        return True, None

    @staticmethod
    def validate_screen_size(size: str) -> Tuple[bool, Optional[str]]:
        """Validate screen resolution format"""
        if not size or not isinstance(size, str):
            return False, "Screen size must be a non-empty string"
        if not re.match(r"^\d+,\d+$", size):
            return False, "Screen size must be in format: WIDTH,HEIGHT"
        width, height = map(int, size.split(","))
        if width < 640 or width > 3840 or height < 480 or height > 2160:
            return False, "Screen size out of valid range (640x480 to 3840x2160)"
        return True, None

    @staticmethod
    def validate_url(url: str) -> Tuple[bool, Optional[str]]:
        """Validate URL"""
        if not url or not isinstance(url, str):
            return False, "URL must be a non-empty string"
        url_pattern = re.compile(
            r"^https?://"
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)*[A-Z]{2,6}\.?|localhost|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        if not url_pattern.match(url):
            return False, "Invalid URL format"
        return True, None

    @staticmethod
    def validate_profile_id(profile_id: str) -> Tuple[bool, Optional[str]]:
        """Validate profile ID format"""
        if not profile_id or not isinstance(profile_id, str):
            return False, "Profile ID must be a non-empty string"
        if not re.match(r"^nova_\d+(_\d+)?$", profile_id):
            return False, "Invalid profile ID format"
        return True, None


class ProxyValidator:
    """Validate proxy data"""

    @staticmethod
    def validate_proxy_format(proxy: str) -> Tuple[bool, Optional[str]]:
        """Validate proxy string format
        
        Supported formats:
        - IP:Port
        - IP:Port:User:Pass
        - User:Pass@IP:Port
        - http://IP:Port
        - http://User:Pass@IP:Port
        """
        if not proxy or not isinstance(proxy, str):
            return False, "Proxy must be a non-empty string"

        # Remove protocol if present
        clean = proxy.replace("http://", "").replace("https://", "").strip()

        # Check for credentials
        if "@" in clean:
            cred_part, host_part = clean.rsplit("@", 1)
            # Validate credentials
            if ":" not in cred_part:
                return False, "Credentials must be in format: user:pass"
            user, pwd = cred_part.split(":", 1)
            if not user or not pwd:
                return False, "Username and password cannot be empty"
            # Validate host
            if ":" not in host_part:
                return False, "Host must include port: ip:port"
        else:
            # Check if it's IP:Port or IP:Port:User:Pass
            if clean.count(":") < 1:
                return False, "Proxy must include port (format: ip:port)"

        # Validate IP and Port
        parts = clean.split(":")
        ip = parts[0]
        try:
            port = int(parts[1])
            if port < 1 or port > 65535:
                return False, "Port must be between 1 and 65535"
        except ValueError:
            return False, "Invalid port number"

        # Validate IP address
        if not ProxyValidator._is_valid_ip(ip):
            return False, "Invalid IP address"

        return True, None

    @staticmethod
    def _is_valid_ip(ip: str) -> bool:
        """Check if IP address is valid"""
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        for part in parts:
            try:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            except ValueError:
                return False
        return True

    @staticmethod
    def parse_proxy(proxy_str: str) -> Tuple[str, str, str, str]:
        """Parse proxy string into components
        
        Returns: (ip, port, username, password)
        """
        clean = proxy_str.replace("http://", "").replace("https://", "").strip()
        user, pwd, ip, port = "", "", "", ""

        if "@" in clean:
            cred, host = clean.split("@", 1)
            user, pwd = cred.split(":", 1)
            ip, port = host.split(":", 1)
        elif clean.count(":") == 3:
            ip, port, user, pwd = clean.split(":")
        elif clean.count(":") == 1:
            ip, port = clean.split(":")

        return ip, port, user, pwd
