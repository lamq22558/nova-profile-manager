"""Initial Setup and Database Initialization"""

import sys
from pathlib import Path
from nova.config import settings
from nova.core.database import Database
from nova.logger import get_logger

logger = get_logger(__name__)


def initialize_application():
    """Initialize application and database"""
    print("\n🚀 NOVA Profile Manager - Initializing...\n")

    try:
        # Create directories
        print("📁 Creating directories...")
        settings.ensure_directories()
        print("   ✅ Directories created")

        # Initialize database
        print("\n💾 Initializing database...")
        db = Database()
        print(f"   ✅ Database initialized at {settings.DB_PATH}")

        # Log configuration
        print("\n⚙️  Configuration:")
        print(f"   • App Version: {settings.APP_VERSION}")
        print(f"   • Base Directory: {settings.BASE_DIR}")
        print(f"   • Data Directory: {settings.DATA_DIR}")
        print(f"   • Log Directory: {settings.LOG_DIR}")
        print(f"   • API Port: {settings.API_PORT}")
        print(f"   • Log Level: {settings.LOG_LEVEL}")

        print("\n✨ Initialization Complete!")
        print("\nNext steps:")
        print("   1. Configure .env file if needed")
        print("   2. Run: python main.py (for GUI)")
        print("   3. Or: python -m nova.api.server (for API)")
        print("   4. Or: python -m nova.cli --help (for CLI)\n")

        return True
    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        logger.error(f"Initialization failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = initialize_application()
    sys.exit(0 if success else 1)
