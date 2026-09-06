"""Simple UI - Welcome Screen"""
try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except:
    CTK_AVAILABLE = False

if CTK_AVAILABLE:
    class NovaProfileStudio(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("NOVA Profile Manager v9.0")
            self.geometry("600x400")
            
            # Main frame
            frame = ctk.CTkFrame(self)
            frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Title
            title = ctk.CTkLabel(
                frame,
                text="🚀 NOVA PROFILE MANAGER",
                font=("Arial", 24, "bold")
            )
            title.pack(pady=20)
            
            # Info
            info = ctk.CTkLabel(
                frame,
                text="Enterprise Antidetect Browser Suite v9.0\n\n"
                     "Features:\n"
                     "✓ Profile Management\n"
                     "✓ Proxy Management\n"
                     "✓ Browser Automation\n"
                     "✓ Fingerprint Customization\n"
                     "✓ REST API",
                font=("Arial", 12),
                justify="left"
            )
            info.pack(pady=20)
            
            # Buttons
            btn_frame = ctk.CTkFrame(frame)
            btn_frame.pack(pady=20)
            
            ctk.CTkButton(
                btn_frame,
                text="📖 Documentation",
                command=self.open_docs
            ).pack(pady=10)
            
            ctk.CTkButton(
                btn_frame,
                text="🔌 Start API Server",
                command=self.start_api
            ).pack(pady=10)
            
            ctk.CTkButton(
                btn_frame,
                text="❌ Exit",
                command=self.quit
            ).pack(pady=10)
        
        def open_docs(self):
            import webbrowser
            webbrowser.open("https://github.com/lamq22558/nova-profile-manager")
        
        def start_api(self):
            print("Starting API server...")
            try:
                from nova.api.server import create_app
                import uvicorn
                from nova.config import settings
                
                app = create_app()
                print(f"API available at http://{settings.API_HOST}:{settings.API_PORT}")
                uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
            except Exception as e:
                print(f"Error: {e}")
else:
    class NovaProfileStudio:
        def __init__(self):
            print("CustomTkinter not available. Starting API server instead...")
        
        def mainloop(self):
            from nova.api.server import create_app
            import uvicorn
            from nova.config import settings
            
            app = create_app()
            print(f"\n🚀 API Server Running at http://{settings.API_HOST}:{settings.API_PORT}")
            print(f"📖 Docs: http://{settings.API_HOST}:{settings.API_PORT}/docs\n")
            uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
