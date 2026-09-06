#!/usr/bin/env python
"""Build standalone EXE using PyInstaller"""

import subprocess
import sys
from pathlib import Path

def build_exe():
    """Build executable"""
    print("🔨 Building NOVA Profile Manager EXE...")
    
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=NOVA-Profile-Manager",
        "--icon=nova.ico",
        "--add-data=nova:nova",
        "--collect-all=customtkinter",
        "--collect-all=fastapi",
        "--collect-all=uvicorn",
        "main.py"
    ]
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    
    if result.returncode == 0:
        exe_path = Path(__file__).parent / "dist" / "NOVA-Profile-Manager.exe"
        print(f"\n✅ Build successful!")
        print(f"📦 EXE location: {exe_path}")
        print(f"📥 Copy to any folder and run!")
    else:
        print(f"\n❌ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
