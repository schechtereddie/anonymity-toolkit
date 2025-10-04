#!/usr/bin/env python3
"""
Anonymity Toolkit Backend API
Provides REST API endpoints for the anonymity toolkit
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
import json
import os
import time
from typing import List, Dict, Optional
from datetime import datetime

# Import our toolkit components
try:
    from .proxy_scraper import AdvancedProxyScraper
    from .geo_locator import AdvancedGeoLocator
    from .cookie_manager import CookieManager
    from .leak_detector import LeakDetector
except ImportError:
    # Fallback for direct execution
    from proxy_scraper import AdvancedProxyScraper
    from geo_locator import AdvancedGeoLocator
    from cookie_manager import CookieManager
    from leak_detector import LeakDetector

class AnonymityToolkitBackend:
    def __init__(self):
        self.app = FastAPI(
            title="Anonymity Toolkit API",
            description="Backend API for advanced privacy protection tools",
            version="4.0"
        )

        # Initialize components
        self.proxy_scraper = AdvancedProxyScraper()
        self.geo_locator = AdvancedGeoLocator()
        self.cookie_manager = CookieManager()
        self.leak_detector = LeakDetector()

        # Background task tracking
        self.background_tasks = {}

        # Setup CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.setup_routes()

    def setup_routes(self):
        """Setup API routes"""

        @self.app.get("/")
        async def root():
            return {
                "name": "Anonymity Toolkit API",
                "version": "4.0",
                "status": "running",
                "features": [
                    "SOCKS5 Proxy Management",
                    "Geo-Location Intelligence",
                    "Cookie Management",
                    "Leak Detection",
                    "Background Processing"
                ]
            }

        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "timestamp": datetime.now().isoformat()}

        @self.app.get("/components/status")
        async def get_component_status():
            """Get status of all components"""
            return {
                "proxy_scraper": {
                    "sources": len(self.proxy_scraper.sources),
                    "user_agents": len(self.proxy_scraper.user_agents),
                    "maxmind_db": self.proxy_scraper.maxmind_reader is not None
                },
                "geo_locator": {
                    "cache_size": len(self.geo_locator.cache),
                    "maxmind_db": self.geo_locator.maxmind_reader is not None
                },
                "background_tasks": len(self.background_tasks)
            }

        # Proxy Management Routes
        @self.app.post("/proxy/scrape")
        async def scrape_proxies(background_tasks: BackgroundTasks):
            """Start proxy scraping in background"""
            task_id = f"scrape_{int(time.time())}"
            background_tasks.add_task(self._background_scrape, task_id)
            return {"task_id": task_id, "status": "started"}

        @self.app.post("/proxy/verify")
        async def verify_proxies(background_tasks: BackgroundTasks):
            """Start proxy verification in background"""
            task_id = f"verify_{int(time.time())}"
            background_tasks.add_task(self._background_verify, task_id)
            return {"task_id": task_id, "status": "started"}

        @self.app.get("/proxy/list")
        async def get_proxies(limit: int = 100, country: str = None):
            """Get list of proxies"""
            proxies = self.proxy_scraper.verified_proxies

            if country:
                proxies = [p for p in proxies if p.get('country', '').lower() == country.lower()]

            return {
                "total": len(proxies),
                "limit": limit,
                "proxies": proxies[:limit]
            }

        @self.app.get("/proxy/stats")
        async def get_proxy_stats():
            """Get proxy statistics"""
            working = [p for p in self.proxy_scraper.verified_proxies if p.get('working')]
            countries = set(p.get('country', 'Unknown') for p in working)

            return {
                "total_scraped": len(self.proxy_scraper.proxies),
                "total_verified": len(self.proxy_scraper.verified_proxies),
                "working": len(working),
                "unique_countries": len(countries),
                "countries": list(countries)
            }

        # Geo Location Routes
        @self.app.get("/geo/lookup/{ip}")
        async def lookup_ip(ip: str):
            """Lookup geo information for IP"""
            try:
                geo_info = self.geo_locator.get_geo_info(ip)
                return geo_info
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/geo/current")
        async def get_current_ip():
            """Get current public IP"""
            current_ip = self.geo_locator.get_current_ip()
            if current_ip == 'Unknown':
                raise HTTPException(status_code=500, detail="Could not determine current IP")

            geo_info = self.geo_locator.get_geo_info(current_ip)
            return {
                "current_ip": current_ip,
                "geo_info": geo_info
            }

        @self.app.get("/geo/cache")
        async def get_geo_cache():
            """Get geo cache statistics"""
            return self.geo_locator.get_geo_stats()

        @self.app.delete("/geo/cache")
        async def clear_geo_cache():
            """Clear geo cache"""
            self.geo_locator.clear_cache()
            return {"status": "cache_cleared"}

        # Cookie Management Routes
        @self.app.get("/cookies/generate")
        async def generate_cookies(browser: str = "random", domain: Optional[str] = None):
            """Generate browser cookies"""
            try:
                ua = self.cookie_manager.generate_user_agent(browser)
                cookies = self.cookie_manager.create_cookies(domain or "example.com")

                return {
                    "user_agent": ua,
                    "cookies": cookies,
                    "browser": browser
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/cookies/export")
        async def export_cookies():
            """Export cookies to file"""
            try:
                filename = f"cookies_export_{int(time.time())}.json"
                self.cookie_manager.export_cookies(filename)
                return {"filename": filename, "status": "exported"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        # Leak Detection Routes
        @self.app.post("/leak/start")
        async def start_leak_monitoring(proxy_host: str = None, proxy_port: str = None):
            """Start leak monitoring"""
            try:
                proxy_config = None
                if proxy_host and proxy_port:
                    proxy_config = {
                        'http': f'socks5://{proxy_host}:{proxy_port}',
                        'https': f'socks5://{proxy_host}:{proxy_port}'
                    }

                self.leak_detector.start_leak_protection(proxy_config)
                return {"status": "monitoring_started"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/leak/stop")
        async def stop_leak_monitoring():
            """Stop leak monitoring"""
            try:
                self.leak_detector.stop_leak_protection()
                return {"status": "monitoring_stopped"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/leak/check")
        async def check_leaks():
            """Check for current leaks"""
            try:
                leaks = self.leak_detector.get_leaks()
                return {"leaks": leaks, "count": len(leaks)}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        # Background Task Management
        @self.app.get("/tasks")
        async def get_background_tasks():
            """Get list of background tasks"""
            return {
                "tasks": list(self.background_tasks.keys()),
                "count": len(self.background_tasks)
            }

        @self.app.get("/tasks/{task_id}")
        async def get_task_status(task_id: str):
            """Get status of specific task"""
            if task_id not in self.background_tasks:
                raise HTTPException(status_code=404, detail="Task not found")

            return self.background_tasks[task_id]

    async def _background_scrape(self, task_id: str):
        """Background proxy scraping task"""
        self.background_tasks[task_id] = {
            "id": task_id,
            "type": "scrape",
            "status": "running",
            "start_time": datetime.now().isoformat()
        }

        try:
            proxies = self.proxy_scraper.scrape_proxies()
            self.background_tasks[task_id].update({
                "status": "completed",
                "result": {"proxies_scraped": len(proxies)},
                "end_time": datetime.now().isoformat()
            })
        except Exception as e:
            self.background_tasks[task_id].update({
                "status": "failed",
                "error": str(e),
                "end_time": datetime.now().isoformat()
            })

    async def _background_verify(self, task_id: str):
        """Background proxy verification task"""
        self.background_tasks[task_id] = {
            "id": task_id,
            "type": "verify",
            "status": "running",
            "start_time": datetime.now().isoformat()
        }

        try:
            verified = self.proxy_scraper.verify_proxies(include_geo=True)
            self.background_tasks[task_id].update({
                "status": "completed",
                "result": {"proxies_verified": len(verified)},
                "end_time": datetime.now().isoformat()
            })
        except Exception as e:
            self.background_tasks[task_id].update({
                "status": "failed",
                "error": str(e),
                "end_time": datetime.now().isoformat()
            })

    def run(self, host="127.0.0.1", port=8080):
        """Run the backend server"""
        print("🚀 Starting Anonymity Toolkit Backend API")
        print(f"📡 Server: http://{host}:{port}")
        print(f"📚 Docs: http://{host}:{port}/docs")
        print("=" * 50)

        uvicorn.run(self.app, host=host, port=port)

def create_backend_app():
    """Create and return the FastAPI app"""
    backend = AnonymityToolkitBackend()
    return backend.app

if __name__ == "__main__":
    backend = AnonymityToolkitBackend()
    backend.run()
