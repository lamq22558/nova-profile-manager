"""API Server"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from nova.config import settings
from nova.services import ProfileService
from nova.core import db

class ProfileCreate(BaseModel):
    name: str
    group: str = "Default Group"
    proxy: str = ""
    user_agent: str = ""
    screen_size: str = "1366,768"
    url: str = "https://facebook.com"

def create_app():
    app = FastAPI(
        title="NOVA Profile Manager API",
        version="9.0.0",
        description="Enterprise Antidetect Browser Profile Manager"
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    @app.get("/")
    async def root():
        return {"message": "NOVA Profile Manager API", "version": "9.0.0"}
    
    @app.get("/health")
    async def health():
        return {"status": "ok"}
    
    @app.post("/api/v1/profiles")
    async def create_profile(profile: ProfileCreate):
        success, prof, error = ProfileService.create_profile(
            name=profile.name,
            group=profile.group,
            proxy=profile.proxy,
            user_agent=profile.user_agent,
            screen_size=profile.screen_size,
            url=profile.url
        )
        if not success:
            raise HTTPException(status_code=400, detail=error)
        return {"success": True, "profile": prof}
    
    @app.get("/api/v1/profiles")
    async def list_profiles():
        profiles = ProfileService.get_all_profiles()
        return {"profiles": profiles}
    
    @app.get("/api/v1/profiles/{profile_id}")
    async def get_profile(profile_id: str):
        profile = ProfileService.get_profile(profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Not found")
        return {"profile": profile}
    
    @app.delete("/api/v1/profiles/{profile_id}")
    async def delete_profile(profile_id: str):
        if ProfileService.delete_profile(profile_id):
            return {"success": True}
        raise HTTPException(status_code=404, detail="Not found")
    
    @app.get("/api/v1/stats")
    async def stats():
        profiles = ProfileService.get_all_profiles()
        return {
            "total_profiles": len(profiles),
            "by_group": {}
        }
    
    return app
