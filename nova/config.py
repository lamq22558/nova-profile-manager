"""Configuration Management"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

class Settings:
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "nova_profiles_data"
    BIN_DIR = BASE_DIR / "nova_browser_bin"
    LOG_DIR = BASE_DIR / "logs"
    DB_PATH = BASE_DIR / "nova_database.json"
    LOG_PATH = LOG_DIR / "nova_system.log"
    
    API_HOST = os.getenv("NOVA_API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("NOVA_API_PORT", "54345"))
    BROWSER_TIMEOUT = int(os.getenv("NOVA_BROWSER_TIMEOUT", "30"))
    LOG_LEVEL = os.getenv("NOVA_LOG_LEVEL", "INFO")
    
    def ensure_directories(self):
        for path in [self.DATA_DIR, self.BIN_DIR, self.LOG_DIR]:
            path.mkdir(parents=True, exist_ok=True)

settings = Settings()
settings.ensure_directories()
