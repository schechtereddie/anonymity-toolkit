#!/usr/bin/env python3
"""
User Browser Integration - Real web browser with complete anonymity features
Launches actual browser that users can use for normal web surfing with all stealth features
"""

import os
import json
import time
import subprocess
import threading
import psutil
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
import tempfile
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserStealthBrowser:
    """Real web browser with complete anonymity integration"""

    def __init__(self):
        self.browser_processes = {}
        self.session_monitors = {}
        self.fingerprint_manager = None
        self.status_callbacks = []

    def set_fingerprint_manager(self, manager):
        """Set the fingerprint manager for profile-consistent fingerprinting"""
        self.fingerprint_manager = manager

    def add_status_callback(self, callback):
        """Add callback for real-time status updates"""
        self.status_callbacks.append(callback)

    def _update_status(self, message: str, status_type: str = "info"):
        """Update status to all registered callbacks"""
        for callback in self.status_callbacks:
            try:
                callback(message, status_type)
            except Exception as e:
                logger.error(f"Status callback error: {e}")

    def launch_anonymous_browser(self, proxy: Optional[str] = None, profile_data: Optional[Dict[str, Any]] = None,
                                browser_type: str = "chrome", url: str = "https://whatismyipaddress.com/") -> bool:
        """
        Launch real browser with complete anonymity integration

        Args:
            proxy: SOCKS5 proxy (ip:port format)
            profile_data: Profile configuration data
            browser_type: Browser to launch (chrome, firefox, edge, brave)
            url: Starting URL

        Returns:
            bool: True if browser launched successfully
        """
        try:
            self._update_status("🚀 Initializing anonymous browser...", "info")

            # Validate inputs
            if not profile_data:
                self._update_status("❌ No profile data provided", "error")
                return False

            # Check if browser is installed
            if not self._check_browser_installed(browser_type):
                self._update_status(f"❌ {browser_type} browser not found. Please install it first.", "error")
                return False

            # Generate profile-consistent fingerprint
            if self.fingerprint_manager:
                fingerprint = self.fingerprint_manager.generate_fingerprint(profile_data)
                fingerprint_score = self.fingerprint_manager.get_fingerprint_score(fingerprint, profile_data)
                self._update_status(f"🔍 Generated fingerprint (Score: {fingerprint_score}/100)", "info")
            else:
                fingerprint = None
                self._update_status("⚠️ No fingerprint manager available", "warning")

            # Create temporary profile directory for this session
            session_profile_dir = self._create_session_profile(profile_data, fingerprint)

            # Build browser command with all stealth features
            command, env_vars = self._build_browser_command(
                browser_type, proxy, profile_data, fingerprint, session_profile_dir, url
            )

            # Launch browser
            self._update_status(f"🌐 Launching {browser_type} with stealth features...", "info")

            process = subprocess.Popen(
                command,
                env={**os.environ, **env_vars},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Track the process
            session_id = f"{profile_data.get('profile_name', 'default')}_{int(time.time())}"
            self.browser_processes[session_id] = {
                'process': process,
                'browser_type': browser_type,
                'proxy': proxy,
                'profile_data': profile_data,
                'fingerprint': fingerprint,
                'start_time': time.time(),
                'session_profile_dir': session_profile_dir
            }

            # Start monitoring thread
            monitor_thread = threading.Thread(
                target=self._monitor_browser_session,
                args=(session_id,),
                daemon=True
            )
            monitor_thread.start()
            self.session_monitors[session_id] = monitor_thread

            self._update_status(f"✅ Browser launched successfully (PID: {process.pid})", "success")
            self._update_status(f"🔗 Session ID: {session_id}", "info")

            return True

        except Exception as e:
            self._update_status(f"❌ Browser launch failed: {e}", "error")
            return False

    def _check_browser_installed(self, browser_type: str) -> bool:
        """Check if the specified browser is installed"""
        browser_commands = {
            'chrome': ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser'],
            'firefox': ['firefox', 'firefox-bin'],
            'edge': ['microsoft-edge', 'microsoft-edge-stable'],
            'brave': ['brave-browser', 'brave']
        }

        commands = browser_commands.get(browser_type.lower(), [])
        for cmd in commands:
            if shutil.which(cmd):
                return True
        return False

    def _create_session_profile(self, profile_data: Dict[str, Any], fingerprint = None) -> str:
        """Create temporary profile directory for this session"""
        try:
            # Create base temp directory
            temp_dir = tempfile.mkdtemp(prefix="anon_browser_")

            # Create user data directory
            user_data_dir = os.path.join(temp_dir, "user_data")
            os.makedirs(user_data_dir, exist_ok=True)

            # Save profile configuration
            profile_config = {
                'profile_data': profile_data,
                'session_start': int(time.time()),
                'fingerprint_applied': fingerprint is not None
            }

            with open(os.path.join(user_data_dir, 'profile_config.json'), 'w') as f:
                json.dump(profile_config, f, indent=2)

            # Create preferences file for browser
            self._create_browser_preferences(user_data_dir, profile_data, fingerprint)

            return user_data_dir

        except Exception as e:
            logger.error(f"Error creating session profile: {e}")
            return tempfile.mkdtemp(prefix="anon_browser_fallback_")

    def _create_browser_preferences(self, user_data_dir: str, profile_data: Dict[str, Any], fingerprint = None):
        """Create browser-specific preference files"""
        try:
            # Chrome preferences
            chrome_prefs = {
                'profile': {
                    'name': profile_data.get('profile_name', 'Anonymous'),
                    'avatar_index': 0
                },
                'browser': {
                    'check_default_browser': False,
                    'show_home_button': False
                },
                'homepage_is_newtabpage': True,
                'session': {
                    'restore_on_startup': 4,  # Restore from URL
                    'startup_urls': ['https://whatismyipaddress.com/']
                }
            }

            prefs_dir = os.path.join(user_data_dir, 'Default')
            os.makedirs(prefs_dir, exist_ok=True)

            with open(os.path.join(prefs_dir, 'Preferences'), 'w') as f:
                json.dump(chrome_prefs, f, indent=2)

        except Exception as e:
            logger.error(f"Error creating browser preferences: {e}")

    def _build_browser_command(self, browser_type: str, proxy: Optional[str], profile_data: Dict[str, Any],
                              fingerprint, session_profile_dir: str, url: str) -> tuple:
        """Build browser command with all stealth features"""

        browser_commands = {
            'chrome': 'google-chrome',
            'firefox': 'firefox',
            'edge': 'microsoft-edge',
            'brave': 'brave-browser'
        }

        base_command = browser_commands.get(browser_type.lower(), 'google-chrome')
        command = [base_command]

        # Add user data directory
        command.extend(['--user-data-dir', session_profile_dir])

        # Add stealth arguments based on browser type
        if browser_type.lower() == 'chrome':
            command.extend(self._get_chrome_stealth_args(proxy, profile_data, fingerprint))
        elif browser_type.lower() == 'firefox':
            command.extend(self._get_firefox_stealth_args(proxy, profile_data, fingerprint))
        elif browser_type.lower() == 'edge':
            command.extend(self._get_edge_stealth_args(proxy, profile_data, fingerprint))
        elif browser_type.lower() == 'brave':
            command.extend(self._get_brave_stealth_args(proxy, profile_data, fingerprint))

        # Add URL
        command.append(url)

        # Environment variables
        env_vars = os.environ.copy()

        # Add proxy environment variables if needed
        if proxy:
            env_vars['HTTP_PROXY'] = f'socks5://{proxy}'
            env_vars['HTTPS_PROXY'] = f'socks5://{proxy}'

        return command, env_vars

    def _get_chrome_stealth_args(self, proxy: Optional[str], profile_data: Dict[str, Any], fingerprint) -> list:
        """Get Chrome-specific stealth arguments"""
        args = [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-software-rasterizer',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-features=VizDisplayCompositor',
            '--disable-ipc-flooding-protection',
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=TranslateUI',
            '--disable-features=BlinkGenPropertyTrees',
            '--disable-client-side-phishing-detection',
            '--disable-component-extensions-with-background-pages',
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-images',  # Optional: can be removed for better UX
            '--disable-javascript',  # Optional: can be removed for better UX
            '--incognito',
            '--new-window',
            '--disable-logging',
            '--disable-login-animations',
            '--disable-notifications',
            '--disable-popup-blocking',
            '--no-first-run',
            '--no-default-browser-check',
            '--no-pings',
            '--no-zygote',
            '--disable-background-networking',
            '--disable-breakpad',
            '--disable-crash-reporter',
            '--disable-hang-monitor',
            '--disable-metrics',
            '--disable-metrics-reporting',
            '--disable-sync',
            '--disable-translate',
            '--hide-scrollbars',
            '--metrics-recording-only',
            '--mute-audio',
            '--no-crash-upload',
            '--disable-webrtc'
        ]

        # Add proxy if specified
        if proxy:
            args.extend(['--proxy-server', f'socks5://{proxy}'])

        # Add fingerprint-based arguments
        if fingerprint:
            chrome_options = fingerprint.to_chrome_options()
            args.extend(chrome_options)

        # Add profile-specific arguments
        if profile_data.get('screen_resolution'):
            width, height = profile_data['screen_resolution'].split('x')
            args.extend([
                '--window-size', f'{width},{height}',
                '--window-position', '0,0'
            ])

        return args

    def _get_firefox_stealth_args(self, proxy: Optional[str], profile_data: Dict[str, Any], fingerprint) -> list:
        """Get Firefox-specific stealth arguments"""
        args = [
            '--private-window',
            '--new-instance',
            '--safe-mode',
            '--disable-background-tasks',
            '--disable-crash-reporter',
            '--disable-mozilla-data-reporting',
            '--disable-ping',
            '--disable-telemetry',
            '--disable-default-browser-agent',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-images',  # Optional
            '--disable-javascript',  # Optional
            '--disable-background-networking'
        ]

        if proxy:
            args.extend(['--proxy', f'socks5://{proxy}'])

        return args

    def _get_edge_stealth_args(self, proxy: Optional[str], profile_data: Dict[str, Any], fingerprint) -> list:
        """Get Edge-specific stealth arguments"""
        # Edge uses similar arguments to Chrome
        return self._get_chrome_stealth_args(proxy, profile_data, fingerprint)

    def _get_brave_stealth_args(self, proxy: Optional[str], profile_data: Dict[str, Any], fingerprint) -> list:
        """Get Brave-specific stealth arguments"""
        # Brave uses similar arguments to Chrome
        return self._get_chrome_stealth_args(proxy, profile_data, fingerprint)

    def _monitor_browser_session(self, session_id: str):
        """Monitor browser session health and performance"""
        try:
            session_info = self.browser_processes.get(session_id)
            if not session_info:
                return

            process = session_info['process']
            start_time = session_info['start_time']

            while process.poll() is None:  # Process is still running
                try:
                    # Check if process is still alive
                    if process.poll() is not None:
                        break

                    # Get process info
                    proc = psutil.Process(process.pid)

                    # Calculate session duration
                    duration = time.time() - start_time

                    # Check memory usage
                    memory_mb = proc.memory_info().rss / 1024 / 1024

                    # Update status every 30 seconds
                    if int(duration) % 30 == 0:
                        self._update_status(
                            f"🔄 Browser session active ({int(duration)}s, {memory_mb:.1f}MB)",
                            "info"
                        )

                    time.sleep(10)

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break
                except Exception as e:
                    logger.error(f"Error monitoring session {session_id}: {e}")
                    break

            # Session ended
            self._cleanup_session(session_id)

        except Exception as e:
            logger.error(f"Error in session monitor for {session_id}: {e}")

    def _cleanup_session(self, session_id: str):
        """Clean up browser session resources"""
        try:
            session_info = self.browser_processes.get(session_id)
            if not session_info:
                return

            # Kill process if still running
            process = session_info['process']
            if process.poll() is None:
                try:
                    parent = psutil.Process(process.pid)
                    children = parent.children(recursive=True)
                    for child in children:
                        child.kill()
                    parent.kill()
                except:
                    pass

            # Clean up temporary profile directory
            profile_dir = session_info.get('session_profile_dir')
            if profile_dir and os.path.exists(profile_dir):
                try:
                    shutil.rmtree(profile_dir)
                except Exception as e:
                    logger.error(f"Error cleaning up profile directory: {e}")

            # Remove from tracking
            self.browser_processes.pop(session_id, None)
            self.session_monitors.pop(session_id, None)

            self._update_status(f"🧹 Browser session {session_id} cleaned up", "info")

        except Exception as e:
            logger.error(f"Error during session cleanup: {e}")

    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Get information about active browser sessions"""
        active_sessions = []

        for session_id, session_info in self.browser_processes.items():
            process = session_info['process']

            if process.poll() is None:  # Process still running
                try:
                    proc = psutil.Process(process.pid)
                    memory_mb = proc.memory_info().rss / 1024 / 1024
                    duration = time.time() - session_info['start_time']

                    active_sessions.append({
                        'session_id': session_id,
                        'browser_type': session_info['browser_type'],
                        'proxy': session_info['proxy'],
                        'profile_name': session_info['profile_data'].get('profile_name', 'Unknown'),
                        'duration_seconds': int(duration),
                        'memory_mb': round(memory_mb, 1),
                        'pid': process.pid
                    })

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    # Process died, clean it up
                    self._cleanup_session(session_id)

        return active_sessions

    def terminate_session(self, session_id: str) -> bool:
        """Terminate a specific browser session"""
        try:
            if session_id in self.browser_processes:
                self._cleanup_session(session_id)
                self._update_status(f"🛑 Browser session {session_id} terminated", "info")
                return True
            else:
                self._update_status(f"❌ Session {session_id} not found", "error")
                return False

        except Exception as e:
            self._update_status(f"❌ Error terminating session: {e}", "error")
            return False

    def terminate_all_sessions(self) -> int:
        """Terminate all active browser sessions"""
        session_ids = list(self.browser_processes.keys())
        terminated_count = 0

        for session_id in session_ids:
            if self.terminate_session(session_id):
                terminated_count += 1

        if terminated_count > 0:
            self._update_status(f"🛑 Terminated {terminated_count} browser sessions", "info")

        return terminated_count

    def get_browser_status(self) -> Dict[str, Any]:
        """Get comprehensive browser status"""
        active_sessions = self.get_active_sessions()

        return {
            'total_sessions': len(self.browser_processes),
            'active_sessions': len(active_sessions),
            'sessions': active_sessions,
            'supported_browsers': self._get_supported_browsers(),
            'system_resources': self._get_system_resources()
        }

    def _get_supported_browsers(self) -> Dict[str, bool]:
        """Check which browsers are installed and available"""
        browsers = ['chrome', 'firefox', 'edge', 'brave']
        availability = {}

        for browser in browsers:
            availability[browser] = self._check_browser_installed(browser)

        return availability

    def _get_system_resources(self) -> Dict[str, Any]:
        """Get system resource information"""
        try:
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)

            return {
                'memory_total_gb': round(memory.total / (1024**3), 1),
                'memory_available_gb': round(memory.available / (1024**3), 1),
                'memory_percent': memory.percent,
                'cpu_percent': cpu_percent
            }
        except Exception as e:
            logger.error(f"Error getting system resources: {e}")
            return {'error': str(e)}

    def install_browser(self, browser_type: str) -> bool:
        """Attempt to install missing browser"""
        try:
            if self._check_browser_installed(browser_type):
                self._update_status(f"✅ {browser_type} is already installed", "info")
                return True

            self._update_status(f"📦 Installing {browser_type}...", "info")

            # Installation commands for different systems
            install_commands = {
                'chrome': {
                    'linux': 'sudo apt update && sudo apt install -y google-chrome-stable',
                    'windows': 'winget install Google.Chrome',
                    'darwin': 'brew install google-chrome'
                },
                'firefox': {
                    'linux': 'sudo apt update && sudo apt install -y firefox',
                    'windows': 'winget install Mozilla.Firefox',
                    'darwin': 'brew install firefox'
                },
                'edge': {
                    'linux': 'curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list && apt update && apt install -y microsoft-edge-stable',
                    'windows': 'winget install Microsoft.Edge',
                    'darwin': 'brew install microsoft-edge'
                },
                'brave': {
                    'linux': 'sudo apt install -y curl && curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg && echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg arch=amd64] https://brave-browser-apt-release.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser-release.list && sudo apt update && sudo apt install -y brave-browser',
                    'windows': 'winget install Brave.Brave',
                    'darwin': 'brew install brave-browser'
                }
            }

            import platform
            system = platform.system().lower()

            if browser_type in install_commands and system in install_commands[browser_type]:
                command = install_commands[browser_type][system]

                result = subprocess.run(command, shell=True, capture_output=True, text=True)

                if result.returncode == 0:
                    self._update_status(f"✅ {browser_type} installed successfully", "success")
                    return True
                else:
                    self._update_status(f"❌ Installation failed: {result.stderr}", "error")
                    return False
            else:
                self._update_status(f"❌ Unsupported system ({system}) for {browser_type}", "error")
                return False

        except Exception as e:
            self._update_status(f"❌ Error installing browser: {e}", "error")
            return False

    def __del__(self):
        """Cleanup all sessions when object is destroyed"""
        try:
            self.terminate_all_sessions()
        except:
            pass
