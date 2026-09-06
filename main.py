#!/usr/bin/env python
"""NOVA Profile Manager - Main Entry Point"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from nova.config import settings
from nova.logger import get_logger
from nova.core.setup import initialize_application

logger = get_logger(__name__)


def main():
    """Main entry point"""
    try:
        # Initialize application
        if not initialize_application():
            return 1

        # Start GUI
        logger.info("Starting NOVA GUI Application...")
        
        try:
            from nova.ui.main_window import NovaProfileStudio
            import customtkinter as ctk
            
            app = NovaProfileStudio()
            app.mainloop()
        except ImportError:
            logger.warning("CustomTkinter not available, starting API server instead...")
            from nova.api.server import create_app
            import uvicorn
            
            app = create_app()
            uvicorn.run(
                app,
                host=settings.API_HOST,
                port=settings.API_PORT,
                log_level=settings.LOG_LEVEL.lower(),
            )
        
        return 0
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
