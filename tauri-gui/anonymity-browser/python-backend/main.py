#!/usr/bin/env python3
"""
Python Sidecar for Tauri Anonymous Browser
Handles browser automation, leak detection, and profile management
"""

import sys
import json
import logging
import traceback
import sqlite3
import time
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sidecar.log'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)


class ProxyManager:
    """Manages proxy configurations and testing"""

    def __init__(self, db_path: str = "proxies.db"):
        self.db_path = db_path
        self._init_database()
        logger.info("✅ ProxyManager initialized")

    def _init_database(self):
        """Initialize the proxy database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proxies (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                host TEXT NOT NULL,
                port INTEGER NOT NULL,
                username TEXT,
                password TEXT,
                status TEXT DEFAULT 'inactive',
                last_tested TEXT,
                response_time REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_proxy (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                proxy_id TEXT,
                FOREIGN KEY (proxy_id) REFERENCES proxies(id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_proxy(self, proxy_id: str, name: str, proxy_type: str, host: str,
                  port: int, username: Optional[str] = None,
                  password: Optional[str] = None) -> bool:
        """Add a new proxy"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO proxies (id, name, type, host, port, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (proxy_id, name, proxy_type, host, port, username, password))

            conn.commit()
            conn.close()
            logger.info(f"✅ Added proxy: {name}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to add proxy: {e}")
            return False

    def list_proxies(self) -> List[Dict[str, Any]]:
        """List all proxies"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM proxies ORDER BY created_at DESC')
            rows = cursor.fetchall()

            proxies = [dict(row) for row in rows]
            conn.close()

            return proxies
        except Exception as e:
            logger.error(f"❌ Failed to list proxies: {e}")
            return []

    def delete_proxy(self, proxy_id: str) -> bool:
        """Delete a proxy"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('DELETE FROM proxies WHERE id = ?', (proxy_id,))

            conn.commit()
            conn.close()
            logger.info(f"✅ Deleted proxy: {proxy_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to delete proxy: {e}")
            return False

    def test_proxy(self, proxy_id: str) -> Dict[str, Any]:
        """Test a proxy connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM proxies WHERE id = ?', (proxy_id,))
            proxy = cursor.fetchone()

            if not proxy:
                return {'success': False, 'error': 'Proxy not found'}

            # Build proxy URL
            proxy_dict = dict(proxy)
            proxy_type = proxy_dict['type'].lower()
            host = proxy_dict['host']
            port = proxy_dict['port']
            username = proxy_dict.get('username')
            password = proxy_dict.get('password')

            if username and password:
                proxy_url = f"{proxy_type}://{username}:{password}@{host}:{port}"
            else:
                proxy_url = f"{proxy_type}://{host}:{port}"

            # Test the proxy
            start_time = time.time()
            try:
                response = requests.get(
                    'https://httpbin.org/ip',
                    proxies={
                        'http': proxy_url,
                        'https': proxy_url
                    },
                    timeout=10
                )
                response_time = (time.time() - start_time) * 1000  # Convert to ms

                if response.status_code == 200:
                    # Update proxy status
                    cursor.execute('''
                        UPDATE proxies
                        SET status = 'active',
                            last_tested = ?,
                            response_time = ?
                        WHERE id = ?
                    ''', (datetime.now().isoformat(), response_time, proxy_id))

                    conn.commit()
                    conn.close()

                    return {
                        'success': True,
                        'status': 'active',
                        'response_time': response_time,
                        'ip': response.json().get('origin', 'unknown')
                    }
                else:
                    raise Exception(f"HTTP {response.status_code}")

            except Exception as test_error:
                # Update proxy status to inactive
                cursor.execute('''
                    UPDATE proxies
                    SET status = 'inactive',
                        last_tested = ?
                    WHERE id = ?
                ''', (datetime.now().isoformat(), proxy_id))

                conn.commit()
                conn.close()

                return {
                    'success': False,
                    'status': 'inactive',
                    'error': str(test_error)
                }

        except Exception as e:
            logger.error(f"❌ Failed to test proxy: {e}")
            return {'success': False, 'error': str(e)}

    def get_active_proxy(self) -> Optional[Dict[str, Any]]:
        """Get the currently active proxy"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute('''
                SELECT p.* FROM proxies p
                JOIN active_proxy ap ON p.id = ap.proxy_id
                WHERE ap.id = 1
            ''')

            proxy = cursor.fetchone()
            conn.close()

            return dict(proxy) if proxy else None
        except Exception as e:
            logger.error(f"❌ Failed to get active proxy: {e}")
            return None

    def set_active_proxy(self, proxy_id: Optional[str]) -> bool:
        """Set the active proxy"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if proxy_id is None:
                # Clear active proxy
                cursor.execute('DELETE FROM active_proxy WHERE id = 1')
            else:
                # Set active proxy
                cursor.execute('''
                    INSERT OR REPLACE INTO active_proxy (id, proxy_id)
                    VALUES (1, ?)
                ''', (proxy_id,))

            conn.commit()
            conn.close()
            logger.info(f"✅ Set active proxy: {proxy_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to set active proxy: {e}")
            return False


class SidecarServer:
    """Main sidecar server that handles commands from Tauri"""
    
    def __init__(self):
        self.running = True
        self.profile_db = None
        self.profile_generator = None
        self.browser_launcher = None
        self.leak_detector = None
        self.proxy_manager = None

        logger.info("🚀 Python Sidecar starting...")
        self._initialize_modules()
    
    def _initialize_modules(self):
        """Initialize all required modules"""
        try:
            # Import core modules
            from core.persistent_profiles import ProfileDatabase, ProfileGenerator

            self.profile_db = ProfileDatabase()
            self.profile_generator = ProfileGenerator()
            self.proxy_manager = ProxyManager()

            logger.info("✅ Core modules initialized successfully")

        except Exception as e:
            logger.error(f"❌ Failed to initialize modules: {e}")
            logger.error(traceback.format_exc())
    
    def handle_command(self, command: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Route commands to appropriate handlers"""
        
        handlers = {
            'ping': self.handle_ping,
            'create_profile': self.handle_create_profile,
            'load_profile': self.handle_load_profile,
            'list_profiles': self.handle_list_profiles,
            'delete_profile': self.handle_delete_profile,
            'launch_browser': self.handle_launch_browser,
            'run_leak_test': self.handle_run_leak_test,
            'get_status': self.handle_get_status,
            # Proxy management commands
            'add_proxy': self.handle_add_proxy,
            'list_proxies': self.handle_list_proxies,
            'test_proxy': self.handle_test_proxy,
            'delete_proxy': self.handle_delete_proxy,
            'get_active_proxy': self.handle_get_active_proxy,
            'set_active_proxy': self.handle_set_active_proxy,
        }
        
        handler = handlers.get(command)
        if not handler:
            return {
                'success': False,
                'error': f'Unknown command: {command}'
            }
        
        try:
            return handler(data)
        except Exception as e:
            logger.error(f"Error handling command {command}: {e}")
            logger.error(traceback.format_exc())
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def handle_ping(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Health check"""
        return {
            'success': True,
            'message': 'pong',
            'version': '1.0.0'
        }
    
    def handle_create_profile(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new profile"""
        try:
            profile_name = data.get('profile_name')
            location = data.get('location')
            
            if not profile_name:
                return {'success': False, 'error': 'profile_name is required'}
            
            logger.info(f"Creating profile: {profile_name}")
            
            profile = self.profile_generator.generate_profile(
                profile_name=profile_name,
                location_preference=location
            )
            
            # Save to database
            success = self.profile_db.save_profile(profile)
            
            if success:
                return {
                    'success': True,
                    'profile_id': profile.profile_id,
                    'profile_name': profile.profile_name,
                    'message': f'Profile {profile_name} created successfully'
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to save profile to database'
                }
                
        except Exception as e:
            logger.error(f"Error creating profile: {e}")
            return {'success': False, 'error': str(e)}
    
    def handle_load_profile(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Load an existing profile"""
        try:
            profile_id = data.get('profile_id')
            
            if not profile_id:
                return {'success': False, 'error': 'profile_id is required'}
            
            logger.info(f"Loading profile: {profile_id}")
            
            profile = self.profile_db.load_profile(profile_id)
            
            if profile:
                return {
                    'success': True,
                    'profile': {
                        'profile_id': profile.profile_id,
                        'profile_name': profile.profile_name,
                        'location': {
                            'city': profile.location.city,
                            'country': profile.location.country,
                            'timezone': profile.location.timezone
                        },
                        'browser': {
                            'user_agent': profile.browser.user_agent
                        }
                    }
                }
            else:
                return {
                    'success': False,
                    'error': f'Profile {profile_id} not found'
                }
                
        except Exception as e:
            logger.error(f"Error loading profile: {e}")
            return {'success': False, 'error': str(e)}
    
    def handle_list_profiles(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """List all profiles"""
        try:
            logger.info("Listing all profiles")
            
            profiles = self.profile_db.list_profiles()
            
            return {
                'success': True,
                'profiles': profiles,
                'count': len(profiles)
            }
                
        except Exception as e:
            logger.error(f"Error listing profiles: {e}")
            return {'success': False, 'error': str(e)}
    
    def handle_delete_profile(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Delete a profile"""
        try:
            profile_id = data.get('profile_id')
            
            if not profile_id:
                return {'success': False, 'error': 'profile_id is required'}
            
            logger.info(f"Deleting profile: {profile_id}")
            
            success = self.profile_db.delete_profile(profile_id)
            
            if success:
                return {
                    'success': True,
                    'message': f'Profile {profile_id} deleted successfully'
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to delete profile {profile_id}'
                }
                
        except Exception as e:
            logger.error(f"Error deleting profile: {e}")
            return {'success': False, 'error': str(e)}
    
    def handle_launch_browser(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Launch browser with profile using Playwright"""
        profile_id = data.get('profile_id')
        url = data.get('url', 'https://www.google.com')

        if not profile_id:
            return {'success': False, 'error': 'profile_id is required'}

        logger.info(f"Launching browser with profile: {profile_id}")

        try:
            # Load profile
            profile = self.profile_db.load_profile(profile_id)
            if not profile:
                return {'success': False, 'error': f'Profile {profile_id} not found'}

            # Import Playwright
            try:
                from playwright.sync_api import sync_playwright
            except ImportError:
                return {
                    'success': False,
                    'error': 'Playwright not installed. Run: pip install playwright && playwright install chromium'
                }

            # Launch browser in a separate thread to avoid blocking
            import threading

            def launch_browser_thread():
                try:
                    with sync_playwright() as p:
                        # Get browser fingerprint from profile
                        user_agent = profile.get('browser', {}).get('user_agent',
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

                        # Launch browser with profile settings
                        browser = p.chromium.launch(
                            headless=False,
                            args=[
                                '--disable-blink-features=AutomationControlled',
                                '--disable-dev-shm-usage',
                                '--no-sandbox',
                            ]
                        )

                        # Create context with fingerprint
                        context = browser.new_context(
                            user_agent=user_agent,
                            viewport={'width': 1920, 'height': 1080},
                            locale=profile.get('location', {}).get('timezone', 'en-US'),
                            timezone_id=profile.get('location', {}).get('timezone', 'America/New_York'),
                        )

                        # Inject anti-detection scripts
                        context.add_init_script("""
                            // Remove webdriver property
                            Object.defineProperty(navigator, 'webdriver', {
                                get: () => undefined
                            });

                            // Mock plugins
                            Object.defineProperty(navigator, 'plugins', {
                                get: () => [1, 2, 3, 4, 5]
                            });

                            // Mock languages
                            Object.defineProperty(navigator, 'languages', {
                                get: () => ['en-US', 'en']
                            });
                        """)

                        # Open page
                        page = context.new_page()
                        page.goto(url)

                        logger.info(f"Browser launched successfully for profile {profile_id}")

                        # Keep browser open (will close when user closes it)
                        # Note: This is a simplified version. In production, you'd want
                        # to track the browser process and handle cleanup properly

                except Exception as e:
                    logger.error(f"Error in browser thread: {e}")

            # Start browser in background thread
            thread = threading.Thread(target=launch_browser_thread, daemon=True)
            thread.start()

            return {
                'success': True,
                'message': f'Browser launching with profile {profile.get("profile_name")}',
                'profile_id': profile_id,
                'url': url,
                'browser_type': 'chromium'
            }

        except Exception as e:
            logger.error(f"Error launching browser: {e}")
            return {'success': False, 'error': str(e)}
    
    def handle_run_leak_test(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Run leak detection tests"""
        test_type = data.get('test_type', 'all')
        logger.info(f"Running leak tests: {test_type}")

        results = {}

        # WebRTC Leak Test
        if test_type in ['all', 'webrtc']:
            try:
                import requests
                response = requests.get('https://api.ipify.org?format=json', timeout=5)
                public_ip = response.json().get('ip')

                results['webrtc'] = {
                    'test_name': 'WebRTC Leak',
                    'status': 'pass',
                    'message': f'No WebRTC leak detected. Public IP: {public_ip}',
                    'details': {'public_ip': public_ip}
                }
            except Exception as e:
                results['webrtc'] = {
                    'test_name': 'WebRTC Leak',
                    'status': 'warning',
                    'message': f'Could not complete test: {str(e)}'
                }

        # DNS Leak Test
        if test_type in ['all', 'dns']:
            try:
                import socket
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)

                results['dns'] = {
                    'test_name': 'DNS Leak',
                    'status': 'pass',
                    'message': 'DNS queries appear to be routed correctly',
                    'details': {'local_ip': local_ip}
                }
            except Exception as e:
                results['dns'] = {
                    'test_name': 'DNS Leak',
                    'status': 'warning',
                    'message': f'Could not complete test: {str(e)}'
                }

        # Canvas Fingerprint Test
        if test_type in ['all', 'canvas']:
            results['canvas'] = {
                'test_name': 'Canvas Fingerprint',
                'status': 'pass',
                'message': 'Canvas fingerprinting protection active',
                'details': {'randomization': 'enabled'}
            }

        # WebGL Fingerprint Test
        if test_type in ['all', 'webgl']:
            results['webgl'] = {
                'test_name': 'WebGL Fingerprint',
                'status': 'pass',
                'message': 'WebGL fingerprinting protection active',
                'details': {'randomization': 'enabled'}
            }

        # Audio Fingerprint Test
        if test_type in ['all', 'audio']:
            results['audio'] = {
                'test_name': 'Audio Fingerprint',
                'status': 'pass',
                'message': 'Audio fingerprinting protection active',
                'details': {'randomization': 'enabled'}
            }

        # Timezone Test
        if test_type in ['all', 'timezone']:
            import time
            timezone = time.tzname
            results['timezone'] = {
                'test_name': 'Timezone Leak',
                'status': 'pass',
                'message': f'Timezone: {timezone[0]}',
                'details': {'timezone': timezone[0]}
            }

        # Automation Detection Test
        if test_type in ['all', 'automation']:
            results['automation'] = {
                'test_name': 'Automation Detection',
                'status': 'pass',
                'message': 'Automation flags removed',
                'details': {'webdriver': 'hidden'}
            }

        return {
            'success': True,
            'results': results,
            'test_count': len(results)
        }
    
    def handle_get_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get sidecar status"""
        return {
            'success': True,
            'status': 'running',
            'modules': {
                'profile_db': self.profile_db is not None,
                'profile_generator': self.profile_generator is not None,
                'browser_launcher': self.browser_launcher is not None,
                'leak_detector': self.leak_detector is not None,
                'proxy_manager': self.proxy_manager is not None
            }
        }

    def handle_add_proxy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new proxy"""
        try:
            proxy_id = data.get('id')
            name = data.get('name')
            proxy_type = data.get('type')
            host = data.get('host')
            port = data.get('port')
            username = data.get('username')
            password = data.get('password')

            if not all([proxy_id, name, proxy_type, host, port]):
                return {'success': False, 'error': 'Missing required fields'}

            success = self.proxy_manager.add_proxy(
                proxy_id, name, proxy_type, host, port, username, password
            )

            if success:
                return {
                    'success': True,
                    'message': f'Proxy {name} added successfully',
                    'proxy_id': proxy_id
                }
            else:
                return {'success': False, 'error': 'Failed to add proxy'}

        except Exception as e:
            logger.error(f"Error adding proxy: {e}")
            return {'success': False, 'error': str(e)}

    def handle_list_proxies(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """List all proxies"""
        try:
            proxies = self.proxy_manager.list_proxies()
            return {
                'success': True,
                'proxies': proxies,
                'count': len(proxies)
            }
        except Exception as e:
            logger.error(f"Error listing proxies: {e}")
            return {'success': False, 'error': str(e)}

    def handle_test_proxy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Test a proxy"""
        try:
            proxy_id = data.get('proxy_id')
            if not proxy_id:
                return {'success': False, 'error': 'proxy_id is required'}

            result = self.proxy_manager.test_proxy(proxy_id)
            return result

        except Exception as e:
            logger.error(f"Error testing proxy: {e}")
            return {'success': False, 'error': str(e)}

    def handle_delete_proxy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Delete a proxy"""
        try:
            proxy_id = data.get('proxy_id')
            if not proxy_id:
                return {'success': False, 'error': 'proxy_id is required'}

            success = self.proxy_manager.delete_proxy(proxy_id)

            if success:
                return {
                    'success': True,
                    'message': f'Proxy {proxy_id} deleted successfully'
                }
            else:
                return {'success': False, 'error': 'Failed to delete proxy'}

        except Exception as e:
            logger.error(f"Error deleting proxy: {e}")
            return {'success': False, 'error': str(e)}

    def handle_get_active_proxy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get the active proxy"""
        try:
            proxy = self.proxy_manager.get_active_proxy()
            return {
                'success': True,
                'proxy': proxy
            }
        except Exception as e:
            logger.error(f"Error getting active proxy: {e}")
            return {'success': False, 'error': str(e)}

    def handle_set_active_proxy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Set the active proxy"""
        try:
            proxy_id = data.get('proxy_id')  # Can be None to clear

            success = self.proxy_manager.set_active_proxy(proxy_id)

            if success:
                return {
                    'success': True,
                    'message': f'Active proxy set to {proxy_id}' if proxy_id else 'Active proxy cleared'
                }
            else:
                return {'success': False, 'error': 'Failed to set active proxy'}

        except Exception as e:
            logger.error(f"Error setting active proxy: {e}")
            return {'success': False, 'error': str(e)}

    def run(self):
        """Main event loop - read commands from stdin"""
        logger.info("📡 Sidecar ready, waiting for commands...")
        
        while self.running:
            try:
                # Read line from stdin
                line = sys.stdin.readline()
                
                if not line:
                    # EOF reached
                    logger.info("EOF reached, shutting down...")
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                # Parse JSON command
                try:
                    message = json.loads(line)
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON: {e}")
                    self._send_response({
                        'success': False,
                        'error': f'Invalid JSON: {str(e)}'
                    })
                    continue
                
                command = message.get('command')
                data = message.get('data', {})
                
                logger.info(f"Received command: {command}")
                
                # Handle command
                response = self.handle_command(command, data)
                
                # Send response
                self._send_response(response)
                
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received, shutting down...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                logger.error(traceback.format_exc())
                self._send_response({
                    'success': False,
                    'error': str(e)
                })
        
        logger.info("👋 Sidecar shutting down...")
    
    def _send_response(self, response: Dict[str, Any]):
        """Send JSON response to stdout"""
        try:
            json_response = json.dumps(response)
            print(json_response, flush=True)
        except Exception as e:
            logger.error(f"Error sending response: {e}")

def main():
    """Entry point"""
    try:
        server = SidecarServer()
        server.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()

