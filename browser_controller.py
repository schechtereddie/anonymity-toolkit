#!/usr/bin/env python3
"""
Browser Controller - Full selenium webdriver integration for manual browser control
"""
import json
import time
import threading
import os
from typing import Optional, Dict, Any, cast
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import random

class BrowserController:
    """Advanced browser control with selenium webdriver"""

    def __init__(self):
        self.driver = None
        self.ua = UserAgent()
        self.performance_stats: Dict[str, float] = {
            'requests': 0.0,
            'successful_requests': 0.0,
            'total_time': 0.0,
            'avg_response_time': 0.0
        }

    def start_manual_browser(self, proxy: Optional[str] = None, user_agent: Optional[str] = None) -> bool:
        """Start a manual browser session with privacy settings"""
        try:
            # Configure Chrome options for privacy
            chrome_options = Options()

            # Basic privacy settings
            chrome_options.add_argument('--incognito')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_argument('--disable-extensions-http-throttling')
            chrome_options.add_argument('--disable-background-timer-throttling')
            chrome_options.add_argument('--disable-renderer-backgrounding')
            chrome_options.add_argument('--disable-backgrounding-occluded-windows')

            # Canvas/WebGL protection
            chrome_options.add_argument('--disable-reading-from-canvas')
            chrome_options.add_argument('--disable-accelerated-video-decode')

            # Set user agent if provided
            if user_agent:
                chrome_options.add_argument(f'--user-agent={user_agent}')
            else:
                chrome_options.add_argument(f'--user-agent={self.ua.random}')

            # Proxy configuration
            if proxy:
                chrome_options.add_argument(f'--proxy-server=socks5://{proxy}')

            # Disable automation detection
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")

            # Start browser
            try:
                self.driver = webdriver.Chrome(options=chrome_options)

                # Execute script to remove webdriver property
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

                return True

            except Exception as e:
                print(f"Chrome not found, trying Firefox: {e}")
                # Fallback to Firefox
                firefox_options = webdriver.FirefoxOptions()
                firefox_options.add_argument('--private')
                firefox_options.add_argument('--incognito')

                if user_agent:
                    firefox_options.set_preference("general.useragent.override", user_agent)

                if proxy:
                    firefox_options.set_preference("network.proxy.type", 1)
                    firefox_options.set_preference("network.proxy.socks", proxy.split(':')[0])
                    firefox_options.set_preference("network.proxy.socks_port", int(proxy.split(':')[1]))

                self.driver = webdriver.Firefox(options=firefox_options)
                return True

        except Exception as e:
            print(f"Failed to start browser: {e}")
            return False

    def navigate_to(self, url: str, timeout: int = 30) -> bool:
        """Navigate to URL with timing and error handling"""
        start_time = time.time()

        if not self.driver:
            print("Error: Browser not started. Cannot navigate.")
            return False

        try:
            self.driver.get(url)

            # Wait for page to load
            # Cast self.driver to WebDriver to satisfy Pylance
            WebDriverWait(cast(webdriver.Remote, self.driver), timeout).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )

            load_time = time.time() - start_time
            self.performance_stats['requests'] += 1
            self.performance_stats['successful_requests'] += 1
            self.performance_stats['total_time'] += load_time
            self.performance_stats['avg_response_time'] = self.performance_stats['total_time'] / self.performance_stats['requests']

            return True

        except Exception as e:
            load_time = time.time() - start_time
            self.performance_stats['requests'] += 1
            self.performance_stats['total_time'] += load_time
            print(f"Navigation failed to {url}: {e}")
            return False

    def get_browser_fingerprint_analysis(self) -> Dict[str, Any]:
        """Comprehensive browser fingerprint analysis"""
        fingerprint_data = {}

        if not self.driver:
            return {"error": "Browser not started"}

        try:
            # Basic fingerprinting data
            fingerprint_data['user_agent'] = self.driver.execute_script("return navigator.userAgent;")
            fingerprint_data['platform'] = self.driver.execute_script("return navigator.platform;")
            fingerprint_data['language'] = self.driver.execute_script("return navigator.language;")
            fingerprint_data['languages'] = self.driver.execute_script("return navigator.languages;")
            fingerprint_data['cookie_enabled'] = self.driver.execute_script("return navigator.cookieEnabled;")
            fingerprint_data['do_not_track'] = self.driver.execute_script("return navigator.doNotTrack;")
            fingerprint_data['timezone_offset'] = self.driver.execute_script("return new Date().getTimezoneOffset();")

            # Screen properties
            fingerprint_data['screen_width'] = self.driver.execute_script("return screen.width;")
            fingerprint_data['screen_height'] = self.driver.execute_script("return screen.height;")
            fingerprint_data['screen_avail_width'] = self.driver.execute_script("return screen.availWidth;")
            fingerprint_data['screen_avail_height'] = self.driver.execute_script("return screen.availHeight;")
            fingerprint_data['screen_color_depth'] = self.driver.execute_script("return screen.colorDepth;")
            fingerprint_data['screen_pixel_ratio'] = self.driver.execute_script("return window.devicePixelRatio;")

            # WebGL fingerprinting
            try:
                fingerprint_data['webgl_vendor'] = self.driver.execute_script("""
                    var canvas = document.createElement('canvas');
                    var gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                    if (gl) {
                        var debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                        return debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : null;
                    }
                    return null;
                """)

                fingerprint_data['webgl_renderer'] = self.driver.execute_script("""
                    var canvas = document.createElement('canvas');
                    var gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                    if (gl) {
                        var debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                        return debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : null;
                    }
                    return null;
                """)
            except:
                fingerprint_data['webgl_fingerprint'] = "Not available"

            # Canvas fingerprinting
            try:
                fingerprint_data['canvas_fingerprint'] = self.driver.execute_script("""
                    var canvas = document.createElement('canvas');
                    var ctx = canvas.getContext('2d');
                    ctx.textBaseline = 'top';
                    ctx.font = '14px Arial';
                    ctx.textBaseline = 'alphabetic';
                    ctx.fillStyle = '#f60';
                    ctx.fillRect(125,1,62,20);
                    ctx.fillStyle = '#069';
                    ctx.fillText('BrowserLeaks,com <canvas> 1.0',2,15);
                    ctx.fillStyle = 'rgba(102, 204, 0, 0.7)';
                    ctx.fillText('BrowserLeaks,com <canvas> 1.0',4,17);
                    return canvas.toDataURL().slice(-50);
                """)
            except:
                fingerprint_data['canvas_fingerprint'] = "Not available"

            # WebRTC leak detection
            fingerprint_data['webrtc_available'] = self.driver.execute_script("""
                return !!(window.RTCPeerConnection || window.webkitRTCPeerConnection || window.mozRTCPeerConnection);
            """)

            # Plugin enumeration (limited)
            fingerprint_data['plugins'] = self.driver.execute_script("return navigator.plugins.length;")

            # Touch support (mobile detection)
            fingerprint_data['touch_support'] = self.driver.execute_script("return 'ontouchstart' in window;")

            # Hardware concurrency
            fingerprint_data['hardware_concurrency'] = self.driver.execute_script("return navigator.hardwareConcurrency || 2;")

            fingerprint_data['analysis_complete'] = True

        except Exception as e:
            fingerprint_data['error'] = str(e)

        return fingerprint_data

    def check_leaks_detailed(self) -> Dict[str, Any]:
        """Advanced leak detection using browser"""
        leak_results = {
            'dns_leaks': [],
            'webrtc_leaks': [],
            'canvas_fingerprintable': False,
            'webgl_fingerprintable': False,
            'timestamp': time.time()
        }

        if not self.driver:
            return {"error": "Browser not started"}

        try:
            # WebRTC leak testing
            webrtc_available = self.driver.execute_script("""
                return !!(window.RTCPeerConnection || window.webkitRTCPeerConnection || window.mozRTCPeerConnection);
            """)

            leak_results['webrtc_available'] = webrtc_available

            if webrtc_available:
                # Test actual WebRTC leak (simplified)
                try:
                    leak_results['webrtc_test_result'] = self.driver.execute_script("""
                        try {
                            var RTCPeerConnection = window.RTCPeerConnection || window.webkitRTCPeerConnection || window.mozRTCPeerConnection;
                            var pc = new RTCPeerConnection({iceServers: []});
                            pc.createDataChannel('');
                            pc.createOffer(function(sdp) {
                                window.webrtc_offer_created = true;
                            }, function(e) { window.webrtc_error = e; });
                            return {webrtc_offer_created: window.webrtc_offer_created, error: window.webrtc_error};
                        } catch(e) {
                            return {error: e.message};
                        }
                    """)
                except Exception as e:
                    leak_results['webrtc_test_result'] = str(e)

            # Canvas fingerprinting assessment
            canvas_hash = self.driver.execute_script("""
                try {
                    var canvas = document.createElement('canvas');
                    var ctx = canvas.getContext('2d');
                    ctx.font = '12px Arial';
                    ctx.fillText('Fingerprint', 10, 10);
                    ctx.fillStyle = 'red';
                    ctx.fillRect(0, 0, 10, 10);
                    return canvas.toDataURL();
                } catch(e) {
                    return null;
                }
            """)

            leak_results['canvas_fingerprint'] = canvas_hash
            leak_results['canvas_fingerprintable'] = canvas_hash is not None and len(str(canvas_hash)) > 50

            # Advanced fingerprinting score
            fingerprint_data = self.get_browser_fingerprint_analysis()

            # Calculate entropy/fingerprintability score
            unique_values = len(set(str(v) for v in fingerprint_data.values() if not str(v).startswith('error')))
            total_fields = len([k for k in fingerprint_data.keys() if not k.startswith('error')])

            if total_fields > 0:
                leak_results['fingerprintability_score'] = (unique_values / total_fields) * 100
            else:
                leak_results['fingerprintability_score'] = 0

            leak_results['privacy_rating'] = self._calculate_privacy_rating(leak_results)

        except Exception as e:
            leak_results['error'] = str(e)

        return leak_results

    def _calculate_privacy_rating(self, leak_results: Dict[str, Any]) -> str:
        """Calculate privacy rating based on leak analysis"""
        score = 0

        # WebRTC availability reduces privacy
        if leak_results.get('webrtc_available', False):
            score += 20

        # Canvas fingerprinting reduces privacy
        if leak_results.get('canvas_fingerprintable', False):
            score += 30

        # WebGL fingerprinting (if has distinct vendor/renderer)
        if leak_results.get('webgl_vendor') and leak_results.get('webgl_renderer'):
            score += 25

        # Fingerprintability score
        fp_score = leak_results.get('fingerprintability_score', 0)
        score += fp_score * 0.25  # 25% weight

        if score < 30:
            return "Excellent Privacy"
        elif score < 50:
            return "Good Privacy"
        elif score < 70:
            return "Moderate Privacy"
        else:
            return "Poor Privacy"

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get browser performance statistics"""
        if not self.driver:
            return {"error": "Browser not started"}

        stats = self.performance_stats.copy()

        try:
            navigation_timing = self.driver.execute_script("""
                try {
                    var perfData = performance.timing;
                    return {
                        navigation_start: perfData.navigationStart,
                        load_event_end: perfData.loadEventEnd,
                        dom_content_loaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                        total_load_time: perfData.loadEventEnd - perfData.navigationStart
                    };
                } catch(e) {
                    return null;
                }
            """)

            if navigation_timing:
                stats['page_load_timing'] = navigation_timing

            # Resource loading info
            resources = self.driver.execute_script("""
                try {
                    var resources = performance.getEntriesByType('resource');
                    return resources.length;
                } catch(e) {
                    return 0;
                }
            """)

            stats['resources_loaded'] = resources

        except Exception as e:
            stats['timing_error'] = str(e)

        return stats

    def close_browser(self):
        """Safely close the browser"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                print("Browser closed successfully")
            except Exception as e:
                print(f"Error closing browser: {e}")

    def get_driver(self):
        """Return the current WebDriver instance"""
        return self.driver

# Configuration persistence
class BrowserConfigManager:
    """Manages browser configuration settings"""

    def __init__(self, config_file: str = "browser_config.json"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                return self.get_default_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.get_default_config()

    def save_config(self):
        """Save current configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "last_proxy": None,
            "last_user_agent": None,
            "preferred_browser": "chrome",
            "privacy_settings": {
                "block_webrtc": True,
                "disable_canvas_fingerprinting": True,
                "randomize_timezone": False,
                "disable_plugins": False
            },
            "performance_settings": {
                "enable_monitoring": True,
                "log_requests": False,
                "collect_fingerprints": True
            },
            "quick_sites": [
                "https://whatismyipaddress.com/",
                "https://www.google.com/",
                "https://github.com/",
                "https://stackoverflow.com/"
            ],
            "last_used": None,
            "session_count": 0
        }

    def update_setting(self, key: str, value: Any):
        """Update a configuration setting"""
        keys = key.split('.')
        conf = self.config

        for k in keys[:-1]:
            if k not in conf:
                conf[k] = {}
            conf = conf[k]

        conf[keys[-1]] = value
        self.save_config()

    def get_setting(self, key: str, default=None):
        """Get a configuration setting"""
        keys = key.split('.')
        conf = self.config

        try:
            for k in keys:
                conf = conf[k]
            return conf
        except KeyError:
            return default
