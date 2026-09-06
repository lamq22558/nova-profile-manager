"""Fingerprint Generation Service"""

import random
from typing import Dict, Any
from nova.constants import DEFAULT_USER_AGENTS, DEFAULT_SCREEN_SIZES
from nova.logger import get_logger

logger = get_logger(__name__)


class FingerprintService:
    """Service for generating realistic browser fingerprints"""

    @staticmethod
    def generate_fingerprint() -> Dict[str, Any]:
        """Generate complete fingerprint configuration"""
        return {
            "user_agent": FingerprintService.generate_user_agent(),
            "screen_size": FingerprintService.generate_screen_size(),
            "canvas": FingerprintService.generate_canvas_fingerprint(),
            "webgl": FingerprintService.generate_webgl_fingerprint(),
            "timezone": FingerprintService.generate_timezone(),
            "language": FingerprintService.generate_language(),
            "device": FingerprintService.generate_device(),
            "plugins": FingerprintService.generate_plugins(),
        }

    @staticmethod
    def generate_user_agent() -> str:
        """Generate random user agent"""
        return random.choice(DEFAULT_USER_AGENTS)

    @staticmethod
    def generate_screen_size() -> str:
        """Generate random screen size"""
        return random.choice(DEFAULT_SCREEN_SIZES)

    @staticmethod
    def generate_canvas_fingerprint() -> Dict[str, Any]:
        """Generate canvas fingerprint data"""
        return {
            "enabled": True,
            "randomize": True,
            "noise_level": random.randint(1, 5),
        }

    @staticmethod
    def generate_webgl_fingerprint() -> Dict[str, Any]:
        """Generate WebGL fingerprint data"""
        return {
            "enabled": True,
            "randomize": True,
            "vendor": random.choice(["Intel", "NVIDIA", "AMD"]),
            "renderer": random.choice(["HD Graphics", "GeForce", "Radeon"]),
        }

    @staticmethod
    def generate_timezone() -> str:
        """Generate timezone"""
        timezones = [
            "America/New_York",
            "America/Los_Angeles",
            "America/Chicago",
            "Europe/London",
            "Europe/Berlin",
            "Asia/Tokyo",
            "Asia/Shanghai",
            "Australia/Sydney",
        ]
        return random.choice(timezones)

    @staticmethod
    def generate_language() -> str:
        """Generate language"""
        languages = ["en-US", "en-GB", "de-DE", "fr-FR", "ja-JP", "zh-CN"]
        return random.choice(languages)

    @staticmethod
    def generate_device() -> Dict[str, Any]:
        """Generate device fingerprint"""
        return {
            "type": "Desktop",
            "os": random.choice(["Windows", "macOS", "Linux"]),
            "cpu_cores": random.choice([2, 4, 6, 8, 16]),
            "memory_mb": random.choice([4096, 8192, 16384, 32768]),
        }

    @staticmethod
    def generate_plugins() -> list:
        """Generate browser plugins list"""
        return [
            {"name": "Chrome PDF Plugin", "description": "Portable Document Format"},
            {"name": "Chrome PDF Viewer", "description": ""},
            {"name": "Native Client Executable", "description": ""},
        ]
