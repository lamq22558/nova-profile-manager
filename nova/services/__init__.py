"""Profile Service"""
from typing import List, Dict, Any, Optional, Tuple
from nova.core import db
from nova.logger import get_logger
import time

logger = get_logger(__name__)

class ProfileService:
    @staticmethod
    def create_profile(
        name: str,
        group: str = "Default Group",
        proxy: str = "",
        user_agent: str = "",
        screen_size: str = "1366,768",
        url: str = "https://facebook.com"
    ) -> Tuple[bool, Optional[Dict], Optional[str]]:
        
        if not name:
            return False, None, "Name required"
        
        profiles = db.get("profiles", [])
        if any(p.get("name") == name for p in profiles):
            return False, None, "Profile name exists"
        
        profile = {
            "id": f"nova_{int(time.time() * 1000)}",
            "name": name,
            "group": group,
            "proxy": proxy,
            "user_agent": user_agent,
            "screen_size": screen_size,
            "url": url,
            "status": "idle",
            "debug_port": 9222 + len(profiles)
        }
        
        profiles.append(profile)
        if db.set("profiles", profiles):
            logger.info(f"Profile created: {profile['id']}")
            return True, profile, None
        return False, None, "Failed to save"
    
    @staticmethod
    def get_all_profiles() -> List[Dict]:
        return db.get("profiles", [])
    
    @staticmethod
    def get_profile(profile_id: str) -> Optional[Dict]:
        profiles = db.get("profiles", [])
        return next((p for p in profiles if p.get("id") == profile_id), None)
    
    @staticmethod
    def delete_profile(profile_id: str) -> bool:
        profiles = db.get("profiles", [])
        filtered = [p for p in profiles if p.get("id") != profile_id]
        if len(filtered) < len(profiles):
            return db.set("profiles", filtered)
        return False
    
    @staticmethod
    def update_profile(profile_id: str, **kwargs) -> bool:
        profiles = db.get("profiles", [])
        for i, p in enumerate(profiles):
            if p.get("id") == profile_id:
                profiles[i].update(kwargs)
                return db.set("profiles", profiles)
        return False
