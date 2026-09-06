"""Application Constants"""

# Default User Agents
DEFAULT_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

# Default Screen Sizes
DEFAULT_SCREEN_SIZES = [
    "1280,720",
    "1366,768",
    "1440,900",
    "1600,900",
    "1920,1080",
    "2560,1440",
]

# Default Groups
DEFAULT_GROUPS = [
    "Default Group",
    "Group 1",
    "Group 2",
    "Campaign_Reels",
]

# Browser Launch Arguments
CHROME_LAUNCH_ARGS = [
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-background-networking",
    "--disable-features=TranslateUI",
    "--disable-session-crashed-bubble",
    "--hide-crash-restore-bubble",
    "--test-type",
    "--enforce-webrtc-ip-permission-check",
    "--force-webrtc-ip-handling-policy=disable_non_proxied_udp",
]

# API Response Codes
API_SUCCESS = 200
API_CREATED = 201
API_BAD_REQUEST = 400
API_UNAUTHORIZED = 401
API_FORBIDDEN = 403
API_NOT_FOUND = 404
API_CONFLICT = 409
API_INTERNAL_ERROR = 500

# Status Codes
STATUS_IDLE = "idle"
STATUS_RUNNING = "running"
STATUS_ERROR = "error"
STATUS_STOPPED = "stopped"

# Proxy Status
PROXY_LIVE = "live"
PROXY_DEAD = "dead"
PROXY_CHECKING = "checking"

# Browser Process States
BROWSER_NOT_STARTED = "not_started"
BROWSER_STARTING = "starting"
BROWSER_RUNNING = "running"
BROWSER_STOPPING = "stopping"
BROWSER_STOPPED = "stopped"
BROWSER_CRASHED = "crashed"

# Notification Types
NOTIF_INFO = "info"
NOTIF_WARNING = "warning"
NOTIF_ERROR = "error"
NOTIF_SUCCESS = "success"
