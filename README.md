# 🚀 NOVA PROFILE MANAGER - Enterprise Antidetect Suite v9.0

> **Advanced browser fingerprinting, proxy management, automation, and cloud sync platform**

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen)
![Status](https://img.shields.io/badge/Status-Active-success)

## ✨ Core Features

### 👤 Profile Management
- ✅ Independent fingerprint customization (UA, Resolution, WebRTC, Canvas, WebGL)
- ✅ Bulk profile creation and management
- ✅ Profile grouping and organization
- ✅ Advanced search and filtering
- ✅ Profile templates and presets

### 🌐 Proxy Management
- ✅ Proxy pool with auto-rotation
- ✅ Real-time proxy health checking
- ✅ Proxy-specific authentication bridge
- ✅ ISP/Residential proxy detection
- ✅ Geographic distribution visualization
- ✅ Proxy performance testing and analytics

### ⏰ Automation & Scheduling
- ✅ Cron-based task scheduling
- ✅ Batch profile launching
- ✅ Auto-close browser after X minutes
- ✅ Profile rotation scheduling
- ✅ Event-driven automation

### 💾 Data Management
- ✅ JSON/CSV import and export
- ✅ Encrypted database backup
- ✅ Auto-backup to cloud (Google Drive, Dropbox)
- ✅ Incremental backup and delta sync
- ✅ Database optimization

### 🔐 Security & Privacy
- ✅ Encrypted proxy credentials
- ✅ PIN/2FA protection for sensitive actions
- ✅ Comprehensive audit logging
- ✅ Secure proxy validation
- ✅ Data encryption at rest and in transit

### 📊 Monitoring & Analytics
- ✅ Real-time dashboard with statistics
- ✅ Performance monitoring (CPU, Memory, Network)
- ✅ Browser session analytics
- ✅ Proxy usage statistics
- ✅ Alert system with notifications

### 🛠️ Developer Tools
- ✅ RESTful API server
- ✅ Command-line interface (CLI)
- ✅ WebSocket support for real-time updates
- ✅ Webhook notifications
- ✅ Integration with Selenium/Puppeteer

## 📋 System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **RAM**: Minimum 4GB (8GB+ recommended)
- **Storage**: 500MB for application + browser binaries

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/lamq22558/nova-profile-manager.git
cd nova-profile-manager

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment configuration
cp .env.example .env

# Initialize database
python -m nova.core.setup
```

### Run Application

```bash
# Start GUI Application
python main.py

# Start API Server
python -m nova.api.server

# Start CLI
python -m nova.cli --help
```

## 📁 Project Structure

```
nova-profile-manager/
├── main.py                    # GUI Application Entry Point
├── requirements.txt           # Python Dependencies
├── .env.example              # Environment Configuration Template
├── .gitignore                # Git Ignore Rules
│
├── nova/
│   ├── __init__.py
│   ├── config.py             # Configuration Management
│   ├── constants.py          # Application Constants
│   ├── logger.py             # Logging Setup
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── setup.py          # Initial Setup & DB Initialization
│   │   ├── database.py       # Database Operations
│   │   ├── encryption.py     # Encryption/Decryption Utilities
│   │   └── validators.py     # Input Validation
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── profile.py        # Profile Data Model
│   │   ├── proxy.py          # Proxy Data Model
│   │   ├── group.py          # Group Data Model
│   │   ├── audit.py          # Audit Log Model
│   │   └── backup.py         # Backup Metadata Model
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── profile_service.py       # Profile Management
│   │   ├── proxy_service.py         # Proxy Management & Health Check
│   │   ├── browser_service.py       # Browser Instance Management
│   │   ├── scheduler_service.py     # Task Scheduling
│   │   ├── backup_service.py        # Backup & Recovery
│   │   ├── notification_service.py  # Alert & Notifications
│   │   ├── analytics_service.py     # Performance Analytics
│   │   └── fingerprint_service.py   # Fingerprint Generation
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── server.py         # FastAPI/Flask Server
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── profiles.py   # Profile Endpoints
│   │   │   ├── proxies.py    # Proxy Endpoints
│   │   │   ├── browser.py    # Browser Control Endpoints
│   │   │   ├── scheduler.py  # Scheduler Endpoints
│   │   │   ├── analytics.py  # Analytics Endpoints
│   │   │   └── health.py     # Health Check Endpoint
│   │   └── websocket.py      # WebSocket Support
│   │
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py           # CLI Entry Point
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── profile.py    # Profile Commands
│   │   │   ├── proxy.py      # Proxy Commands
│   │   │   ├── browser.py    # Browser Commands
│   │   │   └── batch.py      # Batch Operations
│   │   └── formatters.py     # Output Formatting
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py    # Main GUI Window
│   │   ├── dialogs/
│   │   │   ├── __init__.py
│   │   │   ├── profile_dialog.py    # Profile Editor
│   │   │   ├── proxy_dialog.py      # Proxy Manager
│   │   │   ├── scheduler_dialog.py  # Task Scheduler
│   │   │   ├── backup_dialog.py     # Backup Manager
│   │   │   └── settings_dialog.py   # Settings
│   │   ├── widgets/
│   │   │   ├── __init__.py
│   │   │   ├── dashboard.py         # Dashboard Widget
│   │   │   ├── profile_table.py     # Profile Table
│   │   │   ├── proxy_table.py       # Proxy Table
│   │   │   ├── logs_viewer.py       # Logs Viewer
│   │   │   └── analytics_chart.py   # Analytics Chart
│   │   └── styles.py         # UI Styling & Themes
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── http_client.py    # HTTP Client with Retry Logic
│   │   ├── file_utils.py     # File Operations
│   │   ├── time_utils.py     # Time/Date Utilities
│   │   ├── path_utils.py     # Path Management
│   │   ├── cloud_sync.py     # Cloud Sync Integration
│   │   └── decorators.py     # Utility Decorators
│   │
│   └── integrations/
│       ├── __init__.py
│       ├── slack.py          # Slack Integration
│       ├── telegram.py       # Telegram Integration
│       ├── google_drive.py   # Google Drive Backup
│       ├── dropbox.py        # Dropbox Backup
│       ├── selenium.py       # Selenium Integration
│       └── puppeteer.py      # Puppeteer Integration
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Pytest Configuration
│   ├── test_profile_service.py
│   ├── test_proxy_service.py
│   ├── test_browser_service.py
│   ├── test_api.py
│   └── fixtures/
│       ├── sample_profiles.json
│       └── sample_proxies.json
│
├── docs/
│   ├── README.md
│   ├── INSTALLATION.md       # Detailed Installation Guide
│   ├── USER_GUIDE.md         # User Guide
│   ├── API_REFERENCE.md      # API Documentation
│   ├── CLI_REFERENCE.md      # CLI Documentation
│   ├── DEVELOPMENT.md        # Development Guide
│   ├── ARCHITECTURE.md       # System Architecture
│   └── TROUBLESHOOTING.md    # Troubleshooting Guide
│
├── examples/
│   ├── api_client.py         # Python API Client Example
│   ├── bulk_profile_creation.py
│   ├── proxy_rotation_automation.py
│   ├── selenium_integration.py
│   └── webhook_listener.py
│
└── docker/
    ├── Dockerfile            # Docker Configuration
    ├── docker-compose.yml    # Multi-container Setup
    └── .dockerignore
```

## 🔧 Configuration

See `.env.example` for all available configuration options:

```bash
# Copy and customize
cp .env.example .env
nano .env  # Edit as needed
```

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [User Guide](docs/USER_GUIDE.md)
- [API Reference](docs/API_REFERENCE.md)
- [CLI Reference](docs/CLI_REFERENCE.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Architecture](docs/ARCHITECTURE.md)

## 🌐 API Usage

### Start API Server

```bash
python -m nova.api.server
```

### Example Requests

```bash
# Get all profiles
curl http://localhost:54345/api/v1/profiles

# Create new profile
curl -X POST http://localhost:54345/api/v1/profiles \
  -H "Content-Type: application/json" \
  -d '{"name": "Profile1", "group": "Default Group"}'

# Launch profile
curl -X POST http://localhost:54345/api/v1/browser/launch \
  -H "Content-Type: application/json" \
  -d '{"profile_id": "nova_12345"}'
```

## 💻 CLI Usage

```bash
# List all profiles
python -m nova.cli profile list

# Create new profile
python -m nova.cli profile create --name "MyProfile" --group "Default Group"

# Launch profile
python -m nova.cli browser launch --profile-id nova_12345

# Schedule task
python -m nova.cli scheduler create --cron "0 9 * * *" --action launch --profile-id nova_12345
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_profile_service.py

# Run with coverage
pytest --cov=nova tests/

# Run with detailed output
pytest -v tests/
```

## 🐳 Docker Support

```bash
# Build image
docker build -f docker/Dockerfile -t nova-manager:latest .

# Run container
docker run -d \
  -p 54345:54345 \
  -v ~/nova_data:/app/nova_data \
  nova-manager:latest

# Using docker-compose
docker-compose -f docker/docker-compose.yml up -d
```

## 🤝 Contributing

Contributions are welcome! Please see [DEVELOPMENT.md](docs/DEVELOPMENT.md) for guidelines.

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

- 📖 Check [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- 💬 Open an issue on GitHub
- 📧 Email: support@novanet.com

## 🙏 Acknowledgments

- Chromium/Chrome browser project
- CustomTkinter GUI framework
- FastAPI framework
- All open-source contributors

---

**Made with ❤️ by NOVA Development Team**
