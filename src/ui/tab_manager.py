#!/usr/bin/env python3
"""
Tab Manager - Modular tab coordination system
Extracted from the monolithic EnhancedAnonymityGUI to improve maintainability
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class TabConfig:
    """Configuration for a single tab"""
    name: str
    title: str
    create_method: Callable
    priority: int = 0  # Lower numbers = higher priority in ordering


class TabManager:
    """
    Manages creation and coordination of GUI tabs
    Handles tab ordering, state management, and inter-tab communication
    """

    def __init__(self, parent_notebook: ttk.Notebook, parent_gui):
        """
        Initialize the tab manager

        Args:
            parent_notebook: The ttk.Notebook widget to add tabs to
            parent_gui: Reference to the main GUI instance for callbacks
        """
        self.notebook = parent_notebook
        self.parent_gui = parent_gui
        self.tabs: Dict[str, tk.Frame] = {}
        self.tab_configs: Dict[str, TabConfig] = {}

        # Track tab creation status
        self.created_tabs: Dict[str, bool] = {}

        logger.info("✅ TabManager initialized")

    def register_tab(self, name: str, title: str, create_method: Callable,
                    priority: int = 0) -> None:
        """
        Register a tab for creation

        Args:
            name: Internal name for the tab
            title: Display title for the tab
            create_method: Method to call to create the tab content
            priority: Ordering priority (lower = appears first)
        """
        self.tab_configs[name] = TabConfig(
            name=name,
            title=title,
            create_method=create_method,
            priority=priority
        )
        logger.debug(f"📝 Registered tab: {name} -> {title}")

    def register_standard_tabs(self) -> None:
        """Register all standard tabs with their default priorities"""
        # Dashboard should be first (highest priority = lowest number)
        self.register_tab("dashboard", "🏠 Enhanced Dashboard",
                         self.parent_gui.create_dashboard_tab, priority=0)

        # Core functionality tabs
        self.register_tab("browser", "🌐 User Browser",
                         self.parent_gui.create_browser_tab, priority=10)
        self.register_tab("proxy", "🔍 Enhanced Proxy Manager",
                         self.parent_gui.create_proxy_tab, priority=20)
        self.register_tab("cookie", "🍪 Enhanced Cookie Manager",
                         self.parent_gui.create_cookie_tab, priority=30)
        self.register_tab("profile", "👤 Enhanced Profile Manager",
                         self.parent_gui.create_profile_tab, priority=40)

        # Monitoring and debugging (lower priority = appear later)
        self.register_tab("monitoring", "🔍 Enhanced Traffic Monitor",
                         self.parent_gui.create_monitoring_tab, priority=50)
        self.register_tab("status", "📊 Enhanced Status",
                         self.parent_gui.create_status_tab, priority=60)

        logger.info("✅ Registered all standard tabs")

    def create_all_tabs(self) -> None:
        """Create all registered tabs in priority order"""
        # Sort tabs by priority
        sorted_configs = sorted(
            self.tab_configs.values(),
            key=lambda config: config.priority
        )

        for config in sorted_configs:
            try:
                self._create_tab(config)
            except Exception as e:
                logger.error(f"❌ Failed to create tab {config.name}: {e}")
                # Continue with other tabs even if one fails

        logger.info(f"✅ Created {len(self.tabs)} tabs successfully")

    def _create_tab(self, config: TabConfig) -> None:
        """Create a single tab"""
        # Create the tab frame
        tab_frame = tk.Frame(self.notebook)
        self.tabs[config.name] = tab_frame

        # Add to notebook
        self.notebook.add(tab_frame, text=config.title)

        # Call the creation method with the frame as context
        # Temporarily set the frame as an attribute for the creation method
        original_create_method = config.create_method

        def wrapped_create_method():
            """Wrap the creation method to handle different signatures"""
            try:
                # Try calling with self parameter (regular method)
                original_create_method()
            except TypeError:
                # If that fails, try calling as standalone function with tab_frame
                original_create_method(tab_frame)

        # Set a temporary reference for the creation method to use
        self.parent_gui.current_tab_frame = tab_frame

        # Call the creation method
        wrapped_create_method()

        # Clean up temporary reference
        if hasattr(self.parent_gui, 'current_tab_frame'):
            delattr(self.parent_gui, 'current_tab_frame')

        # Mark as created
        self.created_tabs[config.name] = True

        logger.debug(f"🏗️ Created tab: {config.name}")

    def get_tab(self, name: str) -> Optional[tk.Frame]:
        """Get a tab frame by name"""
        return self.tabs.get(name)

    def get_tab_names(self) -> List[str]:
        """Get list of all tab names"""
        return list(self.tabs.keys())

    def get_created_tabs(self) -> Dict[str, bool]:
        """Get dictionary of tab creation status"""
        return self.created_tabs.copy()

    def tab_exists(self, name: str) -> bool:
        """Check if a tab exists"""
        return name in self.tabs

    def get_tab_count(self) -> int:
        """Get the number of created tabs"""
        return len(self.tabs)

    def refresh_tab(self, name: str) -> bool:
        """
        Refresh a specific tab's content
        Returns True if refresh was successful
        """
        if not self.tab_exists(name):
            logger.warning(f"Cannot refresh non-existent tab: {name}")
            return False

        try:
            config = self.tab_configs.get(name)
            if config and hasattr(self.parent_gui, config.create_method.__name__):
                # For now, just log the refresh request
                # Full refresh logic would need to be implemented per tab
                logger.info(f"🔄 Refresh requested for tab: {name}")
                return True
        except Exception as e:
            logger.error(f"❌ Failed to refresh tab {name}: {e}")
            return False

        return False

    def get_tab_info(self) -> Dict[str, Any]:
        """Get comprehensive information about all tabs"""
        return {
            'total_tabs': len(self.tabs),
            'created_tabs': len([t for t in self.created_tabs.values() if t]),
            'registered_configs': len(self.tab_configs),
            'tab_details': [
                {
                    'name': name,
                    'title': config.title,
                    'priority': config.priority,
                    'created': self.created_tabs.get(name, False)
                }
                for name, config in self.tab_configs.items()
            ]
        }

    def destroy_tab(self, name: str) -> bool:
        """
        Destroy a tab (advanced operation, use with caution)
        Returns True if destruction was successful
        """
        if not self.tab_exists(name):
            return False

        try:
            # Remove from notebook
            tab_index = None
            for i in range(self.notebook.index('end')):
                if self.notebook.tab(i, 'text') == self.tab_configs[name].title:
                    tab_index = i
                    break

            if tab_index is not None:
                self.notebook.forget(tab_index)

            # Destroy the frame
            self.tabs[name].destroy()
            del self.tabs[name]

            logger.info(f"🗑️ Destroyed tab: {name}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to destroy tab {name}: {e}")
            return False
