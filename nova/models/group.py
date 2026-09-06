"""Group Data Model"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any
from datetime import datetime


@dataclass
class Group:
    """Profile Group Model"""

    name: str
    description: str = ""
    color: str = "#2563eb"
    created_at: str = ""
    profile_count: int = 0

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Group":
        """Create from dictionary"""
        return cls(**data)

    def __repr__(self) -> str:
        return f"Group(name={self.name}, profiles={self.profile_count})"
