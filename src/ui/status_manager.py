#!/usr/bin/env python3
"""
StatusManager - Modular status banner and system status UI component
Extracted from the monolithic EnhancedAnonymityGUI to improve maintainability
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging
import threading
import time

logger = logging.getLogger(__name__)


@dataclass
class StatusComponent:
    """Represents a single status component with display and update logic"""
    name: str
    display_name: str
    initial_value: str = ""
    update_callback: Optional[Callable] = None
    update_interval: Optional[float] = None  # Seconds between auto-updates
    last_updated: Optional[datetime] = None

    def should_update(self) -> bool:
        """Check if this component should be updated based on interval"""
        if self.update_interval is None:
            return False
        if self.last_updated is None:
            return True
        return (datetime.now() - self.last_updated).total_seconds() >= self.update_interval


@dataclass
class AnonymityMetrics:
    """Data structure for anonymity score calculation"""
    anonymity_score: int = 0
    profile_name: Optional[str] = None
    proxy_status: str = "Disconnected"
    cookie_count: int = 0
    browser_sessions: int = 0
    system_health: str = "Unknown"


class StatusManager:
    """
    Manages the display and updating of system status components
    Provides centralized status monitoring and real-time updates
    """

    def __init__(self, parent_frame: ttk.Frame, parent_gui):
        """
        Initialize the StatusManager

        Args:
            parent_frame: The parent frame to add status components to
            parent_gui: Reference to the main GUI instance for data access
        """
        self.parent_frame = parent_frame
        self.parent_gui = parent_gui

        # Status components registry
        self.status_components: Dict[str, StatusComponent] = {}
        self.status_labels: Dict[str, ttk.Label] = {}

        # Status banner integration
        self.status_banner = None

        # Auto-update thread
        self.update_thread = None
        self.updating = False
        self.update_interval = 5.0  # seconds

        # Anonymity score tracking
        self.current_metrics = AnonymityMetrics()

        logger.info("✅ StatusManager initialized")

    def register_component(self, name: str, display_name: str,
                          initial_value: str = "",
                          update_callback: Optional[Callable] = None,
                          update_interval: Optional[float] = None) -> None:
        """
        Register a status component for display and updates

        Args:
            name: Internal component name
            display_name: Display name shown to user
            initial_value: Initial display value
            update_callback: Function to call for updates (should return new value)
            update_interval: How often to auto-update in seconds
        """
        component = StatusComponent(
            name=name,
            display_name=display_name,
            initial_value=initial_value,
            update_callback=update_callback,
            update_interval=update_interval
        )

        self.status_components[name] = component
        logger.debug(f"📝 Registered status component: {name}")

    def setup_standard_components(self) -> None:
        """Setup the standard set of status components used by anonymity toolkit"""

        # Core component status
        self.register_component(
            "proxy_scraper",
            "🔍 Proxy Scraper",
            "Loading...",
            self._get_proxy_scraper_status,
            10.0  # Update every 10 seconds
        )

        self.register_component(
            "geo_locator",
            "🌍 Geo Locator",
            "Ready",
            None  # Static for now
        )

        self.register_component(
            "cookie_manager",
            "🍪 Cookie Manager",
            "Ready",
            None  # Static for now
        )

        self.register_component(
            "leak_detector",
            "🛡️ Leak Detector",
            "Ready",
            None  # Static for now
        )

        self.register_component(
            "fingerprint_manager",
            "👤 Fingerprint Manager",
            "Ready",
            None  # Static for now
        )

        self.register_component(
            "user_browser",
            "🌐 User Browser",
            "Ready",
            None  # Static for now
        )

        self.register_component(
            "status_banner",
            "📊 Status Banner",
            "Active",
            None  # Static for now
        )

        self.register_component(
            "stealth_mode",
            "🔐 Stealth Mode",
            "Disabled",
            self._get_stealth_mode_status
        )

        self.register_component(
            "current_proxy",
            "🌀 Current Proxy",
            "None",
            self._get_current_proxy_status
        )

        self.register_component(
            "active_profile",
            "👤 Active Profile",
            "None",
            self._get_active_profile_status
        )

        logger.info("✅ Registered all standard status components")

    def create_status_display(self) -> ttk.Frame:
        """
        Create the visual status display

        Returns:
            The main status grid frame containing the status display
        """
        # System Status Overview Section
        status_frame = ttk.LabelFrame(self.parent_frame, text="📊 System Status")
        status_frame.pack(fill='x', padx=20, pady=10)

        status_grid = ttk.Frame(status_frame)
        status_grid.pack(pady=10)

        # Create labels for each component
        for component in self.status_components.values():
            # Create the display row
            ttk.Label(status_grid, text=f"{component.display_name}:",
                      font=("Arial", 10, "bold")).grid(
                row=len(self.status_labels), column=0, sticky='w', padx=10
            )

            self.status_labels[component.name] = ttk.Label(
                status_grid, text=component.initial_value
            )
            self.status_labels[component.name].grid(
                row=len(self.status_labels) - 1, column=1, sticky='w', padx=10
            )

        # Initialize status banner if available
        if hasattr(self.parent_gui, 'status_banner') and self.parent_gui.status_banner:
            self.status_banner = self.parent_gui.status_banner

        # Start auto-updates
        self.start_auto_updates()

        logger.info("✅ Status display created with auto-updates")
        return status_grid

    def update_all_components(self) -> None:
        """Update all status components with current values"""
        for name, component in self.status_components.items():
            self.update_component(name)

    def update_component(self, name: str) -> None:
        """Update a specific status component"""
        if name not in self.status_components:
            logger.warning(f"Unknown status component: {name}")
            return

        component = self.status_components[name]

        # Call update callback if available
        if component.update_callback:
            try:
                new_value = component.update_callback()
                component.last_updated = datetime.now()

                # Update the label if it exists
                if name in self.status_labels:
                    self.status_labels[name].config(text=new_value)
                    logger.debug(f"📈 Updated {name}: {new_value}")

            except Exception as e:
                logger.error(f"❌ Error updating {name}: {e}")
                if name in self.status_labels:
                    self.status_labels[name].config(text="Error")

    def start_auto_updates(self) -> None:
        """Start the background thread for automatic status updates"""
        if self.update_thread and self.update_thread.is_alive():
            return  # Already running

        self.updating = True
        self.update_thread = threading.Thread(
            target=self._auto_update_loop,
            daemon=True,
            name="StatusManager-AutoUpdate"
        )
        self.update_thread.start()
        logger.info("🔄 Started automatic status updates")

    def stop_auto_updates(self) -> None:
        """Stop automatic status updates"""
        self.updating = False
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=2.0)
        logger.info("🛑 Stopped automatic status updates")

    def _auto_update_loop(self) -> None:
        """Background loop for automatic updates"""
        while self.updating:
            try:
                # Find components that need updating
                now = datetime.now()
                components_to_update = []

                for name, component in self.status_components.items():
                    if component.should_update():
                        components_to_update.append(name)

                # Update components in main thread
                if components_to_update:
                    def update_ui():
                        for name in components_to_update:
                            self.update_component(name)

                    # Schedule UI update in main thread
                    self.parent_frame.after(0, update_ui)

                time.sleep(self.update_interval)

            except Exception as e:
                logger.error(f"❌ Auto-update loop error: {e}")
                time.sleep(self.update_interval)

    # Status callback methods
    def _get_proxy_scraper_status(self) -> str:
        """Get current proxy scraper status"""
        try:
            if hasattr(self.parent_gui, 'proxy_scraper') and self.parent_gui.proxy_scraper:
                source_count = len(getattr(self.parent_gui.proxy_scraper, 'sources', []))
                verified_count = len(getattr(self.parent_gui.verified_proxies, 'verified_proxies', self.parent_gui.verified_proxies))
                return f"{source_count} sources ({verified_count} verified)"
            return "Loading..."
        except Exception:
            return "Error"

    def _get_stealth_mode_status(self) -> str:
        """Get stealth mode status"""
        try:
            if hasattr(self.parent_gui, 'stealth_mode'):
                return "Enabled" if self.parent_gui.stealth_mode else "Disabled"
            return "Unknown"
        except Exception:
            return "Error"

    def _get_current_proxy_status(self) -> str:
        """Get current proxy status"""
        try:
            if hasattr(self.parent_gui, 'current_proxy'):
                return self.parent_gui.current_proxy or "None"
            return "None"
        except Exception:
            return "Error"

    def _get_active_profile_status(self) -> str:
        """Get active profile status"""
        try:
            if hasattr(self.parent_gui, 'selected_profile'):
                return self.parent_gui.selected_profile or "None"
            return "None"
        except Exception:
            return "Error"

    def update_anonymity_score(self) -> None:
        """Update the anonymity score based on current system state"""
        try:
            if not self.status_banner:
                return

            # Gather current metrics
            self.current_metrics.anonymity_score = self._calculate_anonymity_score()
            self.current_metrics.profile_name = self._get_active_profile_status()
            self.current_metrics.proxy_status = "Connected" if self._get_current_proxy_status() != "None" else "Disconnected"
            self.current_metrics.cookie_count = self._get_cookie_count()
            self.current_metrics.browser_sessions = self._get_active_browser_sessions()
            self.current_metrics.system_health = self._get_system_health()

            # Update status banner
            status_data = {
                'anonymity_score': self.current_metrics.anonymity_score,
                'profile_name': self.current_metrics.profile_name,
                'proxy_status': self.current_metrics.proxy_status,
                'cookie_count': self.current_metrics.cookie_count,
                'browser_sessions': self.current_metrics.browser_sessions,
                'system_health': self.current_metrics.system_health
            }

            self.status_banner.update_status(status_data)

        except Exception as e:
            logger.error(f"❌ Error updating anonymity score: {e}")

    def _calculate_anonymity_score(self) -> int:
        """Calculate overall anonymity score (0-100)"""
        score = 0

        try:
            # Profile score (25 points)
            if self._get_active_profile_status() != "None":
                score += 25

            # Proxy score (25 points)
            if self._get_current_proxy_status() != "None":
                score += 25

            # Cookie score (25 points max)
            cookie_count = self._get_cookie_count()
            if cookie_count > 0:
                cookie_score = min(25, cookie_count // 5)  # 5 cookies = 1 point
                score += cookie_score

            # Health score (25 points)
            health = self._get_system_health().lower()
            if health == "excellent":
                score += 25
            elif health == "good":
                score += 18
            elif health == "fair":
                score += 12
            elif health == "poor":
                score += 6

            return min(100, score)

        except Exception:
            return 0

    def _get_cookie_count(self) -> int:
        """Get total cookie count"""
        try:
            if hasattr(self.parent_gui, 'cookie_harvester'):
                profile_name = self._get_active_profile_status()
                if profile_name != "None":
                    stats = self.parent_gui.cookie_harvester.get_harvest_stats(profile_name)
                    return stats.get('total_cookies', 0)
            return 0
        except Exception:
            return 0

    def _get_active_browser_sessions(self) -> int:
        """Get count of active browser sessions"""
        try:
            if hasattr(self.parent_gui, 'user_browser'):
                return len(self.parent_gui.user_browser.get_active_sessions())
            return 0
        except Exception:
            return 0

    def _get_system_health(self) -> str:
        """Get overall system health status"""
        try:
            health_score = 0

            # Check various components
            components = [
                'proxy_scraper', 'geo_locator', 'cookie_manager',
                'leak_detector', 'fingerprint_manager', 'user_browser'
            ]

            available_count = 0
            for comp in components:
                if hasattr(self.parent_gui, comp) and getattr(self.parent_gui, comp) is not None:
                    available_count += 1

            health_score = (available_count / len(components)) * 100

            if health_score >= 90:
                return "Excellent"
            elif health_score >= 70:
                return "Good"
            elif health_score >= 50:
                return "Fair"
            else:
                return "Poor"

        except Exception:
            return "Unknown"

    def get_status_report(self) -> Dict[str, Any]:
        """Get comprehensive status report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'components': {
                name: {
                    'display_name': comp.display_name,
                    'current_value': self.status_labels.get(name, ttk.Label()).cget('text') if name in self.status_labels else "Unknown",
                    'last_updated': comp.last_updated.isoformat() if comp.last_updated else None,
                    'update_interval': comp.update_interval
                }
                for name, comp in self.status_components.items()
            },
            'anonymity_metrics': {
                'score': self.current_metrics.anonymity_score,
                'profile': self.current_metrics.profile_name,
                'proxy': self.current_metrics.proxy_status,
                'cookies': self.current_metrics.cookie_count,
                'sessions': self.current_metrics.browser_sessions,
                'health': self.current_metrics.system_health
            },
            'system_health': self._get_system_health(),
            'auto_updates_active': self.updating
        }

    def cleanup(self) -> None:
        """Clean up resources"""
        self.stop_auto_updates()
        logger.info("🧹 StatusManager cleanup completed")
