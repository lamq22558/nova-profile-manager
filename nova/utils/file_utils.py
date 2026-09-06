"""File Utilities"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from nova.logger import get_logger

logger = get_logger(__name__)


class FileUtils:
    """File operation utilities"""

    @staticmethod
    def read_json(file_path: Path) -> Optional[Dict[str, Any]]:
        """Read JSON file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read JSON file {file_path}: {e}")
            return None

    @staticmethod
    def write_json(file_path: Path, data: Dict[str, Any], pretty: bool = True):
        """Write JSON file"""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                if pretty:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                else:
                    json.dump(data, f, ensure_ascii=False)
            logger.debug(f"JSON file written: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to write JSON file {file_path}: {e}")
            return False

    @staticmethod
    def read_text(file_path: Path) -> Optional[str]:
        """Read text file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read text file {file_path}: {e}")
            return None

    @staticmethod
    def write_text(file_path: Path, content: str):
        """Write text file"""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.debug(f"Text file written: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to write text file {file_path}: {e}")
            return False

    @staticmethod
    def file_exists(file_path: Path) -> bool:
        """Check if file exists"""
        return file_path.exists() and file_path.is_file()

    @staticmethod
    def dir_exists(dir_path: Path) -> bool:
        """Check if directory exists"""
        return dir_path.exists() and dir_path.is_dir()

    @staticmethod
    def create_dir(dir_path: Path) -> bool:
        """Create directory"""
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Failed to create directory {dir_path}: {e}")
            return False

    @staticmethod
    def delete_file(file_path: Path) -> bool:
        """Delete file"""
        try:
            if file_path.exists():
                file_path.unlink()
            return True
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
            return False

    @staticmethod
    def copy_file(src: Path, dst: Path) -> bool:
        """Copy file"""
        try:
            import shutil
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            return True
        except Exception as e:
            logger.error(f"Failed to copy file {src} to {dst}: {e}")
            return False
