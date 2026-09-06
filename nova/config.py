"""Global Configuration Management"""

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load .env file
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file)


class Settings(BaseSettings):
    """Application Settings"""

    # Application
    APP_NAME: str = "NOVA Profile Manager"
    APP_VERSION: str = "9.0.0"
    DEBUG: bool = os.getenv("NOVA_API_DEBUG", "false").lower() == "true"

    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "nova_profiles_data"
    BIN_DIR: Path = BASE_DIR / "nova_browser_bin"
    LOG_DIR: Path = BASE_DIR / "logs"
    DB_PATH: Path = BASE_DIR / "nova_database.json"
    LOG_PATH: Path = LOG_DIR / "nova_system.log"

    # Browser
    CHROMIUM_DOWNLOAD_URL: str = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win_x64%2F1130000%2Fchrome-win.zip?alt=media"
    BROWSER_TIMEOUT: int = int(os.getenv("NOVA_BROWSER_TIMEOUT", "30"))
    BROWSER_MAX_INSTANCES: int = int(os.getenv("NOVA_BROWSER_MAX_INSTANCES", "10"))
    BROWSER_DEBUG_PORT_BASE: int = 9222

    # Proxy
    PROXY_TIMEOUT: int = int(os.getenv("NOVA_PROXY_TIMEOUT", "10"))
    PROXY_CHECK_INTERVAL: int = int(os.getenv("NOVA_PROXY_CHECK_INTERVAL", "300"))
    PROXY_RETRY_COUNT: int = int(os.getenv("NOVA_PROXY_RETRY_COUNT", "3"))
    PROXY_BRIDGE_HOST: str = "127.0.0.1"

    # API
    API_HOST: str = os.getenv("NOVA_API_HOST", "127.0.0.1")
    API_PORT: int = int(os.getenv("NOVA_API_PORT", "54345"))
    API_VERSION: str = "v1"

    # Database
    DB_BACKUP_ENABLED: bool = os.getenv("NOVA_DB_BACKUP_ENABLED", "true").lower() == "true"
    DB_BACKUP_INTERVAL: int = int(os.getenv("NOVA_DB_BACKUP_INTERVAL", "3600"))
    DB_ENCRYPTION_KEY: str = os.getenv("NOVA_DB_ENCRYPTION_KEY", "")

    # Logging
    LOG_LEVEL: str = os.getenv("NOVA_LOG_LEVEL", "INFO")
    LOG_MAX_SIZE: int = int(os.getenv("NOVA_LOG_MAX_SIZE", "10485760"))  # 10MB
    LOG_BACKUP_COUNT: int = int(os.getenv("NOVA_LOG_BACKUP_COUNT", "5"))

    # Cloud Integration
    CLOUD_PROVIDER: str = os.getenv("NOVA_CLOUD_PROVIDER", "")
    CLOUD_API_KEY: str = os.getenv("NOVA_CLOUD_API_KEY", "")
    CLOUD_BUCKET: str = os.getenv("NOVA_CLOUD_BUCKET", "")

    # Notifications
    SLACK_WEBHOOK: str = os.getenv("NOVA_SLACK_WEBHOOK", "")
    TELEGRAM_TOKEN: str = os.getenv("NOVA_TELEGRAM_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("NOVA_TELEGRAM_CHAT_ID", "")
    EMAIL_ENABLED: bool = os.getenv("NOVA_EMAIL_ENABLED", "false").lower() == "true"
    EMAIL_SMTP_HOST: str = os.getenv("NOVA_EMAIL_SMTP_HOST", "")
    EMAIL_SMTP_PORT: int = int(os.getenv("NOVA_EMAIL_SMTP_PORT", "587"))
    EMAIL_SENDER: str = os.getenv("NOVA_EMAIL_SENDER", "")

    class Config:
        env_file = ".env"
        case_sensitive = True

    def ensure_directories(self):
        """Create necessary directories"""
        for path in [self.DATA_DIR, self.BIN_DIR, self.LOG_DIR]:
            path.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
settings.ensure_directories()
