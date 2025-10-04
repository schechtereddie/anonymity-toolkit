#!/usr/bin/env python3
"""
Profile-Consistent Fingerprinting System
Ensures browser fingerprint matches profile data for maximum authenticity
"""

import json
import os
import random
import hashlib
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class BrowserFingerprint:
    """Complete browser fingerprint matching profile data"""

    # Basic browser info
    user_agent: str
    platform: str
    language: str
    timezone: str
    screen_resolution: str

    # Hardware fingerprint
    hardware_concurrency: int
    device_memory: int
    screen_depth: int
    screen_pixel_ratio: float

    # Software fingerprint
    vendor: str
    renderer: str
    webgl_vendor: str
    webgl_renderer: str

    # Font fingerprint
    fonts: list

    # Canvas fingerprint
    canvas_hash: str

    # WebRTC fingerprint
    webrtc_ip: str

    # Plugin fingerprint
    plugins: list

    # Cookie fingerprint
    cookie_enabled: bool
    do_not_track: bool

    def to_chrome_options(self) -> list:
        """Convert fingerprint to Chrome options"""
        options = []

        # User agent
        if self.user_agent:
            options.extend(['--user-agent', self.user_agent])

        # Language and timezone
        if self.language:
            options.append(f'--lang={self.language}')

        # Disable WebRTC for privacy
        options.extend([
            '--disable-webrtc',
            '--disable-features=VizDisplayCompositor'
        ])

        # Disable plugins for consistency
        options.extend([
            '--disable-plugins',
            '--disable-extensions',
            '--disable-default-apps'
        ])

        # Screen and display settings
        if self.screen_resolution:
            width, height = self.screen_resolution.split('x')
            options.extend([
                f'--window-size={width},{height}',
                f'--start-maximized'
            ])

        # Additional stealth options
        options.extend([
            '--disable-blink-features=AutomationControlled',
            '--disable-features=VizDisplayCompositor',
            '--disable-ipc-flooding-protection',
            '--disable-background-timer-throttling',
            '--disable-renderer-backgrounding',
            '--disable-backgrounding-occluded-windows',
            '--disable-field-trial-config',
            '--disable-back-forward-cache',
            '--disable-historical-tab-close-ranking',
            '--disable-features=TranslateUI',
            '--disable-features=BlinkGenPropertyTrees'
        ])

        return options

    def to_firefox_options(self) -> dict:
        """Convert fingerprint to Firefox options"""
        options = {
            'user-agent': self.user_agent,
            'platform': self.platform,
            'language': self.language,
            'timezone': self.timezone,
            'screen_resolution': self.screen_resolution,
            'hardware_concurrency': self.hardware_concurrency,
            'device_memory': self.device_memory
        }
        return options

class ProfileFingerprintManager:
    """Manages browser fingerprints that are consistent with profile data"""

    def __init__(self):
        self.fingerprint_cache = {}
        self.fonts_db = self._load_font_database()

    def _load_font_database(self) -> list:
        """Load common font database for realistic font fingerprinting"""
        return [
            'Arial', 'Helvetica', 'Times New Roman', 'Courier New', 'Georgia',
            'Verdana', 'Geneva', 'Tahoma', 'Trebuchet MS', 'Impact', 'Comic Sans MS',
            'Lucida Grande', 'Lucida Sans Unicode', 'Palatino Linotype', 'Book Antiqua',
            'Arial Black', 'Arial Narrow', 'Century Gothic', 'Consolas', 'Courier',
            'Garamond', 'Monaco', 'MS Sans Serif', 'Symbol', 'Tahoma', 'Times',
            'Wingdings', 'Webdings', 'Apple Symbols', 'Zapf Dingbats'
        ]

    def generate_fingerprint(self, profile_data: Dict[str, Any]) -> BrowserFingerprint:
        """
        Generate a browser fingerprint that matches the profile data
        """
        profile_id = profile_data.get('profile_name', 'default')

        # Check cache first
        if profile_id in self.fingerprint_cache:
            return self.fingerprint_cache[profile_id]

        # Generate fingerprint based on profile data
        fingerprint = BrowserFingerprint(
            user_agent=profile_data.get('user_agent', self._generate_user_agent(profile_data)),
            platform=profile_data.get('platform', 'Win32'),
            language=profile_data.get('language', 'en-US,en;q=0.9'),
            timezone=profile_data.get('timezone', 'America/New_York'),
            screen_resolution=profile_data.get('screen_resolution', '1920x1080'),
            hardware_concurrency=self._generate_hardware_concurrency(),
            device_memory=self._generate_device_memory(),
            screen_depth=24,
            screen_pixel_ratio=1.0,
            vendor='Google Inc.',
            renderer='ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)',
            webgl_vendor='Google Inc. (Intel)',
            webgl_renderer='ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)',
            fonts=self._generate_font_list(),
            canvas_hash=self._generate_canvas_hash(profile_data),
            webrtc_ip='',
            plugins=[],
            cookie_enabled=True,
            do_not_track=False
        )

        # Cache the fingerprint
        self.fingerprint_cache[profile_id] = fingerprint
        return fingerprint

    def _generate_user_agent(self, profile_data: Dict[str, Any]) -> str:
        """Generate user agent based on profile data"""
        platform = profile_data.get('platform', 'Win32')
        browser_type = 'chrome'  # Default to Chrome

        # Detect browser type from user agent if available
        existing_ua = profile_data.get('user_agent', '')
        if 'Firefox' in existing_ua:
            browser_type = 'firefox'
        elif 'Safari' in existing_ua:
            browser_type = 'safari'
        elif 'Edge' in existing_ua:
            browser_type = 'edge'

        # Generate realistic user agent based on platform and browser
        user_agents = {
            'chrome': {
                'Win32': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Linux': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Darwin': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            },
            'firefox': {
                'Win32': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
                'Linux': 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
                'Darwin': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'
            }
        }

        return user_agents.get(browser_type, user_agents['chrome']).get(platform, user_agents['chrome']['Win32'])

    def _generate_hardware_concurrency(self) -> int:
        """Generate realistic hardware concurrency value"""
        return random.choice([2, 4, 6, 8, 12, 16])

    def _generate_device_memory(self) -> int:
        """Generate realistic device memory value"""
        return random.choice([4, 8, 16, 32])

    def _generate_font_list(self) -> list:
        """Generate realistic font list based on OS"""
        base_fonts = ['Arial', 'Helvetica', 'Times New Roman', 'Courier New']

        # Add OS-specific fonts
        if random.random() > 0.5:  # Windows
            base_fonts.extend(['Segoe UI', 'Tahoma', 'Verdana', 'MS Sans Serif'])
        else:  # macOS
            base_fonts.extend(['Lucida Grande', 'Geneva', 'Helvetica Neue'])

        # Add some random fonts from the database
        available_fonts = [f for f in self.fonts_db if f not in base_fonts]
        additional_fonts = random.sample(available_fonts, random.randint(5, 15))

        return base_fonts + additional_fonts

    def _generate_canvas_hash(self, profile_data: Dict[str, Any]) -> str:
        """Generate consistent canvas hash based on profile"""
        # Create a deterministic hash based on profile data
        profile_string = f"{profile_data.get('profile_name', 'default')}_{profile_data.get('user_agent', '')}"
        return hashlib.md5(profile_string.encode()).hexdigest()[:16]

    def get_fingerprint_score(self, fingerprint: BrowserFingerprint, profile_data: Dict[str, Any]) -> int:
        """
        Calculate how well the fingerprint matches the profile data
        Returns score from 0-100
        """
        score = 100

        # Check user agent consistency
        if profile_data.get('user_agent') and fingerprint.user_agent != profile_data['user_agent']:
            score -= 20

        # Check geographic consistency
        if profile_data.get('timezone') and fingerprint.timezone != profile_data['timezone']:
            score -= 15

        if profile_data.get('language') and fingerprint.language != profile_data['language']:
            score -= 15

        # Check screen resolution consistency
        if profile_data.get('screen_resolution') and fingerprint.screen_resolution != profile_data['screen_resolution']:
            score -= 10

        return max(0, score)

    def save_fingerprint(self, profile_id: str, fingerprint: BrowserFingerprint):
        """Save fingerprint to cache and file"""
        self.fingerprint_cache[profile_id] = fingerprint

        # Save to file for persistence
        fingerprint_file = f"src/data/fingerprints_{profile_id}.json"
        os.makedirs('src/data', exist_ok=True)

        fingerprint_data = {
            'profile_id': profile_id,
            'user_agent': fingerprint.user_agent,
            'platform': fingerprint.platform,
            'language': fingerprint.language,
            'timezone': fingerprint.timezone,
            'screen_resolution': fingerprint.screen_resolution,
            'hardware_concurrency': fingerprint.hardware_concurrency,
            'device_memory': fingerprint.device_memory,
            'canvas_hash': fingerprint.canvas_hash,
            'created_at': int(time.time())
        }

        try:
            with open(fingerprint_file, 'w') as f:
                json.dump(fingerprint_data, f, indent=2)
        except Exception as e:
            print(f"Error saving fingerprint: {e}")

    def load_fingerprint(self, profile_id: str) -> Optional[BrowserFingerprint]:
        """Load fingerprint from cache or file"""
        # Check cache first
        if profile_id in self.fingerprint_cache:
            return self.fingerprint_cache[profile_id]

        # Try to load from file
        fingerprint_file = f"src/data/fingerprints_{profile_id}.json"
        if os.path.exists(fingerprint_file):
            try:
                with open(fingerprint_file, 'r') as f:
                    data = json.load(f)

                fingerprint = BrowserFingerprint(
                    user_agent=data.get('user_agent', ''),
                    platform=data.get('platform', 'Win32'),
                    language=data.get('language', 'en-US,en;q=0.9'),
                    timezone=data.get('timezone', 'America/New_York'),
                    screen_resolution=data.get('screen_resolution', '1920x1080'),
                    hardware_concurrency=data.get('hardware_concurrency', 4),
                    device_memory=data.get('device_memory', 8),
                    screen_depth=24,
                    screen_pixel_ratio=1.0,
                    vendor='Google Inc.',
                    renderer='ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                    webgl_vendor='Google Inc. (Intel)',
                    webgl_renderer='ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                    fonts=self._generate_font_list(),
                    canvas_hash=data.get('canvas_hash', ''),
                    webrtc_ip='',
                    plugins=[],
                    cookie_enabled=True,
                    do_not_track=False
                )

                self.fingerprint_cache[profile_id] = fingerprint
                return fingerprint

            except Exception as e:
                print(f"Error loading fingerprint: {e}")

        return None
