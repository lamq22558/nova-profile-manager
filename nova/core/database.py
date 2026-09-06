"""Database Operations and Management"""

import json
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
from nova.config import settings
from nova.logger import get_logger

logger = get_logger(__name__)


class Database:
    """Database singleton for managing application data"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.db_path = settings.DB_PATH
        self.backup_path = settings.DB_PATH.parent / f"{settings.DB_PATH.name}.backup"
        self._lock = threading.RLock()
        self._data = None
        self._initialized = True
        self.load()

    def load(self) -> Dict[str, Any]:
        """Load database from file"""
        with self._lock:
            if self.db_path.exists():
                try:
                    with open(self.db_path, "r", encoding="utf-8") as f:
                        self._data = json.load(f)
                    logger.info(f"Database loaded from {self.db_path}")
                except Exception as e:
                    logger.error(f"Failed to load database: {e}")
                    self._data = self._get_default_db()
            else:
                self._data = self._get_default_db()
                self.save()
        return self._data

    def save(self) -> bool:
        """Save database to file"""
        with self._lock:
            try:
                # Create backup
                if self.db_path.exists():
                    with open(self.db_path, "r", encoding="utf-8") as f:
                        backup_data = json.load(f)
                    with open(self.backup_path, "w", encoding="utf-8") as f:
                        json.dump(backup_data, f, ensure_ascii=False, indent=2)

                # Save current data
                temp_path = self.db_path.parent / f"{self.db_path.name}.tmp"
                with open(temp_path, "w", encoding="utf-8") as f:
                    json.dump(self._data, f, ensure_ascii=False, indent=2)
                temp_path.replace(self.db_path)
                logger.info(f"Database saved to {self.db_path}")
                return True
            except Exception as e:
                logger.error(f"Failed to save database: {e}")
                return False

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from database"""
        with self._lock:
            return self._data.get(key, default)

    def set(self, key: str, value: Any) -> bool:
        """Set value in database"""
        with self._lock:
            self._data[key] = value
            return self.save()

    def get_profiles(self) -> List[Dict[str, Any]]:
        """Get all profiles"""
        return self.get("profiles", [])

    def get_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """Get profile by ID"""
        profiles = self.get_profiles()
        for profile in profiles:
            if profile.get("id") == profile_id:
                return profile
        return None

    def add_profile(self, profile: Dict[str, Any]) -> bool:
        """Add new profile"""
        profiles = self.get_profiles()
        profiles.append(profile)
        return self.set("profiles", profiles)

    def update_profile(self, profile_id: str, updates: Dict[str, Any]) -> bool:
        """Update profile"""
        profiles = self.get_profiles()
        for i, profile in enumerate(profiles):
            if profile.get("id") == profile_id:
                profiles[i].update(updates)
                return self.set("profiles", profiles)
        return False

    def delete_profile(self, profile_id: str) -> bool:
        """Delete profile"""
        profiles = self.get_profiles()
        filtered = [p for p in profiles if p.get("id") != profile_id]
        if len(filtered) < len(profiles):
            return self.set("profiles", filtered)
        return False

    def get_proxies(self) -> List[str]:
        """Get all proxies"""
        return self.get("proxies", [])

    def add_proxy(self, proxy: str) -> bool:
        """Add new proxy"""
        proxies = self.get_proxies()
        if proxy not in proxies:
            proxies.append(proxy)
            return self.set("proxies", proxies)
        return False

    def delete_proxy(self, proxy: str) -> bool:
        """Delete proxy"""
        proxies = self.get_proxies()
        filtered = [p for p in proxies if p != proxy]
        if len(filtered) < len(proxies):
            return self.set("proxies", filtered)
        return False

    def get_groups(self) -> List[str]:
        """Get all groups"""
        return self.get("groups", [])

    def add_group(self, group: str) -> bool:
        """Add new group"""
        groups = self.get_groups()
        if group not in groups:
            groups.append(group)
            return self.set("groups", groups)
        return False

    def delete_group(self, group: str) -> bool:
        """Delete group"""
        groups = self.get_groups()
        filtered = [g for g in groups if g != group]
        if len(filtered) < len(groups):
            return self.set("groups", filtered)
        return False

    def export_data(self, file_path: Path) -> bool:
        """Export database to file"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
            logger.info(f"Database exported to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export database: {e}")
            return False

    def import_data(self, file_path: Path, merge: bool = True) -> bool:
        """Import database from file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                imported_data = json.load(f)

            if not merge:
                self._data = imported_data
            else:
                # Merge profiles
                existing_ids = {p.get("id") for p in self._data.get("profiles", [])}
                for profile in imported_data.get("profiles", []):
                    if profile.get("id") not in existing_ids:
                        self._data.setdefault("profiles", []).append(profile)

                # Merge proxies
                self._data.setdefault("proxies", []).extend(
                    [p for p in imported_data.get("proxies", []) if p not in self._data.get("proxies", [])]
                )

                # Merge groups
                for group in imported_data.get("groups", []):
                    if group not in self._data.get("groups", []):
                        self._data.setdefault("groups", []).append(group)

            self.save()
            logger.info(f"Database imported from {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to import database: {e}")
            return False

    @staticmethod
    def _get_default_db() -> Dict[str, Any]:
        """Get default database structure"""
        from nova.constants import DEFAULT_GROUPS

        return {
            "groups": DEFAULT_GROUPS,
            "profiles": [],
            "proxies": [],
            "settings": {"port": 54345, "sheets": ["FB_CAMPAIGN"]},
            "metadata": {"version": "9.0.0", "created_at": datetime.now().isoformat()},
        }
