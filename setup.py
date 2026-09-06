#!/usr/bin/env python
"""NOVA Profile Manager Setup and Installation"""

from pathlib import Path
import subprocess
import sys


def run_command(cmd, description):
    """Run command and report status"""
    print(f"\n📦 {description}...")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0


def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║    🚀 NOVA PROFILE MANAGER - Setup & Installation         ║
║         Enterprise Antidetect Browser Suite v9.0          ║
╚════════════════════════════════════════════════════════════╝
    """)

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return 1

    print("✓ Python version OK")

    # Create virtual environment
    venv_dir = Path("venv")
    if not venv_dir.exists():
        if not run_command(f"{sys.executable} -m venv venv", "Creating virtual environment"):
            return 1
    else:
        print("✓ Virtual environment already exists")

    # Install dependencies
    if sys.platform == "win32":
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"

    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        return 1

    # Initialize database
    if not run_command(f"{python_cmd} -m nova.core.setup", "Initializing database"):
        return 1

    print("""
✨ Setup Complete! ✨

Next steps:
  1. Activate virtual environment:
  """)
    if sys.platform == "win32":
        print("     .\\venv\\Scripts\\activate")
    else:
        print("     source venv/bin/activate")
    
    print("""
  2. Run NOVA GUI:
     python main.py

  3. Or start API server:
     python -m nova.api.server

  4. Or use CLI:
     python -m nova.cli --help

📚 Documentation: https://github.com/lamq22558/nova-profile-manager
💬 Support: Create an issue on GitHub
    """)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
