"""FastAPI Server"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from nova.config import settings
from nova.logger import get_logger
from nova.services.profile_service import ProfileService
from nova.services.proxy_service import ProxyService
from nova.services.browser_service import BrowserService
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

logger = get_logger(__name__)

# Initialize services
profile_service = ProfileService()
proxy_service = ProxyService()
browser_service = BrowserService()

# Pydantic models
class ProfileCreate(BaseModel):
    name: str
    group: str = "Default Group"
    proxy: str = ""
    user_agent: str = ""
    screen_size: str = ""
    url: str = "https://facebook.com"
    notes: str = ""

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    group: Optional[str] = None
    proxy: Optional[str] = None
    user_agent: Optional[str] = None
    screen_size: Optional[str] = None
    url: Optional[str] = None
    notes: Optional[str] = None

class ProxyAdd(BaseModel):
    proxy: str
    name: str = ""
    provider: str = ""
    country: str = ""

class BrowserLaunch(BaseModel):
    profile_id: str
    headless: bool = False


def create_app():
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="NOVA Profile Manager API",
        description="Enterprise Antidetect Browser Profile Manager API",
        version=settings.APP_VERSION,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check
    @app.get("/health")
    async def health_check():
        return {"status": "ok", "timestamp": datetime.now().isoformat()}

    # Profile endpoints
    @app.post("/api/v1/profiles")
    async def create_profile(profile: ProfileCreate):
        success, created_profile, error = profile_service.create_profile(
            name=profile.name,
            group=profile.group,
            proxy=profile.proxy,
            user_agent=profile.user_agent,
            screen_size=profile.screen_size,
            url=profile.url,
            notes=profile.notes,
        )
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        return {"success": True, "profile": created_profile.to_dict()}

    @app.get("/api/v1/profiles")
    async def list_profiles():
        profiles = profile_service.get_all_profiles()
        return {"profiles": [p.to_dict() for p in profiles]}

    @app.get("/api/v1/profiles/{profile_id}")
    async def get_profile(profile_id: str):
        profile = profile_service.get_profile(profile_id)
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
        return {"profile": profile.to_dict()}

    @app.put("/api/v1/profiles/{profile_id}")
    async def update_profile(profile_id: str, profile: ProfileUpdate):
        updates = profile.dict(exclude_unset=True)
        success, error = profile_service.update_profile(profile_id, **updates)
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        return {"success": True, "message": "Profile updated"}

    @app.delete("/api/v1/profiles/{profile_id}")
    async def delete_profile(profile_id: str):
        success, error = profile_service.delete_profile(profile_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error)
        return {"success": True, "message": "Profile deleted"}

    # Proxy endpoints
    @app.post("/api/v1/proxies")
    async def add_proxy(proxy: ProxyAdd):
        success, error = proxy_service.add_proxy(
            proxy=proxy.proxy,
            name=proxy.name,
            provider=proxy.provider,
            country=proxy.country,
        )
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        return {"success": True, "proxy": proxy.proxy}

    @app.get("/api/v1/proxies")
    async def list_proxies():
        proxies = proxy_service.get_all_proxies()
        return {"proxies": proxies}

    @app.delete("/api/v1/proxies/{proxy}")
    async def delete_proxy(proxy: str):
        success, error = proxy_service.delete_proxy(proxy)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error)
        return {"success": True, "message": "Proxy deleted"}

    @app.post("/api/v1/proxies/check-health")
    async def check_proxy_health(proxy: str):
        is_alive, status_msg = proxy_service.check_proxy_health(proxy)
        return {"proxy": proxy, "alive": is_alive, "status": status_msg}

    # Browser control endpoints
    @app.post("/api/v1/browser/launch")
    async def launch_browser(req: BrowserLaunch):
        profile = profile_service.get_profile(req.profile_id)
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
        
        success, error = browser_service.launch_browser(
            profile_id=req.profile_id,
            profile_data=profile.to_dict(),
            debug_port=profile.debug_port,
            headless=req.headless,
        )
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        return {"success": True, "message": f"Browser launched for {req.profile_id}"}

    @app.post("/api/v1/browser/stop")
    async def stop_browser(profile_id: str):
        success, error = browser_service.stop_browser(profile_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        return {"success": True, "message": f"Browser stopped for {profile_id}"}

    @app.get("/api/v1/browser/running")
    async def get_running_profiles():
        running = browser_service.get_running_profiles()
        return {"running_profiles": running}

    # Statistics endpoints
    @app.get("/api/v1/stats/profiles")
    async def profile_stats():
        stats = profile_service.get_statistics()
        return {"statistics": stats}

    @app.get("/api/v1/stats/proxies")
    async def proxy_stats():
        stats = proxy_service.get_statistics()
        return {"statistics": stats}

    return app


if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        log_level=settings.LOG_LEVEL.lower(),
    )
