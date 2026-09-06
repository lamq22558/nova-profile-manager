"""Database - Simple JSON Storage"""
import json
import threading
from pathlib import Path
from nova.config import settings
from nova.logger import get_logger

logger = get_logger(__name__)

class Database:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.db_path = settings.DB_PATH
        self._lock = threading.RLock()
        self.load()
    
    def load(self):
        with self._lock:
            if self.db_path.exists():
                try:
                    with open(self.db_path, 'r', encoding='utf-8') as f:
                        self._data = json.load(f)
                except:
                    self._data = self._default_db()
            else:
                self._data = self._default_db()
                self.save()
    
    def save(self):
        with self._lock:
            try:
                self.db_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.db_path, 'w', encoding='utf-8') as f:
                    json.dump(self._data, f, ensure_ascii=False, indent=2)
                return True
            except Exception as e:
                logger.error(f"Save failed: {e}")
                return False
    
    def get(self, key, default=None):
        return self._data.get(key, default)
    
    def set(self, key, value):
        self._data[key] = value
        return self.save()
    
    @staticmethod
    def _default_db():
        return {
            "profiles": [],
            "proxies": [],
            "groups": ["Default Group", "Group 1", "Group 2"],
            "settings": {"port": 54345}
        }

db = Database()
