"""Audit Log Model"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum


class AuditAction(str, Enum):
    """Audit action types"""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LAUNCH = "launch"
    STOP = "stop"
    LOGIN = "login"
    EXPORT = "export"
    IMPORT = "import"


@dataclass
class AuditLog:
    """Audit Log Model"""

    action: AuditAction
    resource_type: str  # profile, proxy, group, etc.
    resource_id: str
    description: str
    user: str = "system"
    timestamp: str = ""
    status: str = "success"
    details: dict = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if self.details is None:
            self.details = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data["action"] = self.action.value
        return data

    def __repr__(self) -> str:
        return f"AuditLog(action={self.action}, resource={self.resource_type}/{self.resource_id})"
