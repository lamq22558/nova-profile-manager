"""Profile Data Model"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
from datetime import datetime
from nova.constants import DEFAULT_USER_AGENTS, DEFAULT_SCREEN_SIZES
import random
import time


@dataclass
class Profile:
    """Browser Profile Model"""

    name: str
    group: str = "Default Group"
    proxy: str = ""
    user_agent: str = ""
    screen_size: str = ""
    url: str = "https://facebook.com"
    id: str = ""
    debug_port: int = 9222
    created_at: str = ""
    updated_at: str = ""
    status: str = "idle"
    notes: str = ""
    tags: list = field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            self.id = f"nova_{int(time.time() * 1000)}"
        if not self.user_agent:
            self.user_agent = random.choice(DEFAULT_USER_AGENTS)
        if not self.screen_size:
            self.screen_size = random.choice(DEFAULT_SCREEN_SIZES)
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Profile":
        """Create from dictionary"""
        return cls(**data)

    def update(self, **kwargs):
        """Update profile attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()

    def __repr__(self) -> str:
        return f"Profile(id={self.id}, name={self.name}, status={self.status})"
