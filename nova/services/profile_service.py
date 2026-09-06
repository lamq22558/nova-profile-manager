"""Profile Management Service"""

from typing import List, Dict, Any, Optional, Tuple
from nova.core.database import Database
from nova.core.validators import ProfileValidator
from nova.models.profile import Profile
from nova.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)


class ProfileService:
    """Service for managing browser profiles"""

    def __init__(self):
        self.db = Database()
        self.validator = ProfileValidator()

    def create_profile(
        self,
        name: str,
        group: str = "Default Group",
        proxy: str = "",
        user_agent: str = "",
        screen_size: str = "",
        url: str = "https://facebook.com",
        notes: str = "",
        tags: List[str] = None,
    ) -> Tuple[bool, Optional[Profile], Optional[str]]:
        """Create new profile"""
        # Validate name
        is_valid, error = self.validator.validate_name(name)
        if not is_valid:
            logger.warning(f"Invalid profile name: {error}")
            return False, None, error

        # Validate URL if provided
        if url:
            is_valid, error = self.validator.validate_url(url)
            if not is_valid:
                logger.warning(f"Invalid URL: {error}")
                return False, None, error

        # Validate screen size if provided
        if screen_size:
            is_valid, error = self.validator.validate_screen_size(screen_size)
            if not is_valid:
                logger.warning(f"Invalid screen size: {error}")
                return False, None, error

        # Check for duplicate name
        if self._profile_name_exists(name):
            error = f"Profile with name '{name}' already exists"
            logger.warning(error)
            return False, None, error

        try:
            profile = Profile(
                name=name,
                group=group,
                proxy=proxy,
                user_agent=user_agent,
                screen_size=screen_size,
                url=url,
                notes=notes,
                tags=tags or [],
            )

            if self.db.add_profile(profile.to_dict()):
                logger.info(f"Profile created: {profile.id} - {name}")
                return True, profile, None
            else:
                return False, None, "Failed to save profile to database"
        except Exception as e:
            logger.error(f"Failed to create profile: {e}", exc_info=True)
            return False, None, str(e)

    def get_profile(self, profile_id: str) -> Optional[Profile]:
        """Get profile by ID"""
        data = self.db.get_profile(profile_id)
        if data:
            return Profile.from_dict(data)
        return None

    def get_all_profiles(self) -> List[Profile]:
        """Get all profiles"""
        profiles = self.db.get_profiles()
        return [Profile.from_dict(p) for p in profiles]

    def get_profiles_by_group(self, group: str) -> List[Profile]:
        """Get profiles by group"""
        all_profiles = self.get_all_profiles()
        return [p for p in all_profiles if p.group == group]

    def update_profile(self, profile_id: str, **kwargs) -> Tuple[bool, Optional[str]]:
        """Update profile"""
        try:
            profile = self.get_profile(profile_id)
            if not profile:
                return False, f"Profile '{profile_id}' not found"

            # Validate updated fields
            if "name" in kwargs:
                is_valid, error = self.validator.validate_name(kwargs["name"])
                if not is_valid:
                    return False, error
                if kwargs["name"] != profile.name and self._profile_name_exists(kwargs["name"]):
                    return False, f"Profile with name '{kwargs['name']}' already exists"

            if "screen_size" in kwargs:
                is_valid, error = self.validator.validate_screen_size(kwargs["screen_size"])
                if not is_valid:
                    return False, error

            if "url" in kwargs:
                is_valid, error = self.validator.validate_url(kwargs["url"])
                if not is_valid:
                    return False, error

            kwargs["updated_at"] = datetime.now().isoformat()
            if self.db.update_profile(profile_id, kwargs):
                logger.info(f"Profile updated: {profile_id}")
                return True, None
            else:
                return False, "Failed to update profile"
        except Exception as e:
            logger.error(f"Failed to update profile: {e}", exc_info=True)
            return False, str(e)

    def delete_profile(self, profile_id: str) -> Tuple[bool, Optional[str]]:
        """Delete profile"""
        try:
            if self.db.delete_profile(profile_id):
                logger.info(f"Profile deleted: {profile_id}")
                return True, None
            else:
                return False, "Profile not found"
        except Exception as e:
            logger.error(f"Failed to delete profile: {e}", exc_info=True)
            return False, str(e)

    def search_profiles(self, keyword: str) -> List[Profile]:
        """Search profiles by keyword"""
        keyword = keyword.lower()
        profiles = self.get_all_profiles()
        return [
            p
            for p in profiles
            if keyword in p.name.lower()
            or keyword in p.id.lower()
            or keyword in p.proxy.lower()
            or any(keyword in tag.lower() for tag in p.tags)
        ]

    def add_tag_to_profile(self, profile_id: str, tag: str) -> Tuple[bool, Optional[str]]:
        """Add tag to profile"""
        profile = self.get_profile(profile_id)
        if not profile:
            return False, f"Profile '{profile_id}' not found"

        if tag not in profile.tags:
            profile.tags.append(tag)
            return self.update_profile(profile_id, tags=profile.tags)
        return True, None

    def remove_tag_from_profile(self, profile_id: str, tag: str) -> Tuple[bool, Optional[str]]:
        """Remove tag from profile"""
        profile = self.get_profile(profile_id)
        if not profile:
            return False, f"Profile '{profile_id}' not found"

        if tag in profile.tags:
            profile.tags.remove(tag)
            return self.update_profile(profile_id, tags=profile.tags)
        return True, None

    def _profile_name_exists(self, name: str) -> bool:
        """Check if profile name already exists"""
        profiles = self.get_all_profiles()
        return any(p.name == name for p in profiles)

    def get_statistics(self) -> Dict[str, Any]:
        """Get profile statistics"""
        profiles = self.get_all_profiles()
        groups = {}
        status_count = {}

        for profile in profiles:
            # Count by group
            groups[profile.group] = groups.get(profile.group, 0) + 1
            # Count by status
            status_count[profile.status] = status_count.get(profile.status, 0) + 1

        return {
            "total_profiles": len(profiles),
            "by_group": groups,
            "by_status": status_count,
            "total_groups": len(groups),
        }
