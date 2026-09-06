"""Proxy Data Model"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
from datetime import datetime
from nova.constants import PROXY_CHECKING


@dataclass
class Proxy:
    """Proxy Model"""

    proxy: str  # Full proxy string: IP:Port:User:Pass or IP:Port
    name: str = ""
    provider: str = ""
    country: str = ""
    status: str = PROXY_CHECKING
    last_check: str = ""
    created_at: str = ""
    notes: str = ""
    tags: list = field(default_factory=list)
    rotation_enabled: bool = True

    def __post_init__(self):
        if not self.name:
            self.name = self.proxy
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.last_check:
            self.last_check = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Proxy":
        """Create from dictionary"""
        return cls(**data)

    def update(self, **kwargs):
        """Update proxy attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"Proxy(name={self.name}, status={self.status})"
