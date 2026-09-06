"""Browser Management Service"""

import subprocess
import threading
import time
import os
from typing import Dict, Optional, Tuple
from pathlib import Path
from nova.logger import get_logger
from nova.config import settings
from nova.constants import BROWSER_RUNNING, BROWSER_STOPPED, BROWSER_CRASHED
from nova.services.proxy_service import ProxyService
from nova.core.validators import ProxyValidator

logger = get_logger(__name__)


class BrowserService:
    """Service for managing browser instances"""

    def __init__(self):
        self.proxy_service = ProxyService()
        self.proxy_validator = ProxyValidator()
        self.active_processes: Dict[str, subprocess.Popen] = {}
        self._process_lock = threading.RLock()
        self._monitor_thread = None

    def launch_browser(
        self,
        profile_id: str,
        profile_data: Dict,
        debug_port: int = 9222,
        headless: bool = False,
    ) -> Tuple[bool, Optional[str]]:
        """Launch browser instance for profile"""
        try:
            # Check if already running
            with self._process_lock:
                if profile_id in self.active_processes:
                    proc = self.active_processes[profile_id]
                    if proc.poll() is None:
                        return False, f"Profile {profile_id} is already running"
                    else:
                        del self.active_processes[profile_id]

            # Get browser binary path
            browser_path = self._get_browser_path()
            if not browser_path or not os.path.exists(browser_path):
                return False, "Chrome/Chromium browser not found"

            # Create profile data directory
            profile_dir = settings.DATA_DIR / profile_id
            profile_dir.mkdir(parents=True, exist_ok=True)

            # Build launch command
            cmd = [
                str(browser_path),
                f"--user-data-dir={profile_dir}",
                f"--remote-debugging-port={debug_port}",
            ]

            # Add user agent
            user_agent = profile_data.get("user_agent", "")
            if user_agent:
                cmd.append(f"--user-agent={user_agent}")

            # Add screen size
            screen_size = profile_data.get("screen_size", "1366,768")
            if screen_size:
                cmd.append(f"--window-size={screen_size}")

            # Add proxy if configured
            proxy = profile_data.get("proxy", "").strip()
            if proxy and "direct" not in proxy.lower():
                ip, port, user, pwd = self.proxy_validator.parse_proxy(proxy)
                if ip and port:
                    # Check proxy health
                    is_alive, status = self.proxy_service.check_proxy_health(proxy)
                    if not is_alive:
                        return False, f"Proxy is dead: {status}"
                    cmd.append(f"--proxy-server={ip}:{port}")

            # Add default launch arguments
            from nova.constants import CHROME_LAUNCH_ARGS
            cmd.extend(CHROME_LAUNCH_ARGS)

            # Add headless mode if requested
            if headless:
                cmd.append("--headless")
                cmd.append("--disable-gpu")

            # Add target URL
            target_url = profile_data.get("url", "https://facebook.com")
            cmd.append(target_url)

            # Launch browser
            logger.info(f"Launching browser for profile: {profile_id}")
            proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Verify process started
            time.sleep(1)
            if proc.poll() is not None:
                return False, f"Browser exited with code: {proc.returncode}"

            with self._process_lock:
                self.active_processes[profile_id] = proc

            logger.info(f"Browser launched successfully: {profile_id} (PID: {proc.pid})")
            return True, None
        except Exception as e:
            logger.error(f"Failed to launch browser: {e}", exc_info=True)
            return False, str(e)

    def stop_browser(self, profile_id: str) -> Tuple[bool, Optional[str]]:
        """Stop browser instance"""
        try:
            with self._process_lock:
                if profile_id not in self.active_processes:
                    return False, f"No running instance for profile {profile_id}"

                proc = self.active_processes[profile_id]
                proc.terminate()
                time.sleep(1)

                if proc.poll() is None:
                    proc.kill()
                    time.sleep(0.5)

                del self.active_processes[profile_id]

            logger.info(f"Browser stopped: {profile_id}")
            return True, None
        except Exception as e:
            logger.error(f"Failed to stop browser: {e}", exc_info=True)
            return False, str(e)

    def stop_all_browsers(self) -> int:
        """Stop all running browser instances"""
        with self._process_lock:
            profile_ids = list(self.active_processes.keys())

        count = 0
        for profile_id in profile_ids:
            success, _ = self.stop_browser(profile_id)
            if success:
                count += 1

        logger.info(f"Stopped {count} browser instances")
        return count

    def get_running_profiles(self) -> list:
        """Get list of running profile IDs"""
        with self._process_lock:
            return list(self.active_processes.keys())

    def is_running(self, profile_id: str) -> bool:
        """Check if profile is running"""
        with self._process_lock:
            if profile_id in self.active_processes:
                proc = self.active_processes[profile_id]
                return proc.poll() is None
        return False

    def _get_browser_path(self) -> Optional[Path]:
        """Get path to Chrome/Chromium browser"""
        # Check in NOVA binary directory
        local_chrome = settings.BIN_DIR / "chrome-win" / "chrome.exe"
        if local_chrome.exists():
            return local_chrome

        # Check system paths
        system_paths = [
            Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
            Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
            Path(os.path.expandvars("%LocalAppData%/Google/Chrome/Application/chrome.exe")),
            Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),  # macOS
            Path("/usr/bin/google-chrome"),  # Linux
            Path("/usr/bin/chromium"),  # Linux
        ]

        for path in system_paths:
            if path.exists():
                return path

        return None

    def start_process_monitor(self):
        """Start background process monitor"""
        if self._monitor_thread and self._monitor_thread.is_alive():
            return

        def monitor():
            while True:
                try:
                    with self._process_lock:
                        dead_profiles = []
                        for profile_id, proc in self.active_processes.items():
                            if proc.poll() is not None:
                                dead_profiles.append(profile_id)

                        for profile_id in dead_profiles:
                            logger.warning(f"Browser crashed: {profile_id}")
                            del self.active_processes[profile_id]
                except Exception as e:
                    logger.error(f"Process monitor error: {e}")

                time.sleep(2)

        self._monitor_thread = threading.Thread(target=monitor, daemon=True)
        self._monitor_thread.start()
        logger.info("Process monitor started")
