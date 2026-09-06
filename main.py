"""NOVA Profile Manager - Main Entry Point"""

import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    # Try GUI first
    from nova.ui.main_window import NovaProfileStudio
    import customtkinter as ctk
    
    if __name__ == "__main__":
        app = NovaProfileStudio()
        app.mainloop()
except ImportError as e:
    print(f"Error loading GUI: {e}")
    print("\nTrying API server instead...")
    try:
        from nova.api.server import create_app
        import uvicorn
        from nova.config import settings
        
        app = create_app()
        uvicorn.run(
            app,
            host=settings.API_HOST,
            port=settings.API_PORT,
            log_level="info"
        )
    except Exception as e2:
        print(f"Failed to start: {e2}")
        sys.exit(1)
