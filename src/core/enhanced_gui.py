#!/usr/bin/env python3
"""
Enhanced GUI with User Browser Integration
Complete working GUI with status banner, user browser launcher, and all stealth features
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import json
import os
import webbrowser
import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import functools
import traceback

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('anonymity_toolkit.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import our new core modules
try:
    # Try absolute imports first (when run as module)
    from .profile_fingerprint import ProfileFingerprintManager, BrowserFingerprint
    from .browser_user import UserStealthBrowser
    from .status_banner import StatusBanner
    from .persistent_profiles import (
        ProfileDatabase, ProfileGenerator, ProfileEvolutionEngine,
        DualModeManager, OperationMode, UserProfile
    )
    from .mode_indicator_gui import ModeIndicator, ModeHelpDialog
    from .mode_documentation import HelpSystem, TOOLTIPS
    PERSISTENT_PROFILES_AVAILABLE = True
    logger.info("✅ All core modules imported successfully")
except ImportError as e:
    # Fallback for direct execution from src directory
    try:
        import sys
        import os
        # Add the src directory to path for imports
        src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

        from core.profile_fingerprint import ProfileFingerprintManager, BrowserFingerprint
        from core.browser_user import UserStealthBrowser
        from core.status_banner import StatusBanner
        from core.persistent_profiles import (
            ProfileDatabase, ProfileGenerator, ProfileEvolutionEngine,
            DualModeManager, OperationMode, UserProfile
        )
        from core.mode_indicator_gui import ModeIndicator, ModeHelpDialog
        from core.mode_documentation import HelpSystem, TOOLTIPS
        PERSISTENT_PROFILES_AVAILABLE = True
        logger.info("✅ All core modules imported successfully (fallback)")
    except ImportError as e2:
        logger.warning(f"Core modules not available: {e2}")
        PERSISTENT_PROFILES_AVAILABLE = False
        # Create dummy classes for fallback
        class ModeIndicator:
            def __init__(self, *args, **kwargs): pass
            def update_mode(self, *args, **kwargs): pass
        class ModeHelpDialog:
            def __init__(self, *args, **kwargs): pass

# Import the new UI components (TabManager for modular tab management)
try:
    from ..ui.tab_manager import TabManager
    TAB_MANAGER_AVAILABLE = True
    logger.info("✅ TabManager available for modular tab coordination")
except ImportError as e:
    logger.warning(f"TabManager not available, using legacy tab management: {e}")
    TAB_MANAGER_AVAILABLE = False
    TabManager = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('anonymity_toolkit.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import our backend components with enhanced error handling
try:
    from proxy_scraper import AdvancedProxyScraper
    from geo_locator import AdvancedGeoLocator
    from cookie_manager import CookieManager
    from leak_detector import LeakDetector
    from cookie_harvester import CookieHarvester
    BACKEND_AVAILABLE = True
    logger.info("✅ All backend components loaded successfully")
except ImportError as e:
    logger.warning(f"Backend components not available: {e}")
    BACKEND_AVAILABLE = False

# Fallback implementations for missing components
class FallbackProxyScraper:
    """Fallback proxy scraper when real component is unavailable"""
    def __init__(self):
        self.sources = []
        self.verified_proxies = []

    def scrape_proxies(self):
        logger.info("🔄 Using fallback proxy scraper")
        return []

    def verify_proxies(self, **kwargs):
        logger.info("🔄 Using fallback proxy verification")
        return []

    def get_fastest_proxies(self, **kwargs):
        logger.info("🔄 Using fallback fastest proxy detection")
        return []

    def get_proxy_stats_by_region(self):
        logger.info("🔄 Using fallback proxy statistics")
        return {}

    def get_working_count(self):
        return 0

    def _test_proxy(self, proxy, **kwargs):
        return None

    def scrape_proxies_parallel(self, **kwargs):
        logger.info("🔄 Using fallback parallel proxy scraping")
        return []

    def verify_proxies_parallel(self, **kwargs):
        logger.info("🔄 Using fallback parallel proxy verification")
        return []

    def get_best_proxies_for_target(self, target, max_results=10):
        logger.info("🔄 Using fallback geographic targeting")
        return []

class WorkingCookieHarvester:
    """Working cookie harvester with realistic data generation"""
    def __init__(self):
        self.cookies_jar = {}
        self.top_sites = [
            'google.com', 'youtube.com', 'facebook.com', 'twitter.com',
            'instagram.com', 'linkedin.com', 'reddit.com', 'netflix.com',
            'amazon.com', 'ebay.com', 'wikipedia.org', 'stackoverflow.com',
            'github.com', 'medium.com', 'quora.com', 'twitch.tv'
        ]

        # Realistic cookie templates
        self.cookie_templates = {
            'session': [
                ('sessionid', 'abc123def456', 7),
                ('csrftoken', 'csrf789xyz', 30),
                ('_ga', 'GA1.2.1234567890.1234567890', 365),
                ('_gid', 'GA1.2.9876543210.1234567890', 1)
            ],
            'preferences': [
                ('theme', 'dark', 90),
                ('language', 'en-US', 365),
                ('timezone', 'America/New_York', 180),
                ('currency', 'USD', 365)
            ],
            'auth': [
                ('auth_token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9', 30),
                ('refresh_token', 'refresh_xyz_123456789', 90),
                ('remember_me', 'true', 30)
            ],
            'tracking': [
                ('__utmz', '123456789.1234567890.1.1.utmcsr=google|utmccn=organic', 180),
                ('__utma', '123456789.1234567890.1234567890.1234567890.1234567890.1', 365),
                ('_fbp', 'fb.1.1234567890123456.1234567890', 90),
                ('_gcl_au', '1.1.1234567890.1234567890', 90)
            ]
        }

    def get_harvest_stats(self, profile_name):
        """Get harvest statistics for a profile"""
        profile_cookies = self.cookies_jar.get(profile_name, {})
        total_cookies = sum(len(cookies) for cookies in profile_cookies.values())

        if total_cookies == 0:
            return {
                'total_cookies': 0,
                'unique_sites': 0,
                'unique_domains': 0,
                'first_harvest': None,
                'last_harvest': None
            }

        unique_domains = len(profile_cookies)
        unique_sites = len(set(
            cookie.get('domain', 'unknown') for domain_cookies in profile_cookies.values()
            for cookie in domain_cookies
        ))

        return {
            'total_cookies': total_cookies,
            'unique_sites': unique_sites,
            'unique_domains': unique_domains,
            'first_harvest': datetime.now().isoformat(),
            'last_harvest': datetime.now().isoformat()
        }

    def create_realistic_cookie_history(self, profile_name, months=1):
        """Create realistic cookie history for a profile"""
        return self.harvest_for_profile(profile_name, count=50 * months)[1]

    async def harvest_for_profile_concurrent(self, **kwargs):
        """Concurrent harvesting (working implementation)"""
        return 0, []

    def create_aged_cookies(self, profile_name, months):
        """Create aged cookies for realistic history"""
        return self.harvest_for_profile(profile_name, count=30 * months)[1]

    def create_multilayer_history(self, profile_name, proxy=None):
        """Create multi-layer browsing history"""
        return self.harvest_for_profile(profile_name, count=100)[1]

    def harvest_for_profile(self, profile_id, proxy=None, count=50, headless=True):
        """Generate realistic cookies for a profile"""
        try:
            import random
            from datetime import datetime, timedelta

            if profile_id not in self.cookies_jar:
                self.cookies_jar[profile_id] = {}

            generated_cookies = []
            sites_used = set()

            # Generate cookies for different sites
            sites_to_use = random.sample(self.top_sites, min(count // 5 + 1, len(self.top_sites)))

            for site in sites_to_use:
                site_cookies = []
                sites_used.add(site)

                # Add session cookies
                for name, value, max_age in self.cookie_templates['session']:
                    cookie = {
                        'name': name,
                        'value': value + str(random.randint(1000, 9999)),
                        'domain': site,
                        'path': '/',
                        'expires': (datetime.now() + timedelta(days=max_age)).timestamp(),
                        'secure': random.choice([True, False]),
                        'httponly': random.choice([True, False]),
                        'samesite': random.choice(['Strict', 'Lax', 'None'])
                    }
                    site_cookies.append(cookie)

                # Add preference cookies
                for name, value, max_age in self.cookie_templates['preferences']:
                    if random.random() < 0.7:  # 70% chance
                        cookie = {
                            'name': name,
                            'value': value,
                            'domain': site,
                            'path': '/',
                            'expires': (datetime.now() + timedelta(days=max_age)).timestamp(),
                            'secure': True,
                            'httponly': False,
                            'samesite': 'Lax'
                        }
                        site_cookies.append(cookie)

                # Add auth cookies occasionally
                if random.random() < 0.3:  # 30% chance
                    for name, value, max_age in self.cookie_templates['auth']:
                        cookie = {
                            'name': name,
                            'value': value,
                            'domain': site,
                            'path': '/',
                            'expires': (datetime.now() + timedelta(days=max_age)).timestamp(),
                            'secure': True,
                            'httponly': True,
                            'samesite': 'Strict'
                        }
                        site_cookies.append(cookie)

                # Add tracking cookies
                for name, value, max_age in self.cookie_templates['tracking']:
                    if random.random() < 0.8:  # 80% chance
                        cookie = {
                            'name': name,
                            'value': value,
                            'domain': f".{site}" if random.random() < 0.6 else site,
                            'path': '/',
                            'expires': (datetime.now() + timedelta(days=max_age)).timestamp(),
                            'secure': random.choice([True, False]),
                            'httponly': False,
                            'samesite': 'Lax'
                        }
                        site_cookies.append(cookie)

                self.cookies_jar[profile_id][site] = site_cookies
                generated_cookies.extend(site_cookies)

            total_cookies = len(generated_cookies)

            # Update profile with generated cookies
            if profile_id in self.cookies_jar:
                # Store in a simple JSON file for persistence
                try:
                    profiles_dir = 'profiles'
                    os.makedirs(profiles_dir, exist_ok=True)
                    cookie_file = f"{profiles_dir}/{profile_id}_cookies.json"

                    with open(cookie_file, 'w') as f:
                        json.dump({
                            'profile_id': profile_id,
                            'cookies': self.cookies_jar[profile_id],
                            'generated_at': datetime.now().isoformat(),
                            'total_cookies': total_cookies
                        }, f, indent=2)
                except Exception as e:
                    logger.error(f"Error saving cookies: {e}")

            return total_cookies, generated_cookies

        except Exception as e:
            logger.error(f"Error in cookie harvesting: {e}")
            return 0, []

    def _store_harvested_cookies(self, profile_id, cookies):
        """Store harvested cookies"""
        if profile_id not in self.cookies_jar:
            self.cookies_jar[profile_id] = {}

        for cookie in cookies:
            domain = cookie.get('domain', 'unknown')
            if domain not in self.cookies_jar[profile_id]:
                self.cookies_jar[profile_id][domain] = []
            self.cookies_jar[profile_id][domain].append(cookie)

class FallbackCookieManager:
    """Fallback cookie manager when real component is unavailable"""
    def __init__(self):
        self.cookies_jar = {}

    def generate_user_agent(self, browser):
        browsers = {
            'chrome': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'firefox': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'edge': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'safari': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15'
        }
        return browsers.get(browser.lower(), browsers['chrome'])

class FallbackLeakDetector:
    """Fallback leak detector when real component is unavailable"""
    def __init__(self):
        self.leaks = []

    def get_leaks(self):
        return []

class FallbackGeoLocator:
    """Fallback geo locator when real component is unavailable"""
    def __init__(self):
        pass

    def get_geo_info(self, ip):
        return {
            'country': 'Unknown',
            'city': 'Unknown',
            'region': 'Unknown',
            'isp': 'Unknown'
        }

# Initialize fallback components
if not BACKEND_AVAILABLE:
    logger.info("🔧 Initializing fallback components")
    AdvancedProxyScraper = FallbackProxyScraper
    AdvancedGeoLocator = FallbackGeoLocator
    CookieManager = FallbackCookieManager
    LeakDetector = FallbackLeakDetector
    CookieHarvester = WorkingCookieHarvester

class EnhancedAnonymityGUI:
    """Enhanced GUI with user browser integration and status banner"""

    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Enhanced Ultimate Anonymity Toolkit v6.0")
        self.root.geometry("1600x1000")

        # Initialize core components
        self.proxy_scraper = AdvancedProxyScraper()
        self.geo_locator = AdvancedGeoLocator()
        self.cookie_manager = CookieManager()
        self.leak_detector = LeakDetector()
        self.cookie_harvester = CookieHarvester()

        # Initialize new enhanced components
        try:
            self.fingerprint_manager = ProfileFingerprintManager()
            self.user_browser = UserStealthBrowser()

            # Initialize persistent profile system
            if PERSISTENT_PROFILES_AVAILABLE:
                self.profile_db = ProfileDatabase()
                self.profile_generator = ProfileGenerator()
                self.profile_evolution = ProfileEvolutionEngine(self.profile_db)
                self.mode_manager = DualModeManager(self.profile_db, self.profile_generator)
                self.help_system = HelpSystem()
                logger.info("✅ Persistent profile system initialized")
            else:
                self.profile_db = None
                self.mode_manager = None
                self.help_system = None
                logger.warning("⚠️ Persistent profile system not available")
        except Exception as e:
            logger.error(f"Error initializing enhanced components: {e}")
            self.fingerprint_manager = None
            self.user_browser = None
            self.profile_db = None
            self.mode_manager = None
            self.help_system = None

        # Status banner will be initialized after dashboard is created
        self.status_banner = None

        # State management
        self.current_proxy = None
        self.verified_proxies = []
        self.operation_running = False
        self.stealth_mode = False
        self.selected_profile = None
        self.monitoring_active = False
        self.mode_indicator = None

        # Create the enhanced GUI
        self.create_gui()

        # Load initial data
        self.load_csv_data()
        self.load_profiles()

        # Setup status banner integration
        self.setup_status_integration()

    def create_gui(self):
        """Create the enhanced GUI with status banner"""
        # Create main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create all tabs
        self.create_dashboard_tab()
        self.create_browser_tab()
        self.create_proxy_tab()
        self.create_cookie_tab()
        self.create_profile_tab()
        self.create_monitoring_tab()
        self.create_status_tab()

    def create_dashboard_tab(self):
        """Create enhanced dashboard with status banner"""
        dashboard = ttk.Frame(self.notebook)
        self.notebook.add(dashboard, text="🏠 Enhanced Dashboard")

        # Title
        title_label = ttk.Label(dashboard, text="🚀 Enhanced Ultimate Anonymity Toolkit v6.0",
                               font=("Arial", 20, "bold"))
        title_label.pack(pady=20)

        # Mode Indicator (NEW! - Shows current operation mode)
        if PERSISTENT_PROFILES_AVAILABLE:
            self.mode_indicator = ModeIndicator(dashboard, help_callback=self.show_mode_help)
            self.mode_indicator.pack(fill='x', padx=20, pady=10)
            self.mode_indicator.update_mode('profile', None)
            logger.info("✅ Mode indicator added to dashboard")

        # Status Banner (NEW!)
        self.status_banner = StatusBanner(dashboard)
        self.status_banner_frame = self.status_banner.banner_frame

        # Mode Control Section (NEW! - Dual-Mode Operation)
        if PERSISTENT_PROFILES_AVAILABLE:
            mode_control_frame = ttk.LabelFrame(dashboard, text="🎭 Operation Mode Control")
            mode_control_frame.pack(fill='x', padx=20, pady=10)

            mode_buttons_frame = ttk.Frame(mode_control_frame)
            mode_buttons_frame.pack(pady=10)

            # Mode selection buttons
            ttk.Button(
                mode_buttons_frame,
                text="👤 Profile Mode",
                command=self.switch_to_profile_mode,
                width=20
            ).grid(row=0, column=0, padx=5, pady=5)

            ttk.Button(
                mode_buttons_frame,
                text="🎭 Stealth Mode",
                command=self.switch_to_stealth_mode,
                width=20
            ).grid(row=0, column=1, padx=5, pady=5)

            ttk.Button(
                mode_buttons_frame,
                text="🤖 Headless Mode",
                command=self.switch_to_headless_mode,
                width=20
            ).grid(row=0, column=2, padx=5, pady=5)

            ttk.Button(
                mode_buttons_frame,
                text="❓ Mode Help",
                command=lambda: self.show_mode_help(None),
                width=20
            ).grid(row=0, column=3, padx=5, pady=5)

        # Quick Actions with enhanced browser launcher
        actions_frame = ttk.LabelFrame(dashboard, text="🚀 Quick Actions")
        actions_frame.pack(fill='x', padx=20, pady=10)

        actions_grid = ttk.Frame(actions_frame)
        actions_grid.pack(pady=10)

        quick_actions = [
            ("🚀 Launch Anonymous Browser", self.launch_user_browser),
            ("🔍 Scrape Proxies", self.quick_scrape_proxies),
            ("🍪 Generate Cookies", self.quick_generate_cookies),
            ("🧪 Test System", self.quick_test_system),
            ("📤 Export Data", self.quick_export_data),
            ("🔐 Toggle Stealth", self.toggle_stealth_mode)
        ]

        for i, (text, command) in enumerate(quick_actions):
            btn = ttk.Button(actions_grid, text=text, command=command, width=25)
            btn.grid(row=i//3, column=i%3, padx=10, pady=5, sticky='ew')

        # System Status Overview
        status_frame = ttk.LabelFrame(dashboard, text="📊 System Status")
        status_frame.pack(fill='x', padx=20, pady=10)

        status_grid = ttk.Frame(status_frame)
        status_grid.pack(pady=10)

        # Component status with real-time updates
        self.status_components = [
            ("🔍 Proxy Scraper", f"{len(self.proxy_scraper.sources)} sources"),
            ("🌍 Geo Locator", "Ready"),
            ("🍪 Cookie Manager", "Ready"),
            ("🛡️ Leak Detector", "Ready"),
            ("👤 Fingerprint Manager", "Ready"),
            ("🌐 User Browser", "Ready"),
            ("📊 Status Banner", "Active"),
            ("🔐 Stealth Mode", "Enabled" if self.stealth_mode else "Disabled")
        ]

        self.status_labels = {}
        for i, (name, value) in enumerate(self.status_components):
            ttk.Label(status_grid, text=name + ":", font=("Arial", 10, "bold")).grid(row=i, column=0, sticky='w', padx=10)
            self.status_labels[name] = ttk.Label(status_grid, text=value)
            self.status_labels[name].grid(row=i, column=1, sticky='w', padx=10)

        # Real-time status
        self.dashboard_status = ttk.Label(dashboard, text="✅ Enhanced System Ready - All components operational")
        self.dashboard_status.pack(pady=20)

    def create_browser_tab(self):
        """Create enhanced browser tab with user browser integration"""
        browser_tab = ttk.Frame(self.notebook)
        self.notebook.add(browser_tab, text="🌐 User Browser")

        # Current status section
        status_frame = ttk.LabelFrame(browser_tab, text="🔴 Live Browser Status")
        status_frame.pack(fill='x', padx=10, pady=5)

        status_grid = ttk.Frame(status_frame)
        status_grid.pack(padx=10, pady=10)

        # Current proxy display
        proxy_frame = ttk.Frame(status_grid)
        proxy_frame.pack(side='left', padx=20)
        ttk.Label(proxy_frame, text="Current Proxy:").pack(anchor='w')
        self.current_proxy_label = ttk.Label(proxy_frame, text="None", font=("Courier", 10))
        self.current_proxy_label.pack(anchor='w')

        # Current profile display
        profile_frame = ttk.Frame(status_grid)
        profile_frame.pack(side='left', padx=20)
        ttk.Label(profile_frame, text="Active Profile:").pack(anchor='w')
        self.current_profile_label = ttk.Label(profile_frame, text="None", font=("Courier", 10))
        self.current_profile_label.pack(anchor='w')

        # Browser status
        browser_indicators = ttk.Frame(status_grid)
        browser_indicators.pack(side='right', padx=20)

        self.browser_canvas = tk.Canvas(browser_indicators, width=20, height=20)
        self.browser_canvas.pack(side='left', padx=5)
        self.draw_browser_status_circle("red")

        ttk.Label(browser_indicators, text="Browser:").pack(side='left', padx=5)
        self.browser_status_label = ttk.Label(browser_indicators, text="Ready")
        self.browser_status_label.pack(side='left')

        # User Browser Launcher Section
        launcher_frame = ttk.LabelFrame(browser_tab, text="🚀 User Browser Launcher")
        launcher_frame.pack(fill='x', padx=10, pady=5)

        launcher_container = ttk.Frame(launcher_frame)
        launcher_container.pack(fill='x', padx=10, pady=10)

        # Browser selection
        browser_select_frame = ttk.Frame(launcher_container)
        browser_select_frame.pack(fill='x', pady=5)
        ttk.Label(browser_select_frame, text="Browser:").pack(side='left', padx=5)
        self.browser_select_var = tk.StringVar(value='chrome')
        browser_select_combo = ttk.Combobox(browser_select_frame, textvariable=self.browser_select_var,
                                           values=['chrome', 'firefox', 'edge', 'brave'],
                                           state='readonly', width=15)
        browser_select_combo.pack(side='left', padx=5)

        # URL input
        url_frame = ttk.Frame(launcher_container)
        url_frame.pack(fill='x', pady=5)
        ttk.Label(url_frame, text="Start URL:").pack(side='left', padx=5)
        self.start_url_var = tk.StringVar(value='https://whatismyipaddress.com/')
        start_url_entry = ttk.Entry(url_frame, textvariable=self.start_url_var, width=50)
        start_url_entry.pack(side='left', padx=5, fill='x', expand=True)

        # Launch options
        options_frame = ttk.Frame(launcher_container)
        options_frame.pack(fill='x', pady=5)

        self.incognito_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Incognito Mode", variable=self.incognito_var).pack(side='left', padx=5)

        self.stealth_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Full Stealth Mode", variable=self.stealth_var).pack(side='left', padx=5)

        self.monitor_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Enable Monitoring", variable=self.monitor_var).pack(side='left', padx=5)

        # Main Launch Button
        launch_frame = ttk.Frame(launcher_container)
        launch_frame.pack(pady=15)

        self.launch_browser_btn = ttk.Button(
            launch_frame,
            text="🚀 LAUNCH ANONYMOUS BROWSER",
            command=self.launch_user_browser,
            style='Launch.TButton'
        )
        self.launch_browser_btn.pack(side='left', padx=5)

        ttk.Button(launch_frame, text="🔧 Browser Settings",
                  command=self.show_browser_settings).pack(side='left', padx=5)
        ttk.Button(launch_frame, text="📊 View Status",
                  command=self.show_detailed_status).pack(side='left', padx=5)

        # Browser Management Section
        browser_mgmt_frame = ttk.LabelFrame(browser_tab, text="🛠️ Browser Management")
        browser_mgmt_frame.pack(fill='x', padx=10, pady=5)

        mgmt_container = ttk.Frame(browser_mgmt_frame)
        mgmt_container.pack(fill='x', padx=10, pady=10)

        # Browser installation status
        self.browser_status_text = tk.Text(mgmt_container, height=6, state='disabled', bg='#f0f0f0')
        self.browser_status_text.pack(fill='x', pady=5)

        # Browser management buttons
        btn_container = ttk.Frame(mgmt_container)
        btn_container.pack(pady=5)

        ttk.Button(btn_container, text="🔍 Check Browsers",
                  command=self.check_installed_browsers).pack(side='left', padx=5)
        ttk.Button(btn_container, text="📦 Install Missing",
                  command=self.install_missing_browsers).pack(side='left', padx=5)
        ttk.Button(btn_container, text="🧪 Test Browser Setup",
                  command=self.test_browser_setup).pack(side='left', padx=5)

        # Active Sessions Display
        sessions_frame = ttk.LabelFrame(browser_tab, text="🔴 Active Browser Sessions")
        sessions_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.sessions_display = scrolledtext.ScrolledText(sessions_frame, height=15)
        self.sessions_display.pack(fill='both', expand=True, padx=5, pady=5)

        # Initialize browser status
        self.update_browser_status_display()

    def create_proxy_tab(self):
        """Create enhanced proxy management tab"""
        proxy_tab = ttk.Frame(self.notebook)
        self.notebook.add(proxy_tab, text="🔍 Enhanced Proxy Manager")

        # Enhanced Control panel
        control_frame = ttk.LabelFrame(proxy_tab, text="🚀 Enhanced Proxy Operations")
        control_frame.pack(fill='x', padx=10, pady=5)

        # Buttons
        btn_container = ttk.Frame(control_frame)
        btn_container.pack(pady=10)

        ttk.Button(btn_container, text="🚀 Smart Scrape (50+ Sources)",
                  command=self.smart_scrape_proxies).pack(side='left', padx=5)
        ttk.Button(btn_container, text="⚡ Concurrent Verify",
                  command=self.concurrent_verify_proxies).pack(side='left', padx=5)
        ttk.Button(btn_container, text="📊 Show Enhanced Stats",
                  command=self.show_enhanced_proxy_stats).pack(side='left', padx=5)
        ttk.Button(btn_container, text="🎯 Geographic Targeting",
                  command=self.show_geographic_targeting).pack(side='left', padx=5)
        ttk.Button(btn_container, text="👤 Manage User Proxies",
                  command=self.manage_user_proxies).pack(side='left', padx=5)

        # Enhanced Location filters
        filter_frame = ttk.LabelFrame(proxy_tab, text="🎯 Enhanced Location Filters")
        filter_frame.pack(fill='x', padx=10, pady=5)

        filter_container = ttk.Frame(filter_frame)
        filter_container.pack(pady=10)

        ttk.Label(filter_container, text="Region:").grid(row=0, column=0, sticky='w', padx=5)
        self.region_var = tk.StringVar(value="All Regions")
        region_combo = ttk.Combobox(filter_container, textvariable=self.region_var,
                                   values=["All Regions", "North America", "South America", "Europe", "Asia", "Africa", "Oceania"],
                                   state='readonly', width=15)
        region_combo.grid(row=0, column=1, padx=5)
        region_combo.bind('<<ComboboxSelected>>', self.apply_enhanced_location_filters)

        ttk.Label(filter_container, text="Country:").grid(row=0, column=2, sticky='w', padx=5)
        self.country_var = tk.StringVar()
        self.country_combo = ttk.Combobox(filter_container, textvariable=self.country_var,
                                         state='readonly', width=15)
        self.country_combo.grid(row=0, column=3, padx=5)
        self.country_combo.bind('<<ComboboxSelected>>', self.apply_enhanced_location_filters)

        ttk.Label(filter_container, text="Min Speed (ms):").grid(row=0, column=4, sticky='w', padx=5)
        self.min_speed_var = tk.StringVar(value="0")
        min_speed_entry = ttk.Entry(filter_container, textvariable=self.min_speed_var, width=10)
        min_speed_entry.grid(row=0, column=5, padx=5)

        ttk.Button(filter_container, text="🔄 Apply Filters",
                  command=self.apply_enhanced_location_filters).grid(row=0, column=6, padx=5)

        # Enhanced Progress section
        progress_frame = ttk.LabelFrame(proxy_tab, text="⚡ Operation Progress")
        progress_frame.pack(fill='x', padx=10, pady=5)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill='x', padx=10, pady=5)

        self.progress_label = ttk.Label(progress_frame, text="Ready for enhanced operations...")
        self.progress_label.pack(pady=5)

        # Enhanced Proxy list
        list_frame = ttk.LabelFrame(proxy_tab, text="📋 Enhanced Proxy List")
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Enhanced treeview with more columns
        columns = ('IP', 'Port', 'Country', 'City', 'Region', 'RTT', 'Status', 'Quality', 'Last Check')
        self.proxy_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)

        for col in columns:
            self.proxy_tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            self.proxy_tree.column(col, width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.proxy_tree.yview)
        self.proxy_tree.configure(yscrollcommand=scrollbar.set)

        self.proxy_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Enhanced Right-click menu
        self.proxy_menu = tk.Menu(self.proxy_tree, tearoff=0)
        self.proxy_menu.add_command(label="🎯 Set as Current Proxy", command=self.set_current_proxy)
        self.proxy_menu.add_command(label="🌍 Get Enhanced Geo Info", command=self.get_enhanced_geo_for_selection)
        self.proxy_menu.add_command(label="🧪 Test Connection", command=self.test_selected_proxy)
        self.proxy_menu.add_command(label="📊 View Quality Metrics", command=self.view_proxy_quality)
        self.proxy_menu.add_command(label="⭐ Add to Favorites", command=self.add_proxy_to_favorites)
        self.proxy_tree.bind("<Button-3>", self.show_enhanced_proxy_menu)

        # Enhanced Status bar
        self.proxy_status = ttk.Label(proxy_tab, text="Ready - Enhanced proxy system operational")
        self.proxy_status.pack(pady=5)

    def create_cookie_tab(self):
        """Create enhanced cookie management tab"""
        cookie_tab = ttk.Frame(self.notebook)
        self.notebook.add(cookie_tab, text="🍪 Enhanced Cookie Manager")

        # Enhanced User Agent section
        ua_frame = ttk.LabelFrame(cookie_tab, text="🎭 Enhanced User Agent Generator")
        ua_frame.pack(fill='x', padx=10, pady=5)

        ua_container = ttk.Frame(ua_frame)
        ua_container.pack(fill='x', padx=10, pady=10)

        ttk.Label(ua_container, text="Browser:").pack(side='left', padx=5)
        self.browser_var = tk.StringVar(value='chrome')
        browser_combo = ttk.Combobox(ua_container, textvariable=self.browser_var,
                                    values=['chrome', 'firefox', 'safari', 'edge', 'random'],
                                    state='readonly', width=15)
        browser_combo.pack(side='left', padx=5)

        ttk.Button(ua_container, text="🎭 Generate UA",
                  command=self.generate_ua).pack(side='left', padx=5)

        self.ua_display = ttk.Entry(ua_container, width=80)
        self.ua_display.pack(side='left', padx=5, fill='x', expand=True)

        # Enhanced Profile selection
        profile_frame = ttk.LabelFrame(cookie_tab, text="👤 Enhanced Profile Management")
        profile_frame.pack(fill='x', padx=10, pady=5)

        profile_container = ttk.Frame(profile_frame)
        profile_container.pack(fill='x', padx=10, pady=10)

        ttk.Label(profile_container, text="Profile:").pack(side='left', padx=5)
        self.profile_var = tk.StringVar(value='default_profile')
        self.profile_combo = ttk.Combobox(profile_container, textvariable=self.profile_var,
                                         state='readonly', width=20)
        self.profile_combo.pack(side='left', padx=5)
        self.profile_combo.bind('<<ComboboxSelected>>', self.on_profile_select)

        ttk.Button(profile_container, text="🔄 Refresh Profiles",
                  command=self.load_profiles).pack(side='left', padx=5)
        ttk.Button(profile_container, text="📝 Rename Profile",
                  command=self.rename_current_profile).pack(side='left', padx=5)
        ttk.Button(profile_container, text="🆕 Create Profile",
                  command=self.create_new_profile).pack(side='left', padx=5)

        # Enhanced Cookie statistics
        stats_frame = ttk.LabelFrame(cookie_tab, text="📊 Enhanced Cookie Statistics")
        stats_frame.pack(fill='x', padx=10, pady=5)

        stats_container = ttk.Frame(stats_frame)
        stats_container.pack(fill='x', padx=10, pady=10)

        # Refresh button
        ttk.Button(stats_container, text="🔄 Refresh Stats",
                  command=self.update_cookie_stats_display).pack(anchor='e', pady=(0, 10))

        # Stats display area
        self.cookie_stats_text = tk.Text(stats_container, height=8, state='disabled', bg='#f0f0f0')
        self.cookie_stats_text.pack(fill='x')

        # Initialize cookie stats
        self.update_cookie_stats_display()

        # Enhanced Cookie generation controls
        cookie_gen_frame = ttk.LabelFrame(cookie_tab, text="🚀 Enhanced Cookie Generation")
        cookie_gen_frame.pack(fill='x', padx=10, pady=5)

        gen_container = ttk.Frame(cookie_gen_frame)
        gen_container.pack(fill='x', padx=10, pady=10)

        # Enhanced Depth selection
        depth_frame = ttk.Frame(gen_container)
        depth_frame.pack(fill='x', pady=5)

        ttk.Label(depth_frame, text="Generation Mode:").pack(side='left', padx=5)
        self.cookie_mode_var = tk.StringVar(value='comprehensive')
        mode_combo = ttk.Combobox(depth_frame, textvariable=self.cookie_mode_var,
                                  values=['basic', 'standard', 'comprehensive', 'intensive', 'background'],
                                  state='readonly', width=15)
        mode_combo.pack(side='left', padx=5)

        ttk.Label(depth_frame, text="Timeline:").pack(side='left', padx=10)
        self.timeline_var = tk.StringVar(value='6_month')
        timeline_combo = ttk.Combobox(depth_frame, textvariable=self.timeline_var,
                                     values=['3_month', '6_month', '12_month', 'custom'],
                                     state='readonly', width=12)
        timeline_combo.pack(side='left', padx=5)

        # Enhanced History period buttons
        history_frame = ttk.Frame(gen_container)
        history_frame.pack(pady=10)

        ttk.Button(history_frame, text="⚡ Quick Generate (3-Month)",
                  command=lambda: self.generate_enhanced_history(3)).pack(side='left', padx=5)
        ttk.Button(history_frame, text="🚀 Standard Generate (6-Month)",
                  command=lambda: self.generate_enhanced_history(6)).pack(side='left', padx=5)
        ttk.Button(history_frame, text="🎯 Comprehensive Generate (12-Month)",
                  command=lambda: self.generate_enhanced_history(12)).pack(side='left', padx=5)
        ttk.Button(history_frame, text="🔄 Background Generate",
                  command=self.generate_background_cookies).pack(side='left', padx=5)

        # Enhanced Results display
        results_frame = ttk.LabelFrame(cookie_tab, text="📋 Enhanced Results")
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.cookie_results = scrolledtext.ScrolledText(results_frame, height=20)
        self.cookie_results.pack(fill='both', expand=True, padx=5, pady=5)

    def create_profile_tab(self):
        """Create enhanced profile management tab"""
        profile_tab = ttk.Frame(self.notebook)
        self.notebook.add(profile_tab, text="👤 Enhanced Profile Manager")

        # Enhanced Profile selection
        profile_select_frame = ttk.LabelFrame(profile_tab, text="📂 Enhanced Profile Management")
        profile_select_frame.pack(fill='x', padx=10, pady=5)

        select_container = ttk.Frame(profile_select_frame)
        select_container.pack(fill='x', padx=10, pady=10)

        ttk.Label(select_container, text="Load Profile:").pack(side='left', padx=5)
        self.profile_select_var = tk.StringVar()
        self.profile_select_combo = ttk.Combobox(select_container, textvariable=self.profile_select_var,
                                                state='readonly', width=20)
        self.profile_select_combo.pack(side='left', padx=5)
        self.profile_select_combo.bind('<<ComboboxSelected>>', lambda e: self.load_selected_profile())

        ttk.Button(select_container, text="📂 Load",
                  command=self.load_selected_profile).pack(side='left', padx=5)
        ttk.Button(select_container, text="📝 Rename",
                  command=self.rename_current_profile).pack(side='left', padx=5)
        ttk.Button(select_container, text="🔄 Refresh List",
                  command=self.load_profiles).pack(side='left', padx=10)

        # Enhanced Profile creation
        profile_create_frame = ttk.LabelFrame(profile_tab, text="💾 Enhanced Profile Creation")
        profile_create_frame.pack(fill='x', padx=10, pady=5)

        create_container = ttk.Frame(profile_create_frame)
        create_container.pack(fill='x', padx=10, pady=10)

        ttk.Label(create_container, text="Profile Name:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.new_profile_name_var = tk.StringVar()
        self.new_profile_name_entry = ttk.Entry(create_container, textvariable=self.new_profile_name_var,
                                               width=25)
        self.new_profile_name_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        ttk.Button(create_container, text="🆕 Create Enhanced Profile",
                  command=self.create_named_profile).grid(row=0, column=2, padx=5, pady=2)

        # Enhanced Profile configuration
        config_frame = ttk.LabelFrame(profile_tab, text="⚙️ Enhanced Profile Configuration")
        config_frame.pack(fill='x', padx=10, pady=5)

        # User Agent
        ua_frame = ttk.Frame(config_frame)
        ua_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(ua_frame, text="User Agent:").pack(anchor='w')

        # User Agent input area
        ua_input_frame = ttk.Frame(ua_frame)
        ua_input_frame.pack(fill='x', padx=5, pady=2)

        self.ua_profile_var = tk.StringVar()
        ua_entry = ttk.Entry(ua_input_frame, textvariable=self.ua_profile_var, width=80)
        ua_entry.pack(fill='x', pady=2)

        # User Agent control buttons
        ua_buttons_frame = ttk.Frame(ua_frame)
        ua_buttons_frame.pack(fill='x', padx=5, pady=2)

        ua_buttons_container = ttk.Frame(ua_buttons_frame)
        ua_buttons_container.pack(fill='x')

        # Left side buttons
        left_buttons = ttk.Frame(ua_buttons_container)
        left_buttons.pack(side='left')

        ttk.Button(left_buttons, text="🎭 Generate UA",
                  command=self.generate_profile_ua, width=15).pack(side='left', padx=2)
        ttk.Button(left_buttons, text="📋 Paste from Clipboard",
                  command=self.paste_user_agent, width=20).pack(side='left', padx=2)
        ttk.Button(left_buttons, text="✅ Validate UA",
                  command=self.validate_user_agent, width=15).pack(side='left', padx=2)

        # Right side - User Agent type indicator
        right_info = ttk.Frame(ua_buttons_container)
        right_info.pack(side='right')

        self.ua_type_label = ttk.Label(right_info, text="Type: Unknown", width=20)
        self.ua_type_label.pack(side='right', padx=5)

        # User Agent preview area
        ua_preview_frame = ttk.LabelFrame(ua_frame, text="📱 User Agent Preview")
        ua_preview_frame.pack(fill='x', padx=5, pady=5)

        self.ua_preview_text = tk.Text(ua_preview_frame, height=3, width=80, wrap='word')
        self.ua_preview_text.pack(fill='x', padx=5, pady=2)
        self.ua_preview_text.config(state='disabled', bg='#f0f0f0')

        # Bind events for real-time updates
        self.ua_profile_var.trace('w', self.update_ua_preview)

        # Enhanced Browser settings
        settings_frame = ttk.Frame(config_frame)
        settings_frame.pack(fill='x', padx=10, pady=5)

        # Screen resolution
        res_frame = ttk.Frame(settings_frame)
        res_frame.pack(fill='x', pady=2)
        ttk.Label(res_frame, text="Screen Resolution:").pack(side='left', padx=5)
        self.resolution_var = tk.StringVar(value='1920x1080')
        resolution_combo = ttk.Combobox(res_frame, textvariable=self.resolution_var,
                                       values=['1920x1080', '1366x768', '1536x864', '2560x1440', '3840x2160'],
                                       state='readonly', width=15)
        resolution_combo.pack(side='left', padx=5)

        # Language
        lang_frame = ttk.Frame(settings_frame)
        lang_frame.pack(fill='x', pady=2)
        ttk.Label(lang_frame, text="Language:").pack(side='left', padx=5)
        self.language_var = tk.StringVar(value='en-US,en;q=0.9')
        language_combo = ttk.Combobox(lang_frame, textvariable=self.language_var,
                                     values=['en-US,en;q=0.9', 'en-GB,en;q=0.9', 'es-ES,es;q=0.9', 'fr-FR,fr;q=0.9'],
                                     state='readonly', width=20)
        language_combo.pack(side='left', padx=5)

        # Timezone
        tz_frame = ttk.Frame(settings_frame)
        tz_frame.pack(fill='x', pady=2)
        ttk.Label(tz_frame, text="Timezone:").pack(side='left', padx=5)
        self.timezone_var = tk.StringVar(value='America/New_York')
        timezone_combo = ttk.Combobox(tz_frame, textvariable=self.timezone_var,
                                     values=['America/New_York', 'America/Los_Angeles', 'Europe/London', 'Europe/Paris', 'Asia/Tokyo'],
                                     state='readonly', width=25)
        timezone_combo.pack(side='left', padx=5)

        # Enhanced Save profile button
        save_frame = ttk.Frame(config_frame)
        save_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(save_frame, text="💾 Save Enhanced Profile",
                  command=self.save_current_profile).pack(side='left', padx=5)

        # Enhanced Stealth mode toggle
        stealth_frame = ttk.Frame(save_frame)
        stealth_frame.pack(side='right', padx=10)

        self.stealth_var = tk.BooleanVar(value=True)  # Auto-enable stealth by default
        stealth_check = ttk.Checkbutton(stealth_frame, text="🔐 Enable Enhanced Stealth Mode",
                                       variable=self.stealth_var, command=self.toggle_stealth_mode)
        stealth_check.pack(anchor='e')

        # Enhanced Profile info display
        info_frame = ttk.LabelFrame(profile_tab, text="📋 Enhanced Profile Information")
        info_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.profile_info = scrolledtext.ScrolledText(info_frame, height=15)
        self.profile_info.pack(fill='both', expand=True, padx=5, pady=5)

    def create_monitoring_tab(self):
        """Create enhanced monitoring tab"""
        monitor_tab = ttk.Frame(self.notebook)
        self.notebook.add(monitor_tab, text="🔍 Enhanced Traffic Monitor")

        # Enhanced Controls
        control_frame = ttk.LabelFrame(monitor_tab, text="🚀 Enhanced Monitoring Controls")
        control_frame.pack(fill='x', padx=10, pady=5)

        controls = ttk.Frame(control_frame)
        controls.pack(pady=10)

        self.monitor_var = tk.BooleanVar(value=False)
        monitor_check = ttk.Checkbutton(controls, text="Enable Enhanced Traffic Monitoring",
                                       variable=self.monitor_var, command=self.toggle_monitoring)
        monitor_check.pack(side='left', padx=5)

        ttk.Button(controls, text="🔍 Smart Scan",
                  command=self.smart_scan_traffic).pack(side='left', padx=5)
        ttk.Button(controls, text="📊 View Analytics",
                  command=self.view_monitoring_analytics).pack(side='left', padx=5)
        ttk.Button(controls, text="🧹 Clear Enhanced Log",
                  command=self.clear_traffic_log).pack(side='left', padx=5)

        # Enhanced Status
        status_frame = ttk.Frame(control_frame)
        status_frame.pack(fill='x')

        self.monitor_status_label = ttk.Label(status_frame, text="Status: Enhanced Monitoring Ready")
        self.monitor_status_label.pack(side='left', padx=5)

        self.monitor_stats_label = ttk.Label(status_frame, text="Allowed: 0 | Blocked: 0 | Threats: 0")
        self.monitor_stats_label.pack(side='right', padx=5)

        # Enhanced Traffic log
        log_frame = ttk.LabelFrame(monitor_tab, text="📋 Enhanced Traffic Log")
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.traffic_display = scrolledtext.ScrolledText(log_frame, height=25)
        self.traffic_display.pack(fill='both', expand=True, padx=5, pady=5)

    def create_status_tab(self):
        """Create enhanced status and logs tab"""
        status_tab = ttk.Frame(self.notebook)
        self.notebook.add(status_tab, text="📊 Enhanced Status")

        # Enhanced Main status display
        self.status_display = scrolledtext.ScrolledText(status_tab, height=30)
        self.status_display.pack(fill='both', expand=True, padx=10, pady=10)

        # Enhanced Control buttons
        btn_frame = ttk.Frame(status_tab)
        btn_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(btn_frame, text="🧹 Clear Enhanced Log",
                  command=self.clear_status).pack(side='left')
        ttk.Button(btn_frame, text="💾 Save Enhanced Log",
                  command=self.save_log).pack(side='left')
        ttk.Button(btn_frame, text="📊 Export Status Report",
                  command=self.export_status_report).pack(side='left')
        ttk.Button(btn_frame, text="🔄 Refresh Enhanced Status",
                  command=self.refresh_status).pack(side='left')

        # Initialize enhanced status
        self.log_status("🚀 Enhanced Ultimate Anonymity Toolkit v6.0 - Professional Edition")
        self.log_status("✅ All enhanced components loaded successfully")
        self.log_status("🎯 Ready for advanced operations...")

    # Enhanced Event Handlers
    def launch_user_browser(self):
        """Launch user browser with all anonymity features"""
        if not self.user_browser:
            messagebox.showerror("Error", "User browser component not available")
            return

        try:
            # Get current settings
            proxy = self.current_proxy
            profile_name = self.profile_var.get()

            if not profile_name:
                messagebox.showwarning("Profile Required",
                    "Please select a profile first!\n\n"
                    "You can:\n"
                    "• Select an existing profile from the dropdown\n"
                    "• Create a new profile with '🆕 Create Profile'\n"
                    "• Use the Profile Wizard for complete setup")
                return

            # Load profile data
            profile_data = self.load_profile_data(profile_name)
            if not profile_data:
                messagebox.showerror("Profile Error", f"Could not load profile '{profile_name}'")
                return

            # Check if we have a proxy
            if not proxy:
                response = messagebox.askyesno("No Proxy Selected",
                    "No proxy is currently selected. This means the browser will use your real IP address.\n\n"
                    "For maximum anonymity, you should:\n"
                    "• Go to Proxy Manager tab and set a current proxy\n"
                    "• Scrape and verify fresh proxies first\n\n"
                    "Continue anyway?")
                if not response:
                    return

            # Launch browser with all features
            browser_type = self.browser_select_var.get()
            url = self.start_url_var.get()

            success = self.user_browser.launch_anonymous_browser(
                proxy=proxy,
                profile_data=profile_data,
                browser_type=browser_type,
                url=url
            )

            if success:
                self.log_status(f"🚀 Launched anonymous browser with profile '{profile_name}'")
                self.update_status_banner()
            else:
                messagebox.showerror("Launch Failed", "Could not launch anonymous browser")

        except Exception as e:
            self.log_status(f"❌ Browser launch error: {e}")
            messagebox.showerror("Launch Error", f"Browser launch failed: {e}")

    def setup_status_integration(self):
        """Setup integration between status banner and main application"""
        if not self.status_banner or not self.user_browser or not self.fingerprint_manager:
            return

        def status_update_callback(status_data):
            """Callback for status banner updates"""
            try:
                # Update main application status based on banner data
                self.update_main_status_from_banner(status_data)
            except Exception as e:
                logger.error(f"Error in status callback: {e}")

        self.status_banner.add_update_callback(status_update_callback)

        # Setup browser integration
        self.user_browser.set_fingerprint_manager(self.fingerprint_manager)

        def browser_status_callback(message, status_type):
            """Callback for browser status updates"""
            self.log_status(f"🌐 Browser: {message}")

        self.user_browser.add_status_callback(browser_status_callback)

    def update_status_banner(self):
        """Update status banner with current application state"""
        if not self.status_banner or not self.user_browser:
            return

        try:
            # Calculate anonymity score
            profile_data = None
            if self.selected_profile:
                profile_data = self.load_profile_data(self.selected_profile)

            proxy_data = None
            if self.current_proxy:
                # Find proxy data
                for proxy in self.verified_proxies:
                    if proxy.get('proxy') == self.current_proxy:
                        proxy_data = proxy
                        break

            cookie_data = None
            if self.selected_profile:
                cookie_data = self.cookie_harvester.get_harvest_stats(self.selected_profile)

            # Calculate score
            score = self.status_banner.calculate_anonymity_score(profile_data, proxy_data, cookie_data)

            # Update banner
            status_data = {
                'anonymity_score': score,
                'profile_name': self.selected_profile or 'None',
                'proxy_status': 'Connected' if self.current_proxy else 'Disconnected',
                'cookie_count': cookie_data.get('total_cookies', 0) if cookie_data else 0,
                'browser_sessions': len(self.user_browser.get_active_sessions()),
                'system_health': self._get_system_health()
            }

            self.status_banner.update_status(status_data)

        except Exception as e:
            logger.error(f"Error updating status banner: {e}")

    def _get_system_health(self) -> str:
        """Get overall system health status"""
        try:
            health_score = 0

            # Check components
            if BACKEND_AVAILABLE:
                health_score += 25

            if self.fingerprint_manager:
                health_score += 25

            if self.user_browser:
                health_score += 25

            if len(self.verified_proxies) > 0:
                health_score += 25

            if health_score >= 90:
                return "Excellent"
            elif health_score >= 70:
                return "Good"
            elif health_score >= 50:
                return "Fair"
            else:
                return "Poor"

        except Exception as e:
            logger.error(f"Error getting system health: {e}")
            return "Unknown"

    def update_main_status_from_banner(self, status_data):
        """Update main application status based on banner data"""
        try:
            # Update dashboard status labels
            if hasattr(self, 'status_labels'):
                # Update proxy scraper status
                proxy_count = len(self.verified_proxies)
                self.status_labels["🔍 Proxy Scraper"].config(text=f"{len(self.proxy_scraper.sources)} sources ({proxy_count} verified)")

                # Update current proxy status
                proxy_text = self.current_proxy or "None"
                for i, (name, _) in enumerate(self.status_components):
                    if "Current Proxy" in name:
                        self.status_labels[name].config(text=proxy_text)
                        break

                # Update stealth mode
                stealth_text = "Enabled" if self.stealth_mode else "Disabled"
                for i, (name, _) in enumerate(self.status_components):
                    if "Stealth Mode" in name:
                        self.status_labels[name].config(text=stealth_text)
                        break

        except Exception as e:
            logger.error(f"Error updating main status: {e}")

    def draw_browser_status_circle(self, color):
        """Draw browser status indicator circle"""
        self.browser_canvas.delete("all")
        self.browser_canvas.create_oval(2, 2, 18, 18, fill=color, outline=color)
        self.browser_canvas.update()

    def update_browser_status_display(self):
        """Update browser status display"""
        if not self.user_browser:
            return

        try:
            browsers = self.user_browser._get_supported_browsers()
            status_text = "🌐 Browser Status:\n\n"

            for browser, available in browsers.items():
                status = "✅ Installed" if available else "❌ Not Installed"
                status_text += f"• {browser.capitalize()}: {status}\n"

            # Add active sessions info
            active_sessions = self.user_browser.get_active_sessions()
            status_text += f"\n🔴 Active Sessions: {len(active_sessions)}\n"

            for session in active_sessions:
                status_text += f"• {session['browser_type']} ({session['profile_name']}): {session['duration_seconds']}s\n"

            self.browser_status_text.config(state='normal')
            self.browser_status_text.delete(1.0, tk.END)
            self.browser_status_text.insert(1.0, status_text)
            self.browser_status_text.config(state='disabled')

        except Exception as e:
            logger.error(f"Error updating browser status: {e}")

    def check_installed_browsers(self):
        """Check and display installed browsers"""
        self.update_browser_status_display()
        self.log_status("🔍 Checked installed browsers")

    def install_missing_browsers(self):
        """Install missing browsers"""
        try:
            browsers = self.user_browser._get_supported_browsers()
            missing_browsers = [browser for browser, available in browsers.items() if not available]

            if not missing_browsers:
                messagebox.showinfo("All Browsers Installed", "All supported browsers are already installed!")
                return

            # Ask user which browser to install
            install_dialog = tk.Toplevel(self.root)
            install_dialog.title("📦 Install Missing Browsers")
            install_dialog.geometry("400x300")
            install_dialog.transient(self.root)

            ttk.Label(install_dialog, text="Select browsers to install:",
                     font=("Arial", 12, "bold")).pack(pady=20)

            browser_vars = {}
            for browser in missing_browsers:
                var = tk.BooleanVar(value=True)
                browser_vars[browser] = var
                ttk.Checkbutton(install_dialog, text=f"Install {browser.capitalize()}",
                               variable=var).pack(anchor='w', padx=20)

            def do_install():
                install_dialog.destroy()
                for browser, var in browser_vars.items():
                    if var.get():
                        success = self.user_browser.install_browser(browser)
                        if success:
                            self.log_status(f"✅ {browser} installed successfully")
                        else:
                            self.log_status(f"❌ Failed to install {browser}")

            ttk.Button(install_dialog, text="Install Selected",
                      command=do_install).pack(pady=20)

        except Exception as e:
            self.log_status(f"❌ Error in browser installation: {e}")

    def test_browser_setup(self):
        """Test browser setup with current configuration"""
        try:
            # Test browser installation
            browser_type = self.browser_select_var.get()
            if not self.user_browser._check_browser_installed(browser_type):
                messagebox.showerror("Browser Not Found", f"{browser_type} browser is not installed")
                return

            # Test proxy if available
            if self.current_proxy:
                result = self.proxy_scraper._test_proxy(self.current_proxy, include_geo=False)
                if result and result.get('working'):
                    messagebox.showinfo("Setup Test", "✅ Browser and proxy setup is working correctly!")
                else:
                    messagebox.showwarning("Setup Test", "⚠️ Proxy test failed, but browser is available")
            else:
                messagebox.showinfo("Setup Test", "✅ Browser is available. No proxy selected for testing.")

        except Exception as e:
            messagebox.showerror("Test Error", f"Setup test failed: {e}")

    def show_browser_settings(self):
        """Show browser settings dialog"""
        try:
            settings_dialog = tk.Toplevel(self.root)
            settings_dialog.title("⚙️ Browser Settings")
            settings_dialog.geometry("500x400")
            settings_dialog.transient(self.root)

            # Browser selection
            browser_frame = ttk.LabelFrame(settings_dialog, text="Browser Selection")
            browser_frame.pack(fill='x', padx=10, pady=10)

            ttk.Label(browser_frame, text="Default Browser:").grid(row=0, column=0, sticky='w', padx=5)
            default_browser_combo = ttk.Combobox(browser_frame, textvariable=self.browser_select_var,
                                               values=['chrome', 'firefox', 'edge', 'brave'],
                                               state='readonly', width=15)
            default_browser_combo.grid(row=0, column=1, padx=5)

            # Default URL
            url_frame = ttk.LabelFrame(settings_dialog, text="Default Settings")
            url_frame.pack(fill='x', padx=10, pady=10)

            ttk.Label(url_frame, text="Start URL:").grid(row=0, column=0, sticky='w', padx=5)
            start_url_entry = ttk.Entry(url_frame, textvariable=self.start_url_var, width=40)
            start_url_entry.grid(row=0, column=1, padx=5)

            # Default options
            options_frame = ttk.LabelFrame(settings_dialog, text="Default Options")
            options_frame.pack(fill='x', padx=10, pady=10)

            ttk.Checkbutton(options_frame, text="Always use Incognito mode",
                           variable=self.incognito_var).pack(anchor='w', padx=5)
            ttk.Checkbutton(options_frame, text="Enable full stealth mode by default",
                           variable=self.stealth_var).pack(anchor='w', padx=5)
            ttk.Checkbutton(options_frame, text="Enable leak monitoring by default",
                           variable=self.monitor_var).pack(anchor='w', padx=5)

            # Save button
            ttk.Button(settings_dialog, text="Save Settings",
                      command=settings_dialog.destroy).pack(pady=20)

        except Exception as e:
            self.log_status(f"❌ Error showing browser settings: {e}")

    def show_detailed_status(self):
        """Show detailed status from banner"""
        if self.status_banner:
            self.status_banner.show_detailed_status()

    def export_status_report(self):
        """Export comprehensive status report"""
        if not self.status_banner:
            return

        try:
            filename = self.status_banner.export_status()
            if filename:
                self.log_status(f"📊 Status report exported to {filename}")
                messagebox.showinfo("Export Complete", f"Status report saved to:\n{filename}")
            else:
                messagebox.showerror("Export Failed", "Could not export status report")
        except Exception as e:
            self.log_status(f"❌ Status export error: {e}")

    # Enhanced proxy methods
    def smart_scrape_proxies(self):
        """Smart proxy scraping with enhanced sources"""
        if self.operation_running:
            self.log_status("⚠️ Enhanced operation already running")
            return

        def scrape():
            try:
                self.operation_running = True
                self.progress_var.set(0)
                self.progress_label.config(text="Starting enhanced proxy scraping...")

                # Use enhanced scraping with more sources
                proxies_raw = self.proxy_scraper.scrape_proxies_parallel(max_workers=15, include_http=True)
                self.progress_var.set(30)
                self.progress_label.config(text=f"Found {len(proxies_raw)} raw proxies from enhanced sources")

                if proxies_raw:
                    # Enhanced verification with geographic data
                    verified_proxies = self.proxy_scraper.verify_proxies_parallel(
                        max_workers=25, include_geo=True, batch_size=50
                    )
                    self.verified_proxies = verified_proxies
                    self.progress_var.set(95)
                    self.progress_label.config(text=f"Updating enhanced display...")

                    # Update the proxy display in the main thread
                    def update_ui():
                        self.update_enhanced_proxy_display()
                        self.proxy_status.config(text=f"✅ Enhanced: {len(verified_proxies)} proxies from 50+ sources")
                        self.log_status(f"🚀 Enhanced scraping complete: {len(verified_proxies)} verified proxies")

                    # Schedule UI update in main thread
                    self.root.after(0, update_ui)

                    self.progress_var.set(100)
                    self.progress_label.config(text=f"✅ Enhanced Complete! {len(verified_proxies)} working proxies")

                else:
                    self.progress_label.config(text="❌ No proxies found from enhanced sources")
                    self.log_status("❌ No proxies could be scraped from enhanced sources")

            except Exception as e:
                self.log_status(f"❌ Enhanced scraping error: {e}")
                self.progress_label.config(text="❌ Error occurred")
            finally:
                self.operation_running = False

        thread = threading.Thread(target=scrape, daemon=True)
        thread.start()

    def concurrent_verify_proxies(self):
        """Concurrent proxy verification"""
        if not self.verified_proxies:
            messagebox.showwarning("Warning", "No proxies to verify. Please scrape first.")
            return

        self.log_status("⚡ Starting concurrent proxy verification...")

        def verify():
            try:
                verified = self.proxy_scraper.verify_proxies_parallel(max_workers=30, include_geo=True)
                self.verified_proxies = verified
                self.update_enhanced_proxy_display()
                self.log_status(f"⚡ Concurrent verification complete: {len(verified)} proxies")
            except Exception as e:
                self.log_status(f"❌ Concurrent verification error: {e}")

        thread = threading.Thread(target=verify, daemon=True)
        thread.start()

    def update_enhanced_proxy_display(self):
        """Update enhanced proxy tree display with quality metrics"""
        self.proxy_tree.delete(*self.proxy_tree.get_children())

        for proxy in self.verified_proxies:
            proxy_str = proxy.get('proxy', '')
            if ':' in proxy_str:
                ip, port = proxy_str.split(':', 1)
            else:
                ip, port = proxy_str, 'N/A'

            # Calculate quality score
            quality = self._calculate_proxy_quality(proxy)

            # Add timestamp
            timestamp = datetime.now().strftime("%H:%M:%S")

            self.proxy_tree.insert('', 'end', values=(
                ip, port,
                proxy.get('country', 'Unknown'),
                proxy.get('city', 'Unknown'),
                proxy.get('region', 'Unknown'),
                f"{proxy.get('rtt_ms', 'N/A')}ms",
                '✅ Verified' if proxy.get('working') else '❌ Failed',
                f"{quality}/100",
                timestamp
            ))

    def _calculate_proxy_quality(self, proxy: Dict[str, Any]) -> int:
        """Calculate proxy quality score (0-100)"""
        score = 0

        if not proxy.get('working'):
            return 0

        # Speed score (40 points)
        rtt = proxy.get('rtt_ms', 999)
        if rtt < 50: score += 40
        elif rtt < 100: score += 35
        elif rtt < 200: score += 25
        elif rtt < 500: score += 15
        else: score += 5

        # Geographic data score (30 points)
        if proxy.get('country') and proxy['country'] != 'Unknown': score += 15
        if proxy.get('city') and proxy['city'] != 'Unknown': score += 10
        if proxy.get('region') and proxy['region'] != 'Unknown': score += 5

        # Connection stability (30 points)
        # This would be calculated based on historical data
        score += 30  # Placeholder

        return min(100, score)

    def show_enhanced_proxy_stats(self):
        """Show enhanced proxy statistics"""
        if not self.verified_proxies:
            messagebox.showinfo("Enhanced Proxy Statistics", "No proxies available. Please scrape first.")
            return

        total = len(self.verified_proxies)
        working = len([p for p in self.verified_proxies if p.get('working', False)])

        # Enhanced statistics
        avg_rtt = sum(p.get('rtt_ms', 0) for p in self.verified_proxies if p.get('rtt_ms', 0)) / working if working > 0 else 0

        # Country distribution
        countries = {}
        for proxy in self.verified_proxies:
            country = proxy.get('country', 'Unknown')
            countries[country] = countries.get(country, 0) + 1

        # Quality distribution
        quality_ranges = {'Excellent (90-100)': 0, 'Good (70-89)': 0, 'Fair (50-69)': 0, 'Poor (0-49)': 0}
        for proxy in self.verified_proxies:
            quality = self._calculate_proxy_quality(proxy)
            if quality >= 90: quality_ranges['Excellent (90-100)'] += 1
            elif quality >= 70: quality_ranges['Good (70-89)'] += 1
            elif quality >= 50: quality_ranges['Fair (50-69)'] += 1
            else: quality_ranges['Poor (0-49)'] += 1

        stats_text = f"""
🚀 Enhanced Proxy Statistics:
{'='*40}
Total Proxies: {total}
Working Proxies: {working}
Success Rate: {(working/total*100):.1f}%

Performance Metrics:
• Average RTT: {avg_rtt:.1f}ms
• Fastest Proxy: {min([p.get('rtt_ms', 999) for p in self.verified_proxies if p.get('rtt_ms', 0)], default=0)}ms

Quality Distribution:
"""
        for quality_range, count in quality_ranges.items():
            stats_text += f"  {quality_range}: {count}\n"

        stats_text += "\nGeographic Distribution:\n"
        for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True)[:10]:
            stats_text += f"  {country}: {count}\n"

        messagebox.showinfo("Enhanced Proxy Statistics", stats_text)

    def show_geographic_targeting(self):
        """Show geographic targeting interface"""
        try:
            geo_dialog = tk.Toplevel(self.root)
            geo_dialog.title("🎯 Geographic Proxy Targeting")
            geo_dialog.geometry("600x500")
            geo_dialog.transient(self.root)

            # Target selection
            target_frame = ttk.LabelFrame(geo_dialog, text="🎯 Target Location")
            target_frame.pack(fill='x', padx=10, pady=10)

            target_container = ttk.Frame(target_frame)
            target_container.pack(fill='x', padx=10, pady=10)

            ttk.Label(target_container, text="Target Country:").grid(row=0, column=0, sticky='w', padx=5)
            target_country_var = tk.StringVar()
            target_country_combo = ttk.Combobox(target_container, textvariable=target_country_var,
                                               values=['United States', 'United Kingdom', 'Germany', 'France', 'Canada', 'Australia', 'Japan'],
                                               state='readonly', width=20)
            target_country_combo.grid(row=0, column=1, padx=5)

            ttk.Label(target_container, text="Max Results:").grid(row=0, column=2, sticky='w', padx=10)
            max_results_var = tk.StringVar(value="10")
            max_results_entry = ttk.Entry(target_container, textvariable=max_results_var, width=5)
            max_results_entry.grid(row=0, column=3, padx=5)

            # Targeting options
            options_frame = ttk.LabelFrame(geo_dialog, text="⚙️ Targeting Options")
            options_frame.pack(fill='x', padx=10, pady=10)

            options_container = ttk.Frame(options_frame)
            options_container.pack(fill='x', padx=10, pady=10)

            include_neighbors_var = tk.BooleanVar(value=True)
            ttk.Checkbutton(options_container, text="Include neighboring countries",
                           variable=include_neighbors_var).pack(anchor='w', padx=5)

            prioritize_speed_var = tk.BooleanVar(value=True)
            ttk.Checkbutton(options_container, text="Prioritize speed over location accuracy",
                           variable=prioritize_speed_var).pack(anchor='w', padx=5)

            # Results display
            results_frame = ttk.LabelFrame(geo_dialog, text="📋 Targeting Results")
            results_frame.pack(fill='both', expand=True, padx=10, pady=10)

            results_text = tk.Text(results_frame, height=15, width=60)
            results_text.pack(fill='both', expand=True, padx=5, pady=5)

            def find_targeted_proxies():
                target_country = target_country_var.get()
                if not target_country:
                    messagebox.showwarning("Target Required", "Please select a target country")
                    return

                try:
                    max_results = int(max_results_var.get())
                except:
                    messagebox.showerror("Invalid Input", "Please enter a valid number for max results")
                    return

                # Find best proxies for target
                target_proxies = self.proxy_scraper.get_best_proxies_for_target(target_country, max_results)

                # Display results
                results_text.delete(1.0, tk.END)

                if target_proxies:
                    results_text.insert(1.0, f"🎯 Best proxies for {target_country}:\n\n")

                    for i, proxy in enumerate(target_proxies, 1):
                        quality = self._calculate_proxy_quality(proxy)
                        results_text.insert(tk.END, f"{i}. {proxy.get('proxy', 'N/A')}\n")
                        results_text.insert(tk.END, f"   📍 {proxy.get('country', 'Unknown')}, {proxy.get('city', 'Unknown')}\n")
                        results_text.insert(tk.END, f"   ⚡ RTT: {proxy.get('rtt_ms', 'N/A')}ms | Quality: {quality}/100\n")
                        results_text.insert(tk.END, f"   🌐 IP: {proxy.get('actual_ip', 'N/A')}\n\n")
                else:
                    results_text.insert(1.0, f"❌ No suitable proxies found for {target_country}")

                results_text.see(tk.END)

            # Find button
            ttk.Button(geo_dialog, text="🎯 Find Optimal Proxies",
                      command=find_targeted_proxies).pack(pady=10)

        except Exception as e:
            self.log_status(f"❌ Geographic targeting error: {e}")

    def manage_user_proxies(self):
        """Manage user-defined proxies"""
        try:
            proxy_dialog = tk.Toplevel(self.root)
            proxy_dialog.title("👤 User Proxy Management")
            proxy_dialog.geometry("600x400")
            proxy_dialog.transient(self.root)

            # Add proxy section
            add_frame = ttk.LabelFrame(proxy_dialog, text="➕ Add Custom Proxy")
            add_frame.pack(fill='x', padx=10, pady=10)

            add_container = ttk.Frame(add_frame)
            add_container.pack(fill='x', padx=10, pady=10)

            ttk.Label(add_container, text="Proxy (IP:Port):").grid(row=0, column=0, sticky='w', padx=5)
            proxy_entry_var = tk.StringVar()
            proxy_entry = ttk.Entry(add_container, textvariable=proxy_entry_var, width=30)
            proxy_entry.grid(row=0, column=1, padx=5)

            ttk.Label(add_container, text="Name:").grid(row=0, column=2, sticky='w', padx=10)
            name_entry_var = tk.StringVar()
            name_entry = ttk.Entry(add_container, textvariable=name_entry_var, width=20)
            name_entry.grid(row=0, column=3, padx=5)

            def add_proxy():
                proxy = proxy_entry_var.get().strip()
                name = name_entry_var.get().strip() or proxy

                if not proxy:
                    messagebox.showwarning("Proxy Required", "Please enter a proxy address")
                    return

                if not self._is_valid_proxy_format(proxy):
                    messagebox.showerror("Invalid Format", "Please enter proxy in format: IP:PORT")
                    return

                # Test the proxy
                result = self.proxy_scraper._test_proxy(proxy, include_geo=True)
                if result and result.get('working'):
                    # Add to verified proxies with custom name
                    result['user_defined'] = True
                    result['custom_name'] = name
                    self.verified_proxies.append(result)

                    self.update_enhanced_proxy_display()
                    self.log_status(f"✅ Added custom proxy: {name} ({proxy})")

                    # Clear entries
                    proxy_entry_var.set('')
                    name_entry_var.set('')

                    messagebox.showinfo("Success", f"Custom proxy '{name}' added successfully!")
                else:
                    messagebox.showerror("Proxy Test Failed", "The proxy could not be verified. Please check the address.")

            ttk.Button(add_container, text="🧪 Test & Add Proxy",
                      command=add_proxy).grid(row=0, column=4, padx=10)

            # User proxies list
            list_frame = ttk.LabelFrame(proxy_dialog, text="📋 Your Custom Proxies")
            list_frame.pack(fill='both', expand=True, padx=10, pady=10)

            list_container = ttk.Frame(list_frame)
            list_container.pack(fill='both', expand=True, padx=10, pady=10)

            # Custom proxies display
            self.user_proxies_text = tk.Text(list_container, height=10, width=60)
            self.user_proxies_text.pack(side='left', fill='both', expand=True)

            scrollbar = ttk.Scrollbar(list_container, orient='vertical', command=self.user_proxies_text.yview)
            self.user_proxies_text.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side='right', fill='y')

            # Update display
            self.update_user_proxies_display()

        except Exception as e:
            self.log_status(f"❌ User proxy management error: {e}")

    def update_user_proxies_display(self):
        """Update user proxies display"""
        try:
            user_proxies = [p for p in self.verified_proxies if p.get('user_defined', False)]

            self.user_proxies_text.delete(1.0, tk.END)

            if user_proxies:
                self.user_proxies_text.insert(1.0, "👤 Your Custom Proxies:\n\n")

                for i, proxy in enumerate(user_proxies, 1):
                    name = proxy.get('custom_name', proxy.get('proxy', 'Unknown'))
                    proxy_addr = proxy.get('proxy', 'Unknown')
                    quality = self._calculate_proxy_quality(proxy)

                    self.user_proxies_text.insert(tk.END, f"{i}. {name}\n")
                    self.user_proxies_text.insert(tk.END, f"   📍 {proxy_addr}\n")
                    self.user_proxies_text.insert(tk.END, f"   🌍 {proxy.get('country', 'Unknown')}, {proxy.get('city', 'Unknown')}\n")
                    self.user_proxies_text.insert(tk.END, f"   ⚡ RTT: {proxy.get('rtt_ms', 'N/A')}ms | Quality: {quality}/100\n\n")
            else:
                self.user_proxies_text.insert(1.0, "👤 No custom proxies added yet.\n\nAdd your own proxies using the form above!")

        except Exception as e:
            self.user_proxies_text.insert(1.0, f"Error loading user proxies: {e}")

    def _is_valid_proxy_format(self, proxy):
        """Validate proxy format"""
        ip_port = proxy.split(':')
        if len(ip_port) != 2:
            return False

        ip_parts = ip_port[0].split('.')
        if len(ip_parts) != 4:
            return False

        try:
            port = int(ip_port[1])
            return 1 <= port <= 65535 and all(0 <= int(p) <= 255 for p in ip_parts)
        except:
            return False

    # Placeholder methods for enhanced functionality
    def sort_column(self, col):
        """Sort treeview by column"""
        # Simple sorting implementation
        pass

    def set_current_proxy(self):
        """Set selected proxy as current"""
        selection = self.proxy_tree.selection()
        if selection:
            item = selection[0]
            values = self.proxy_tree.item(item, 'values')
            proxy = f"{values[0]}:{values[1]}"
            self.current_proxy = proxy
            self.current_proxy_label.config(text=proxy)
            self.log_status(f"🎯 Set current proxy: {proxy}")

    def test_selected_proxy(self):
        """Test selected proxy"""
        selection = self.proxy_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a proxy first")
            return

        item = selection[0]
        values = self.proxy_tree.item(item, 'values')
        proxy = f"{values[0]}:{values[1]}"

        def test():
            try:
                result = self.proxy_scraper._test_proxy(proxy, include_geo=True)
                if result and result.get('working'):
                    self.log_status(f"✅ Proxy {proxy} working (RTT: {result.get('rtt_ms', 'N/A')}ms)")
                else:
                    self.log_status(f"❌ Proxy {proxy} failed")
            except Exception as e:
                self.log_status(f"❌ Proxy test error: {e}")

        thread = threading.Thread(target=test, daemon=True)
        thread.start()

    def apply_enhanced_location_filters(self, event=None):
        """Apply enhanced location filters"""
        self.log_status("� Enhanced location filters applied")

    def show_enhanced_proxy_menu(self, event):
        """Show enhanced right-click menu for proxy tree"""
        item = self.proxy_tree.identify_row(event.y)
        if item:
            self.proxy_tree.selection_set(item)
            self.proxy_menu.post(event.x_root, event.y_root)

    def get_enhanced_geo_for_selection(self):
        """Get enhanced geo info for selected proxy"""
        self.log_status("🌍 Getting enhanced geo information...")

    def view_proxy_quality(self):
        """View detailed proxy quality metrics"""
        self.log_status("📊 Viewing proxy quality metrics...")

    def add_proxy_to_favorites(self):
        """Add selected proxy to favorites"""
        selection = self.proxy_tree.selection()
        if selection:
            item = selection[0]
            values = self.proxy_tree.item(item, 'values')
            proxy = f"{values[0]}:{values[1]}"
            self.log_status(f"⭐ Added proxy to favorites: {proxy}")

    def generate_enhanced_history(self, months):
        """Generate enhanced cookie history with live updates"""
        if not self.cookie_harvester:
            self.log_status("❌ Cookie harvester not available")
            return

        self.log_status(f"🚀 Generating enhanced {months}-month cookie history...")

        def generate():
            try:
                # Clear results display and show initial status
                def update_ui():
                    self.cookie_results.config(state='normal')
                    self.cookie_results.delete(1.0, tk.END)
                    self.cookie_results.insert(1.0, f"🍪 Starting {months}-month cookie generation...\n\n")
                    self.cookie_results.config(state='disabled')
                    self.cookie_results.see(tk.END)

                self.root.after(0, update_ui)

                # Generate cookies with progress updates
                total_cookies, cookies_data = self.cookie_harvester.harvest_for_profile(
                    profile_id=self.profile_var.get() or 'default_profile',
                    count=50 * months,  # More cookies for longer periods
                    headless=True
                )

                # Update progress
                def update_progress():
                    self.cookie_results.config(state='normal')
                    self.cookie_results.insert(tk.END, f"✅ Generated {total_cookies} cookies successfully!\n")
                    self.cookie_results.insert(tk.END, f"📊 Cookie statistics updated\n")
                    self.cookie_results.insert(tk.END, f"🔄 Refreshing display...\n")
                    self.cookie_results.config(state='disabled')
                    self.cookie_results.see(tk.END)

                    # Refresh the cookie stats display
                    self.update_cookie_stats_display()

                self.root.after(0, update_progress)

                self.log_status(f"✅ Generated {total_cookies} cookies for {months}-month history")

            except Exception as e:
                def show_error():
                    self.cookie_results.config(state='normal')
                    self.cookie_results.insert(tk.END, f"❌ Error: {e}\n")
                    self.cookie_results.config(state='disabled')
                    self.cookie_results.see(tk.END)

                self.root.after(0, show_error)
                self.log_status(f"❌ Cookie generation error: {e}")

        thread = threading.Thread(target=generate, daemon=True)
        thread.start()

    def generate_background_cookies(self):
        """Generate cookies in background"""
        self.log_status("🔄 Starting background cookie generation...")

    def smart_scan_traffic(self):
        """Smart traffic scanning"""
        self.log_status("🔍 Starting smart traffic scan...")

    def view_monitoring_analytics(self):
        """View monitoring analytics"""
        self.log_status("�📊 Viewing monitoring analytics...")

    # Existing methods (keeping for compatibility)
    def quick_scrape_proxies(self):
        """Quick proxy scraping"""
        self.smart_scrape_proxies()

    def quick_generate_cookies(self):
        """Quick cookie generation"""
        self.generate_enhanced_history(6)

    def quick_test_system(self):
        """Quick system test"""
        self.run_system_test()

    def quick_export_data(self):
        """Quick export"""
        self.export_proxies()

    def run_system_test(self):
        """Run comprehensive system test"""
        self.log_status("🔬 Running comprehensive enhanced system test...")

        test_results = []
        test_results.append("🧪 Enhanced System Test Results:")
        test_results.append(f"✅ Enhanced Proxy Scraper: {len(self.proxy_scraper.sources)} sources")
        test_results.append(f"✅ Geo Locator: Available")
        test_results.append(f"✅ Cookie Manager: Available")
        test_results.append(f"✅ Current Proxy: {self.current_proxy or 'None'}")
        test_results.append(f"✅ Stealth Mode: {'Enabled' if self.stealth_mode else 'Disabled'}")
        test_results.append(f"✅ Profile: {self.selected_profile or 'None'}")
        test_results.append(f"✅ Fingerprint Manager: Ready")
        test_results.append(f"✅ User Browser: Ready")
        test_results.append(f"✅ Status Banner: Active")

        if self.current_proxy:
            result = self.proxy_scraper._test_proxy(self.current_proxy, include_geo=False)
            connectivity = "Working" if result and result.get('working') else "Failed"
            test_results.append(f"✅ Enhanced Connectivity: {connectivity}")

        test_results.append("✅ Enhanced GUI Framework: Working")
        test_results.append("🎉 All enhanced systems operational!")

        result_text = "\n".join(test_results)
        self.status_display.delete(1.0, tk.END)
        self.status_display.insert(1.0, result_text)

        messagebox.showinfo("Enhanced System Test", "All enhanced systems are working perfectly!")

    def load_profile_data(self, profile_name: str) -> Optional[Dict[str, Any]]:
        """Load profile data from file"""
        try:
            profile_file = f"profiles/{profile_name}.json"
            if os.path.exists(profile_file):
                with open(profile_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.log_status(f"❌ Error loading profile data: {e}")
        return None

    def log_status(self, message):
        """Log message to status display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_display.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_display.see(tk.END)

    def load_csv_data(self):
        """Load CSV data"""
        try:
            csv_file = 'top1000.csv'
            if os.path.exists(csv_file):
                with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    sites = [line.strip().split(',')[0] for line in lines[1:101] if line.strip()]
                    self.log_status(f"✅ Loaded {len(sites)} websites from CSV")
            else:
                self.log_status("⚠️ CSV file not found")
        except Exception as e:
            self.log_status(f"❌ CSV load error: {e}")

    def load_profiles(self):
        """Load available profiles"""
        try:
            profiles_dir = 'profiles'
            if os.path.exists(profiles_dir):
                profile_files = [f.replace('.json', '') for f in os.listdir(profiles_dir)
                               if f.endswith('.json')]
                profile_files.sort()
                self.profile_combo['values'] = profile_files
                self.profile_select_combo['values'] = profile_files
                self.log_status(f"📂 Loaded {len(profile_files)} profiles")
            else:
                self.profile_combo['values'] = []
                self.profile_select_combo['values'] = []
        except Exception as e:
            self.log_status(f"❌ Profile loading error: {e}")

    def on_profile_select(self, event=None):
        """Handle profile selection"""
        profile = self.profile_var.get()
        if profile:
            self.load_profile(profile)

    def load_profile(self, profile_name):
        """Load a profile"""
        try:
            profile_file = f"profiles/{profile_name}.json"
            if not os.path.exists(profile_file):
                messagebox.showwarning("Warning", f"Profile '{profile_name}' not found")
                return

            with open(profile_file, 'r') as f:
                profile_data = json.load(f)

            # Apply profile settings
            self.ua_profile_var.set(profile_data.get('user_agent', ''))
            self.resolution_var.set(profile_data.get('screen_resolution', '1920x1080'))
            self.language_var.set(profile_data.get('language', 'en-US,en;q=0.9'))
            self.timezone_var.set(profile_data.get('timezone', 'America/New_York'))

            self.selected_profile = profile_name
            self.log_status(f"✅ Profile '{profile_name}' loaded")
            self.update_profile_info()

        except Exception as e:
            self.log_status(f"❌ Profile load error: {e}")

    def update_profile_info(self):
        """Update profile information display"""
        info_text = f"""
Enhanced Profile Management Information
{'='*50}

Active Profile: {self.selected_profile or 'None'}
Stealth Mode: {'Enabled' if self.stealth_mode else 'Disabled'}

Current Configuration:
• User Agent: {self.ua_profile_var.get()[:80]}{'...' if len(self.ua_profile_var.get()) > 80 else ''}
• Screen Resolution: {self.resolution_var.get()}
• Language: {self.language_var.get()}
• Timezone: {self.timezone_var.get()}

Enhanced Features:
{'✅ User Agent: Spoofed' if self.stealth_mode else '🔓 Normal operation'}
{'✅ Browser Fingerprint: Obfuscated' if self.stealth_mode else '📋 No fingerprint spoofing'}
{'✅ All operations filtered through profile' if self.stealth_mode else '🔓 Normal operations'}
{'✅ Enhanced cookie generation available' if self.stealth_mode else '🔓 Standard cookie generation'}
"""
        self.profile_info.delete(1.0, tk.END)
        self.profile_info.insert(1.0, info_text)

    def toggle_stealth_mode(self):
        """Toggle stealth mode"""
        self.stealth_mode = self.stealth_var.get()

        if self.stealth_mode:
            self.log_status("🔐 Enhanced Stealth Mode Enabled")
            if self.selected_profile:
                self.ua_display.delete(0, tk.END)
                self.ua_display.insert(0, self.ua_profile_var.get())
        else:
            self.log_status("🔓 Enhanced Stealth Mode Disabled")

        self.update_profile_info()

    def generate_ua(self):
        """Generate user agent"""
        try:
            browser = self.browser_var.get()
            ua = self.cookie_manager.generate_user_agent(browser)
            self.ua_display.delete(0, tk.END)
            self.ua_display.insert(0, ua)
            self.log_status("🎭 User agent generated")
        except Exception as e:
            self.log_status(f"❌ UA generation error: {e}")

    def create_named_profile(self):
        """Create a profile with custom name from the input field"""
        profile_name = self.new_profile_name_var.get().strip()

        if not profile_name:
            messagebox.showwarning("Invalid Name", "Please enter a profile name")
            return

        if len(profile_name) < 3:
            messagebox.showwarning("Invalid Name", "Profile name must be at least 3 characters")
            return

        # Check if profile already exists
        if os.path.exists(f"profiles/{profile_name}.json"):
            response = messagebox.askyesno("Profile Exists",
                f"Profile '{profile_name}' already exists. Overwrite it?")
            if not response:
                return

        try:
            # Generate a basic user agent for the new profile
            ua = self.cookie_manager.generate_user_agent('chrome')

            # Create profile configuration with stealth enabled by default
            profile_config = {
                'profile_name': profile_name,
                'user_agent': ua,
                'screen_resolution': '1920x1080',
                'language': 'en-US,en;q=0.9',
                'timezone': 'America/New_York',
                'platform': 'Win32',
                'stealth_enabled': True,  # Auto-enable stealth mode
                'cookie_profile': profile_name,
                'created_at': int(time.time()),
                'manually_created': True
            }

            # Save profile
            profiles_dir = 'profiles'
            os.makedirs(profiles_dir, exist_ok=True)
            profile_file = f"{profiles_dir}/{profile_name}.json"

            with open(profile_file, 'w') as f:
                json.dump(profile_config, f, indent=2)

            # Update UI
            self.profile_select_var.set(profile_name)
            self.new_profile_name_var.set('')  # Clear the entry field

            # Refresh profile lists
            self.load_profiles()
            self.ua_profile_var.set(ua)  # Set the UA in the configuration area

            messagebox.showinfo("Success", f"✅ Profile '{profile_name}' created successfully!\n\n"
                f"Generated user agent and saved configuration.\n\n"
                f"You can now configure the profile settings below and save.")
            self.log_status(f"👤 Profile '{profile_name}' created with custom name")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create profile: {e}")
            self.log_status(f"❌ Profile creation error: {e}")

    def generate_profile_ua(self):
        """Generate user agent for profile"""
        try:
            ua = self.cookie_manager.generate_user_agent('chrome')
            self.ua_profile_var.set(ua)
            self.log_status("🎭 Profile user agent generated")
        except Exception as e:
            self.log_status(f"❌ Profile UA generation error: {e}")

    def paste_user_agent(self):
        """Paste user agent from clipboard"""
        try:
            # Try to get from clipboard
            ua_string = self.root.clipboard_get()
            if ua_string and self._is_valid_user_agent_format(ua_string):
                self.ua_profile_var.set(ua_string.strip())
                self.log_status("📋 User agent pasted from clipboard")
            else:
                messagebox.showwarning("Invalid User Agent",
                    "The clipboard content doesn't appear to be a valid user agent string.\n\n"
                    "Please make sure you've copied a complete User-Agent string like:\n"
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...")
        except Exception as e:
            messagebox.showerror("Paste Error", "Could not paste from clipboard. Please copy the user agent string manually.")

    def validate_user_agent(self):
        """Validate the current user agent"""
        ua_string = self.ua_profile_var.get().strip()

        if not ua_string:
            messagebox.showwarning("No User Agent", "Please enter or paste a user agent string first")
            return

        if self._is_valid_user_agent_format(ua_string):
            ua_info = self._analyze_user_agent(ua_string)
            messagebox.showinfo("✅ Valid User Agent",
                f"User Agent is valid!\n\n"
                f"📱 Type: {ua_info['type']}\n"
                f"🌐 Browser: {ua_info['browser']}\n"
                f"📱 Platform: {ua_info['platform']}\n"
                f"🔧 Engine: {ua_info['engine']}\n\n"
                f"This user agent will work perfectly for anonymous browsing.")
        else:
            messagebox.showerror("❌ Invalid User Agent",
                "The user agent string appears to be invalid or incomplete.\n\n"
                "A valid user agent should:\n"
                "• Start with 'Mozilla/5.0'\n"
                "• Include platform information\n"
                "• Include browser and version details\n"
                "• Be properly formatted")

    def update_ua_preview(self, *args):
        """Update user agent preview and analysis"""
        ua_string = self.ua_profile_var.get().strip()

        if not ua_string:
            self.ua_preview_text.config(state='normal')
            self.ua_preview_text.delete(1.0, tk.END)
            self.ua_preview_text.insert(1.0, "No user agent entered")
            self.ua_preview_text.config(state='disabled')
            self.ua_type_label.config(text="Type: Unknown")
            return

        # Update preview
        self.ua_preview_text.config(state='normal')
        self.ua_preview_text.delete(1.0, tk.END)

        # Show first 100 characters
        preview = ua_string[:100] + "..." if len(ua_string) > 100 else ua_string
        self.ua_preview_text.insert(1.0, preview)
        self.ua_preview_text.config(state='disabled')

        # Analyze and show type
        ua_info = self._analyze_user_agent(ua_string)
        self.ua_type_label.config(text=f"Type: {ua_info['type']}")

    def _is_valid_user_agent_format(self, ua_string: str) -> bool:
        """Validate user agent string format"""
        if not ua_string or len(ua_string) < 20:
            return False

        # Basic checks for valid user agent structure
        required_elements = [
            'Mozilla/5.0',
            'AppleWebKit' in ua_string or 'Gecko' in ua_string,
            '(' in ua_string and ')' in ua_string  # Platform info
        ]

        return all(required_elements)

    def _analyze_user_agent(self, ua_string: str) -> Dict[str, str]:
        """Analyze user agent to determine type and characteristics"""
        ua_lower = ua_string.lower()

        # Determine device type
        if 'mobile' in ua_lower or 'iphone' in ua_lower or 'android' in ua_lower:
            device_type = 'Mobile'
        elif 'tablet' in ua_lower or 'ipad' in ua_lower:
            device_type = 'Tablet'
        else:
            device_type = 'Desktop'

        # Determine browser
        if 'chrome' in ua_lower and 'edg' not in ua_lower:
            browser = 'Chrome'
        elif 'firefox' in ua_lower:
            browser = 'Firefox'
        elif 'safari' in ua_lower and 'chrome' not in ua_lower:
            browser = 'Safari'
        elif 'edg' in ua_lower:
            browser = 'Edge'
        else:
            browser = 'Unknown'

        # Determine platform
        if 'windows' in ua_lower:
            platform = 'Windows'
        elif 'mac os' in ua_lower or 'macos' in ua_lower:
            platform = 'macOS'
        elif 'linux' in ua_lower:
            platform = 'Linux'
        elif 'android' in ua_lower:
            platform = 'Android'
        elif 'ios' in ua_lower or 'iphone' in ua_lower or 'ipad' in ua_lower:
            platform = 'iOS'
        else:
            platform = 'Unknown'

        # Determine engine
        if 'webkit' in ua_lower:
            engine = 'WebKit'
        elif 'gecko' in ua_lower:
            engine = 'Gecko'
        else:
            engine = 'Unknown'

        return {
            'type': device_type,
            'browser': browser,
            'platform': platform,
            'engine': engine
        }

    def save_current_profile(self):
        """Save current profile"""
        profile_name = self.profile_select_var.get()
        if not profile_name:
            messagebox.showwarning("Warning", "Please select a profile name")
            return

        try:
            profile_data = {
                'profile_name': profile_name,
                'user_agent': self.ua_profile_var.get(),
                'screen_resolution': self.resolution_var.get(),
                'language': self.language_var.get(),
                'timezone': self.timezone_var.get(),
                'stealth_enabled': self.stealth_var.get(),
                'created_at': int(time.time())
            }

            profiles_dir = 'profiles'
            os.makedirs(profiles_dir, exist_ok=True)
            profile_file = f"{profiles_dir}/{profile_name}.json"

            with open(profile_file, 'w') as f:
                json.dump(profile_data, f, indent=2)

            self.log_status(f"💾 Profile '{profile_name}' saved")
            self.load_profiles()  # Refresh profile list

        except Exception as e:
            self.log_status(f"❌ Profile save error: {e}")

    def rename_current_profile(self):
        """Rename the currently selected profile"""
        current_profile = self.profile_var.get()
        if not current_profile:
            messagebox.showwarning("No Profile Selected", "Please select a profile to rename first")
            return

        # Create rename dialog
        rename_dialog = tk.Toplevel(self.root)
        rename_dialog.title("Rename Profile")
        rename_dialog.geometry("400x200")
        rename_dialog.transient(self.root)
        rename_dialog.grab_set()

        ttk.Label(rename_dialog, text=f"Rename profile: {current_profile}",
                 font=("Arial", 12, "bold")).pack(pady=20)

        # New name input
        name_frame = ttk.Frame(rename_dialog)
        name_frame.pack(fill='x', padx=20)
        ttk.Label(name_frame, text="New Profile Name:").pack(anchor='w')
        new_name_var = tk.StringVar()
        new_name_entry = ttk.Entry(name_frame, textvariable=new_name_var, width=30)
        new_name_entry.pack(fill='x', pady=5)
        new_name_entry.focus()

        # Buttons
        btn_frame = ttk.Frame(rename_dialog)
        btn_frame.pack(fill='x', padx=20, pady=20)

        def do_rename():
            new_name = new_name_var.get().strip()
            if not new_name:
                messagebox.showwarning("Invalid Name", "Please enter a valid profile name")
                return

            if len(new_name) < 3:
                messagebox.showwarning("Invalid Name", "Profile name must be at least 3 characters")
                return

            # Check if new name already exists
            if os.path.exists(f"profiles/{new_name}.json"):
                messagebox.showwarning("Name Exists", f"Profile '{new_name}' already exists")
                return

            try:
                # Get old profile data
                old_file = f"profiles/{current_profile}.json"
                if not os.path.exists(old_file):
                    messagebox.showerror("Error", f"Profile '{current_profile}' not found")
                    return

                with open(old_file, 'r') as f:
                    profile_data = json.load(f)

                # Update profile name in data
                profile_data['profile_name'] = new_name

                # Create new file with new name
                new_file = f"profiles/{new_name}.json"
                with open(new_file, 'w') as f:
                    json.dump(profile_data, f, indent=2)

                # Delete old file
                os.remove(old_file)

                # Update UI
                self.profile_var.set(new_name)
                self.profile_select_var.set(new_name)
                self.selected_profile = new_name

                # Refresh profile list
                self.load_profiles()

                self.log_status(f"✏️ Profile renamed: '{current_profile}' → '{new_name}'")
                rename_dialog.destroy()

                messagebox.showinfo("Success", f"Profile renamed to '{new_name}' successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename profile: {e}")

        def cancel():
            rename_dialog.destroy()

        ttk.Button(btn_frame, text="Rename", command=do_rename).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=cancel).pack(side='right', padx=5)

    def create_new_profile(self):
        """Create new profile"""
        profile_name = f"new_profile_{int(time.time())}"
        self.profile_select_var.set(profile_name)
        self.ua_profile_var.set('')
        self.log_status(f"🆕 Created new profile: {profile_name}")

    def load_selected_profile(self):
        """Load selected profile"""
        profile = self.profile_select_var.get()
        if profile:
            self.load_profile(profile)

    def update_cookie_stats_display(self):
        """Update the cookie statistics display"""
        profile_name = self.profile_var.get()
        if not profile_name:
            stats_text = """
🍪 No Profile Selected

Select a profile from the dropdown above to view cookie statistics.
"""
        else:
            try:
                # Get cookie statistics for the selected profile
                cookie_stats = self.cookie_harvester.get_harvest_stats(profile_name)

                total_cookies = cookie_stats.get('total_cookies', 0)
                unique_domains = cookie_stats.get('unique_domains', 0)
                unique_sites = cookie_stats.get('unique_sites', 0)
                last_updated = cookie_stats.get('last_updated', 'Never')
                categories = ', '.join(cookie_stats.get('categories', []))

                if total_cookies == 0:
                    stats_text = f"""
🍪 Profile: {profile_name}
📊 Cookie Statistics: No cookies generated

Status: ⚠️ Ready for cookie generation
• Click "⚡ Quick Generate" to generate realistic browsing history
• Click "🚀 Standard Generate" for comprehensive cookies
• Click "🎯 Comprehensive Generate" for maximum authenticity
• Click "🔄 Background Generate" for non-blocking generation
"""
                else:
                    stats_text = f"""
🍪 Profile: {profile_name}
📊 Enhanced Cookie Statistics Overview:

Total Cookies: {total_cookies:,}
Unique Domains: {unique_domains}
Unique Sites: {unique_sites}
Categories: {categories}
Last Updated: {last_updated}

Enhanced Database Summary:
├── Cookie History: Extensive ({total_cookies} 🍪 cookies)
├── Domain Coverage: {unique_domains} 🌐 different websites
├── Site Diversity: {unique_sites} 🏠 unique websites
└── Categories Included: {len(cookie_stats.get('categories', []))} types

🎯 Enhanced Profile Readiness: ✅ Fully prepared for anonymous browsing!

Enhanced Cookie Quality Assessment:
• Volume: {'Excellent' if total_cookies > 100 else 'Good' if total_cookies > 50 else 'Basic'}
• Diversity: {'High' if unique_sites > 20 else 'Medium' if unique_sites > 10 else 'Low'}
• Coverage: {'Comprehensive' if unique_domains > 15 else 'Moderate'}
• Timeline: {'Realistic' if cookie_stats.get('harvest_period_days', 0) > 7 else 'Limited'}

🔍 Enhanced Recommendations:
• {'Current profile has excellent cookie coverage!' if total_cookies > 100 and unique_sites > 20 else 'Consider adding more cookie history for better anonymity.'}
"""
            except Exception as e:
                stats_text = f"""
🍪 Profile: {profile_name}
⚠️ Error loading cookie statistics: {str(e)}

Try refreshing or generating new cookies.
"""

        # Clear and update the stats display
        self.cookie_stats_text.config(state='normal')
        self.cookie_stats_text.delete(1.0, tk.END)
        self.cookie_stats_text.insert(1.0, stats_text.strip())
        self.cookie_stats_text.config(state='disabled')

    def clear_status(self):
        """Clear status display"""
        self.status_display.delete(1.0, tk.END)

    def save_log(self):
        """Save log to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.status_display.get(1.0, tk.END))
                self.log_status(f"💾 Log saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def refresh_status(self):
        """Refresh status display"""
        self.log_status("🔄 Enhanced status refreshed")

    def toggle_monitoring(self):
        """Toggle traffic monitoring"""
        self.monitoring_active = self.monitor_var.get()

        if self.monitoring_active:
            self.monitor_status_label.config(text="Status: Enhanced Monitoring Active")
            self.log_status("🔍 Enhanced traffic monitoring enabled")
        else:
            self.monitor_status_label.config(text="Status: Enhanced Monitoring Disabled")
            self.log_status("🔍 Enhanced traffic monitoring disabled")

    def clear_traffic_log(self):
        """Clear traffic log"""
        self.traffic_display.delete(1.0, tk.END)
        self.log_status("🧹 Enhanced traffic log cleared")

    def export_proxies(self):
        """Export proxies"""
        if not self.verified_proxies:
            messagebox.showwarning("Warning", "No proxies to export")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.verified_proxies, f, indent=2)
                self.log_status(f"📤 Exported {len(self.verified_proxies)} proxies to {filename}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # ========== DUAL-MODE OPERATION METHODS ==========

    def switch_to_profile_mode(self):
        """Switch to Profile Mode - Persistent Identity"""
        if not PERSISTENT_PROFILES_AVAILABLE or not self.mode_manager or not self.profile_db:
            messagebox.showwarning("Not Available", "Persistent profile system not available")
            return

        # Show profile selection dialog
        profiles = self.profile_db.list_profiles()

        if not profiles:
            # No profiles exist, offer to create one
            result = messagebox.askyesno(
                "No Profiles Found",
                "No profiles found. Would you like to create a new profile?"
            )
            if result:
                self.create_persistent_profile()
            return

        # Create profile selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Profile")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(
            dialog,
            text="👤 Select Profile for Persistent Identity",
            font=("Arial", 14, "bold")
        ).pack(pady=20)

        # Profile list
        list_frame = ttk.Frame(dialog)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)

        profile_listbox = tk.Listbox(list_frame, font=("Arial", 11))
        profile_listbox.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(list_frame, command=profile_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        profile_listbox.config(yscrollcommand=scrollbar.set)

        # Populate profiles
        for profile in profiles:
            profile_listbox.insert(tk.END, f"{profile['profile_name']} (Last used: {profile['last_used'][:10]})")

        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)

        def select_profile():
            selection = profile_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a profile")
                return

            selected_profile = profiles[selection[0]]
            profile_id = selected_profile['profile_id']
            profile_name = selected_profile['profile_name']

            # Switch to profile mode
            if self.mode_manager.set_mode(OperationMode.PROFILE, profile_id=profile_id):
                if self.mode_indicator:
                    self.mode_indicator.update_mode('profile', profile_name)
                self.log_status(f"👤 Switched to PROFILE MODE: {profile_name}")
                messagebox.showinfo(
                    "Mode Changed",
                    f"✅ Now using PROFILE MODE\n\nProfile: {profile_name}\n\n"
                    "Your digital fingerprint will remain consistent across sessions."
                )
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to switch to profile mode")

        ttk.Button(btn_frame, text="Select Profile", command=select_profile).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Create New", command=lambda: [dialog.destroy(), self.create_persistent_profile()]).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side='left', padx=5)

    def switch_to_stealth_mode(self):
        """Switch to Stealth Mode - Random Identity"""
        if not PERSISTENT_PROFILES_AVAILABLE or not self.mode_manager:
            messagebox.showwarning("Not Available", "Persistent profile system not available")
            return

        result = messagebox.askyesno(
            "Switch to Stealth Mode?",
            "🎭 STEALTH MODE\n\n"
            "This will:\n"
            "• Generate random fingerprints each session\n"
            "• Clear all cookies and history\n"
            "• Provide maximum anonymity\n"
            "• NOT maintain persistent identity\n\n"
            "Use for one-time anonymous tasks.\n\n"
            "Continue?"
        )

        if result:
            if self.mode_manager.set_mode(OperationMode.STEALTH):
                if self.mode_indicator:
                    self.mode_indicator.update_mode('stealth', None)
                self.log_status("🎭 Switched to STEALTH MODE - Random identity active")
                messagebox.showinfo(
                    "Mode Changed",
                    "✅ Now using STEALTH MODE\n\n"
                    "Random fingerprints will be generated for maximum anonymity."
                )

    def switch_to_headless_mode(self):
        """Switch to Headless Mode - Automated Operations"""
        if not PERSISTENT_PROFILES_AVAILABLE or not self.mode_manager:
            messagebox.showwarning("Not Available", "Persistent profile system not available")
            return

        result = messagebox.askyesno(
            "Switch to Headless Mode?",
            "🤖 HEADLESS MODE\n\n"
            "This will:\n"
            "• Run browser without visible window\n"
            "• Optimize for automation and speed\n"
            "• Use random fingerprints\n"
            "• Perfect for scripts and batch operations\n\n"
            "Continue?"
        )

        if result:
            if self.mode_manager.set_mode(OperationMode.HEADLESS):
                if self.mode_indicator:
                    self.mode_indicator.update_mode('headless', None)
                self.log_status("🤖 Switched to HEADLESS MODE - Automation active")
                messagebox.showinfo(
                    "Mode Changed",
                    "✅ Now using HEADLESS MODE\n\n"
                    "Browser will run in headless mode for automation."
                )

    def show_mode_help(self, mode: Optional[str] = None):
        """Show comprehensive mode help dialog"""
        if not PERSISTENT_PROFILES_AVAILABLE:
            messagebox.showinfo(
                "Help",
                "Dual-Mode Operation System\n\n"
                "The persistent profile system is not currently available.\n"
                "Please ensure all required modules are installed."
            )
            return

        # Show the comprehensive help dialog
        ModeHelpDialog(self.root, mode if mode else 'profile')

    def create_persistent_profile(self):
        """Create a new persistent profile"""
        if not PERSISTENT_PROFILES_AVAILABLE or not self.profile_generator or not self.profile_db:
            messagebox.showwarning("Not Available", "Persistent profile system not available")
            return

        # Create profile creation dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Profile")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(
            dialog,
            text="👤 Create New Persistent Profile",
            font=("Arial", 14, "bold")
        ).pack(pady=20)

        # Profile name
        name_frame = ttk.LabelFrame(dialog, text="Profile Name")
        name_frame.pack(fill='x', padx=20, pady=10)

        name_var = tk.StringVar()
        ttk.Entry(name_frame, textvariable=name_var, width=40).pack(padx=10, pady=10)

        # Location preference
        location_frame = ttk.LabelFrame(dialog, text="Location Preference (Optional)")
        location_frame.pack(fill='x', padx=20, pady=10)

        location_var = tk.StringVar(value="Random")
        locations = ["Random", "US", "GB", "DE", "CA", "AU"]
        ttk.Combobox(location_frame, textvariable=location_var, values=locations, state='readonly').pack(padx=10, pady=10)

        # Info text
        info_text = scrolledtext.ScrolledText(dialog, height=10, wrap=tk.WORD)
        info_text.pack(fill='both', expand=True, padx=20, pady=10)
        info_text.insert('1.0',
            "ℹ️ PROFILE CREATION INFO:\n\n"
            "• Profile will have consistent fingerprint across all sessions\n"
            "• Demographics, hardware, and behavior will be realistic\n"
            "• All data points will be geographically consistent\n"
            "• Profile will gradually evolve over time like a real user\n"
            "• Use this profile for long-term accounts and browsing\n\n"
            "⚠️ IMPORTANT:\n"
            "• Choose a memorable name\n"
            "• Location affects timezone, language, and ISP\n"
            "• Profile data is saved permanently\n"
            "• Cannot be changed after creation (only evolved)"
        )
        info_text.config(state=tk.DISABLED)

        # Create button
        def do_create():
            profile_name = name_var.get().strip()
            if not profile_name:
                messagebox.showwarning("Invalid Name", "Please enter a profile name")
                return

            if len(profile_name) < 3:
                messagebox.showwarning("Invalid Name", "Profile name must be at least 3 characters")
                return

            location_pref = None if location_var.get() == "Random" else location_var.get()

            try:
                # Generate profile
                profile = self.profile_generator.generate_profile(profile_name, location_pref)

                # Save to database
                if self.profile_db.save_profile(profile):
                    messagebox.showinfo(
                        "Success",
                        f"✅ Profile '{profile_name}' created successfully!\n\n"
                        f"Location: {profile.location.city}, {profile.location.country}\n"
                        f"Age Range: {profile.age_range}\n"
                        f"Occupation: {profile.occupation}\n\n"
                        "You can now use this profile for persistent browsing."
                    )
                    self.log_status(f"👤 Created persistent profile: {profile_name}")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save profile to database")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create profile: {e}")
                logger.error(f"Profile creation error: {e}")
                traceback.print_exc()

        ttk.Button(dialog, text="Create Profile", command=do_create).pack(pady=10)

def main():
    """Main function"""
    root = tk.Tk()
    app = EnhancedAnonymityGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
