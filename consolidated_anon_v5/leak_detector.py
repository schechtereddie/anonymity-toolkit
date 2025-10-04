# leak_detector.py
import requests
import threading
import time
from typing import Dict, List

class LeakDetector:
    def __init__(self):
        self.test_urls = [
            'http://httpbin.org/ip',
            'http://httpbin.org/user-agent',
            'http://httpbin.org/headers'
        ]
        self.is_monitoring = False
        self.leaks_detected = []

    def start_leak_protection(self, proxy_config, expected_ip=None):
        """Start monitoring for IP leaks"""
        self.is_monitoring = True
        self.leaks_detected = []

        def monitor():
            while self.is_monitoring:
                self._check_for_leaks(proxy_config, expected_ip)
                time.sleep(30)  # Check every 30 seconds

        thread = threading.Thread(target=monitor)
        thread.daemon = True
        thread.start()

    def stop_leak_protection(self):
        """Stop leak monitoring"""
        self.is_monitoring = False

    def _check_for_leaks(self, proxy_config, expected_ip):
        """Check if real IP is leaking"""
        try:
            session = requests.Session()

            # Configure session with proxy
            if proxy_config:
                session.proxies.update(proxy_config)

            for test_url in self.test_urls:
                response = session.get(test_url, timeout=10)

                if test_url.endswith('/ip'):
                    current_ip = response.json().get('origin', '')
                    if expected_ip and expected_ip not in current_ip:
                        leak_info = {
                            'type': 'IP Leak',
                            'expected': expected_ip,
                            'actual': current_ip,
                            'url': test_url,
                            'timestamp': time.time()
                        }
                        self.leaks_detected.append(leak_info)

                elif test_url.endswith('/user-agent'):
                    # Check for consistent user agent
                    pass

        except Exception as e:
            print(f"Leak check error: {e}")

    def get_leaks(self):
        """Get detected leaks"""
        return self.leaks_detected

    def test_browser_fingerprinting(self, session):
        """Test for browser fingerprinting leaks"""
        # Implement basic fingerprinting tests
        tests = {
            'webgl': self._test_webgl,
            'canvas': self._test_canvas_fingerprinting,
            'timezone': self._test_timezone,
            'screen_resolution': self._test_screen_resolution
        }

        results = {}
        for test_name, test_func in tests.items():
            try:
                results[test_name] = test_func(session)
            except:
                results[test_name] = 'Failed'

        return results

    def _test_webgl(self, session):
        """Test for WebGL fingerprinting"""
        # This requires browser automation to get the WebGL vendor and renderer.
        # For now, we can check for the presence of certain headers.
        try:
            response = session.get('https://browserleaks.com/webgl', timeout=10)
            if "WebGL Vendor" in response.text and "WebGL Renderer" in response.text:
                return "Potentially vulnerable"
            else:
                return "Likely not vulnerable"
        except Exception:
            return "Could not test"

    def _test_canvas_fingerprinting(self, session):
        """Test for Canvas fingerprinting"""
        # This requires browser automation to generate a canvas image and get its hash.
        return "Browser automation required for full test"

    def _test_timezone(self, session):
        """Test for timezone leakage"""
        try:
            response = session.get('http://worldtimeapi.org/api/ip', timeout=10)
            if response.status_code == 200:
                return response.json().get('timezone', 'Unknown')
            else:
                return "Could not test"
        except Exception:
            return "Could not test"

    def _test_screen_resolution(self, session):
        """Test for screen resolution leakage"""
        # This requires browser automation to get the screen resolution.
        return "Browser automation required for full test"
