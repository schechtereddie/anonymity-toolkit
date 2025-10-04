# cookie_manager.py
import json
import random
import time
from fake_useragent import UserAgent
from http.cookies import SimpleCookie
import requests

class CookieManager:
    def __init__(self):
        self.ua = UserAgent()
        self.cookies_jar = {}

    def generate_user_agent(self, browser_type=None):
        """Generate random user agent"""
        if browser_type == 'chrome':
            return self.ua.chrome
        elif browser_type == 'firefox':
            return self.ua.firefox
        elif browser_type == 'safari':
            return self.ua.safari
        else:
            return self.ua.random

    def create_cookies(self, domain, count=1):
        """Create realistic cookies for a domain"""
        cookies_list = []

        for _ in range(count):
            cookies = {
                'session_id': self._generate_random_string(32),
                'user_id': str(random.randint(100000, 999999)),
                'csrf_token': self._generate_random_string(16),
                'last_visit': str(int(time.time())),
                'preferences': self._generate_random_string(8)
            }

            self.cookies_jar[domain] = cookies
            cookies_list.append(cookies)

        return cookies_list

    def _generate_random_string(self, length):
        """Generate random string for cookie values"""
        import string
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def export_cookies(self, filename):
        """Export cookies to file"""
        with open(filename, 'w') as f:
            json.dump(self.cookies_jar, f, indent=2)

    def import_cookies(self, filename):
        """Import cookies from file"""
        with open(filename, 'r') as f:
            self.cookies_jar = json.load(f)

    def get_cookies_for_domain(self, domain):
        """Get cookies for specific domain"""
        return self.cookies_jar.get(domain, {})
