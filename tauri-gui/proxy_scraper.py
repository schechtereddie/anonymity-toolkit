# proxy_scraper.py - Ultra-Advanced Proxy Scraper
# Combines threading, verification, async, and MaxMind geo capabilities

import requests
from bs4 import BeautifulSoup
import re
import threading
import asyncio
import aiohttp
from queue import Queue
import time
import os
import logging
import maxminddb
from concurrent.futures import ThreadPoolExecutor
import random
from typing import List, Dict, Optional, Any, Tuple, Union, cast

class AdvancedProxyScraper:
    def __init__(self):
        # Primary SOCKS5 sources
        self.sources = [
            'https://www.socks-proxy.net/',
            'https://www.proxy-list.download/SOCKS5',
            'https://spys.one/en/socks-proxy-list/',
            'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
            'https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&ssl=all',
            'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks5&anonymityLevel=elite',
            'https://free-proxy-list.net/socks-proxy.html',
            'https://www.freeproxylists.net/?c=5&pt=2',  # SOCKS5 only
            'https://proxy-list.download/api/v1/get?type=socks5',
            'https://www.proxy-daily.com/api/getproxylist?apikey=free&format=json&type=socks5',
            'https://hidemyass.com/proxy-list/',
            'https://www.vpnbook.com/free-proxy-list/',
        ]

        # Additional HTTP sources (convertible to SOCKS5)
        self.http_sources = [
            'https://www.free-proxy-list.net/',
            'https://www.us-proxy.org/',
            'https://free-proxy-list.net/',
            'https://www.sslproxies.org/',
            'https://www.proxynova.com/proxy-server-list/',
            'https://www.my-proxy.com/free-proxy-list.html',
            'https://proxy-list.org/english/index.php',
            'https://www.xroxy.com/proxylist.php',
        ]

        # Geographic targeting sources by region with detailed US breakdown
        self.geographic_sources = {
            # Detailed US regional breakdown
            'united_states': [
                # SOCKS5 specific sources
                'https://www.socks-proxy.net/',
                'https://www.proxy-list.download/SOCKS5',
                'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
                'https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&ssl=all',
                # US-specific sources
                'https://www.us-proxy.org/',
                'https://www.proxy-list.download/SOCKS5?country=US',
                'https://www.proxy-list.download/HTTP?country=US',
                'https://www.proxynova.com/proxy-server-list/country-us/',
                'https://free-proxy-list.net/us-proxy.html',
                'https://hidemyass.com/proxy-list/',
                'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&country=US&protocols=socks5'
            ],
            # US Regional subdivisions
            'us_east': [
                'https://www.proxy-list.download/SOCKS5?country=US',
                'https://www.us-proxy.org/regions/east',
                'https://free-proxy-list.net/us-proxy.html?region=east'
            ],
            'us_west': [
                'https://www.proxy-list.download/SOCKS5?country=US',
                'https://www.us-proxy.org/regions/west',
                'https://free-proxy-list.net/us-proxy.html?region=west'
            ],
            'us_south': [
                'https://www.proxy-list.download/SOCKS5?country=US',
                'https://www.us-proxy.org/regions/south',
                'https://free-proxy-list.net/us-proxy.html?region=south'
            ],
            'us_midwest': [
                'https://www.proxy-list.download/SOCKS5?country=US',
                'https://www.us-proxy.org/regions/midwest',
                'https://free-proxy-list.net/us-proxy.html?region=midwest'
            ],
            'europe': [
                'https://www.proxy-list.download/HTTP?country=DE',
                'https://www.proxy-list.download/HTTP?country=UK',
                'https://www.proxy-list.download/HTTP?country=FR',
                'https://www.proxynova.com/proxy-server-list/country-de/',
                'https://www.proxynova.com/proxy-server-list/country-uk/'
            ],
            'asia': [
                'https://www.proxy-list.download/HTTP?country=JP',
                'https://www.proxy-list.download/HTTP?country=KR',
                'https://www.proxy-list.download/HTTP?country=SG',
                'https://www.proxynova.com/proxy-server-list/country-jp/',
                'https://www.proxynova.com/proxy-server-list/country-kr/'
            ],
            'south_america': [
                'https://www.proxy-list.download/HTTP?country=BR',
                'https://www.proxynova.com/proxy-server-list/country-br/',
                'https://free-proxy-list.net/',
                'https://www.sslproxies.org/'
            ],
            'russia': [
                'https://www.proxy-list.download/HTTP?country=RU',
                'https://www.proxynova.com/proxy-server-list/country-ru/',
                'https://free-proxy-list.net/russian-proxy.html'
            ],
            'india': [
                'https://www.proxy-list.download/HTTP?country=IN',
                'https://www.proxynova.com/proxy-server-list/country-in/',
                'https://free-proxy-list.net/india-proxy.html'
            ],
            'china': [
                'https://www.proxy-list.download/HTTP?country=CN',
                'https://www.proxynova.com/proxy-server-list/country-cn/'
            ],
            'east_europe': [
                'https://www.proxy-list.download/HTTP?country=PL',
                'https://www.proxy-list.download/HTTP?country=CZ',
                'https://www.proxy-list.download/HTTP?country=HU',
                'https://free-proxy-list.net/anonymity.html'
            ],
            'middle_east': [
                'https://www.proxy-list.download/HTTP?country=IL',
                'https://www.proxy-list.download/HTTP?country=SA',
                'https://www.proxy-list.download/HTTP?country=TR',
                'https://free-proxy-list.net/anonymous-proxy.html'
            ]
        }

        # Country code mappings for easy targeting
        self.country_mappings = {
            # North America
            'US': 'united_states', 'CA': 'north_america', 'MX': 'south_america',
            # Europe
            'GB': 'europe', 'UK': 'europe', 'DE': 'europe', 'FR': 'europe', 'IT': 'europe', 'ES': 'europe',
            'PL': 'east_europe', 'CZ': 'east_europe', 'HU': 'east_europe', 'RO': 'east_europe',
            'RU': 'russia', 'UA': 'russia',
            # Asia
            'JP': 'asia', 'KR': 'asia', 'CN': 'china', 'SG': 'asia', 'TH': 'asia',
            'IN': 'india', 'PK': 'asia', 'BD': 'asia', 'VN': 'asia', 'MY': 'asia',
            # South America
            'BR': 'south_america', 'AR': 'south_america', 'CO': 'south_america', 'CL': 'south_america',
            'PE': 'south_america', 'VE': 'south_america',
            # Middle East & Africa
            'IL': 'middle_east', 'SA': 'middle_east', 'TR': 'middle_east', 'AE': 'middle_east',
            'EG': 'africa', 'ZA': 'africa', 'NG': 'africa', 'KE': 'africa',
            # Oceania
            'AU': 'oceania', 'NZ': 'oceania'
        }

        # Continent groupings for targeting
        self.continent_mappings = {
            'north_america': ['US', 'CA', 'MX', 'TT', 'JM'],
            'south_america': ['BR', 'AR', 'CO', 'CL', 'PE', 'VE', 'UY', 'PY'],
            'europe': ['GB', 'DE', 'FR', 'IT', 'ES', 'PT', 'NL', 'BE', 'AT', 'SE', 'NO', 'DK', 'FI'],
            'east_europe': ['PL', 'CZ', 'HU', 'RO', 'BG', 'HR', 'SI', 'SK', 'MD'],
            'asia': ['JP', 'KR', 'SG', 'TH', 'PH', 'ID', 'MY', 'VN', 'LK', 'PK', 'BD'],
            'china': ['CN', 'HK', 'TW'],
            'india': ['IN'],
            'russia': ['RU', 'UA', 'BY', 'KZ', 'UZ'],
            'middle_east': ['IL', 'SA', 'TR', 'AE', 'IR', 'JO', 'LB', 'QA', 'KW', 'OM', 'YE'],
            'africa': ['EG', 'ZA', 'NG', 'KE', 'MA', 'TN', 'GH', 'CI', 'SN', 'AO', 'MZ', 'ZM'],
            'oceania': ['AU', 'NZ', 'FJ', 'PG', 'WS']
        }

        self.proxies = []
        self.verified_proxies = []
        self.failed_proxies = []
        self.geo_cache = {}
        self.maxmind_reader = None

        # Initialize MaxMind DB if available
        self._init_maxmind()

        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        ]

    def _init_maxmind(self):
        """Initialize MaxMind GeoIP database"""
        geo_db_paths = ['GeoLite2-City.mmdb', '../geo/GeoLite2-City.mmdb']
        for db_path in geo_db_paths:
            if os.path.exists(db_path):
                try:
                    self.maxmind_reader = maxminddb.open_database(db_path)
                    break
                except Exception as e:
                    continue

    def get_geo_info_maxmind(self, ip, use_cache=True):
        """Get geo info using MaxMind database"""
        if use_cache and ip in self.geo_cache:
            return self.geo_cache[ip]

        if not self.maxmind_reader:
            # Fallback to API
            return self._get_geo_api(ip)

        try:
            geo = self.maxmind_reader.get(ip) or {}

            # Helper function to safely extract nested dict values
            def safe_get_nested(d, *keys):
                current = d
                for key in keys:
                    if isinstance(current, dict) and key in current:
                        current = current[key]
                    else:
                        return None
                return current

            # Safe extraction using nested dict access
            country = safe_get_nested(geo, 'country', 'names', 'en')
            country = country if isinstance(country, str) and country else 'Unknown'

            country_code = safe_get_nested(geo, 'country', 'iso_code')
            country_code = country_code if isinstance(country_code, str) else 'Unknown'

            city = safe_get_nested(geo, 'city', 'names', 'en')
            city = city if isinstance(city, str) and city else 'Unknown'

            region = 'Unknown'
            if isinstance(geo, dict):
                subdivisions = geo.get('subdivisions')
                if isinstance(subdivisions, list) and len(subdivisions) > 0:
                    region = safe_get_nested(subdivisions[0], 'names', 'en')
                    region = region if isinstance(region, str) and region else 'Unknown'

            lat = safe_get_nested(geo, 'location', 'latitude')
            lat = float(lat) if isinstance(lat, (int, float)) else 0.0

            lon = safe_get_nested(geo, 'location', 'longitude')
            lon = float(lon) if isinstance(lon, (int, float)) else 0.0

            zip_code = safe_get_nested(geo, 'postal', 'code')
            zip_code = zip_code if isinstance(zip_code, str) else 'Unknown'

            isp = safe_get_nested(geo, 'traits', 'isp')
            isp = isp if isinstance(isp, str) and isp else 'Unknown'

            asn_raw = safe_get_nested(geo, 'traits', 'autonomous_system_number')
            asn = f"AS{asn_raw}" if isinstance(asn_raw, (int, str)) else 'Unknown'

            info = {
                'ip': ip,
                'country': country,
                'country_code': country_code,
                'region': region,
                'city': city,
                'zip': zip_code,
                'lat': lat,
                'lon': lon,
                'isp': isp,
                'org': isp,  # ISP and ORG are often the same
                'asn': asn
            }

            self.geo_cache[ip] = info
            return info
        except Exception:
            return self._get_geo_api(ip)

    def _get_geo_api(self, ip):
        """Fallback geo lookup using API"""
        try:
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'ip': ip,
                        'country': data.get('country', 'Unknown'),
                        'country_code': data.get('countryCode', 'Unknown'),
                        'region': data.get('regionName', 'Unknown'),
                        'city': data.get('city', 'Unknown'),
                        'zip': data.get('zip', 'Unknown'),
                        'lat': data.get('lat', 0),
                        'lon': data.get('lon', 0),
                        'isp': data.get('isp', 'Unknown'),
                        'org': data.get('org', 'Unknown'),
                        'asn': data.get('as', 'Unknown')
                    }
        except:
            pass
        return {'ip': ip, 'country': 'Unknown', 'city': 'Unknown'}

    def scrape_proxies(self, max_workers=10):
        """Scrape SOCKS5 proxies using multi-threading"""
        self.proxies = []
        threads = []

        for source in self.sources:
            thread = threading.Thread(target=self._scrape_source, args=(source,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Remove duplicates and validate
        self.proxies = list(set(self.proxies))
        self.proxies = [p for p in self.proxies if self._is_valid_proxy_format(p)]

        return self.proxies

    def scrape_proxies_parallel(self, max_workers=20, include_http=False):
        """
        Scrape proxies using multi-threading for maximum performance
        Args:
            max_workers: Number of concurrent scraping threads
            include_http: Also scrape HTTP sources for potential conversion to SOCKS5
        """
        self.proxies = []

        # Combine sources to scrape
        all_sources = list(self.sources)  # SOCKS5 specific
        if include_http:
            all_sources.extend(self.http_sources)  # Add HTTP sources

        print(f"🔍 Scraping {len(all_sources)} proxy sources with {max_workers} concurrent threads...")

        # Use ThreadPoolExecutor for better performance and resource management
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self._scrape_source_sync, source) for source in all_sources]

            # Collect results as they complete
            proxy_sets = []
            for future in futures:
                try:
                    proxy_set = future.result(timeout=30)  # 30 second timeout per source
                    if proxy_set:
                        proxy_sets.append(proxy_set)
                except Exception as e:
                    print(f"⚠️ Error scraping source: {e}")

        # Flatten results and remove duplicates
        all_proxies = []
        for proxy_set in proxy_sets:
            all_proxies.extend(proxy_set)

        self.proxies = list(set(all_proxies))
        self.proxies = [p for p in self.proxies if self._is_valid_proxy_format(p)]

        print(f"✅ Found {len(self.proxies)} unique proxies from {len(proxy_sets)} sources")
        return self.proxies

    def _scrape_source_sync(self, url):
        """Synchronized version for ThreadPoolExecutor"""
        try:
            headers = {'User-Agent': random.choice(self.user_agents)}
            response = requests.get(url, headers=headers, timeout=15)

            proxies = []

            if response.status_code == 200:
                text = response.text

                # Extract IP:PORT patterns
                ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b:\d+'
                matches = re.findall(ip_pattern, text)

                if matches:
                    # Validate each match
                    for proxy in matches:
                        if self._is_valid_proxy_format(proxy):
                            proxies.append(proxy)

                # Also try BeautifulSoup for HTML sources
                try:
                    soup = BeautifulSoup(text, 'html.parser')
                    text_content = soup.get_text()
                    html_matches = re.findall(ip_pattern, text_content)
                    for proxy in html_matches:
                        if self._is_valid_proxy_format(proxy):
                            proxies.append(proxy)
                except Exception:
                    pass  # BeautifulSoup failed, continue with regex matches

                # Remove duplicates from this source
                proxies = list(set(proxies))

            return proxies

        except Exception as e:
            # Don't print individual errors in batch operations
            return []

    def verify_proxies_parallel(self, max_workers=30, include_geo=True, batch_size=50):
        """
        Verify proxies using multi-threading in batches for optimal performance
        Args:
            max_workers: Number of concurrent verification threads
            include_geo: Include geolocation data
            batch_size: Process proxies in batches to manage memory
        """
        self.verified_proxies = []
        self.failed_proxies = []

        if not self.proxies:
            print("❌ No proxies to verify")
            return []

        total_proxies = len(self.proxies)
        print(f"🔍 Verifying {total_proxies} proxies with {max_workers} concurrent threads...")

        # Process in batches to manage memory and provide progress updates
        batches = [self.proxies[i:i + batch_size] for i in range(0, total_proxies, batch_size)]

        verified_count = 0
        failed_count = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i, batch in enumerate(batches):
                print(f"  📦 Verifying batch {i+1}/{len(batches)} ({len(batch)} proxies)...")

                futures = [executor.submit(self._test_proxy, proxy, include_geo) for proxy in batch]

                # Collect results
                for future in futures:
                    try:
                        result = future.result(timeout=35)  # 35 second timeout per proxy
                        if result and result.get('working'):
                            self.verified_proxies.append(result)
                            verified_count += 1
                        else:
                            failed_count += 1
                            if result:
                                self.failed_proxies.append(result)
                    except Exception as e:
                        failed_count += 1
                        print(f"⚠️ Verification error: {e}")

        print(f"✅ Verification complete: {verified_count} working, {failed_count} failed")
        return self.verified_proxies

    async def scrape_proxies_async(self):
        """Asynchronous proxy scraping for better performance"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in self.sources:
                tasks.append(self._async_scrape_source(session, url))

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if not isinstance(result, Exception) and isinstance(result, list):
                    self.proxies.extend(result)

            # Clean up
            self.proxies = list(set(self.proxies))
            self.proxies = [p for p in self.proxies if self._is_valid_proxy_format(p)]

            return self.proxies

    async def _async_scrape_source(self, session, url):
        """Asynchronous source scraping"""
        try:
            headers = {'User-Agent': random.choice(self.user_agents)}
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    text = await response.text()

                    # Extract IP:PORT patterns
                    proxies = []
                    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b:\d+'
                    matches = re.findall(ip_pattern, text)
                    proxies.extend(matches)

                    # Also try BeautifulSoup for HTML
                    try:
                        soup = BeautifulSoup(text, 'html.parser')
                        text_content = soup.get_text()
                        matches.extend(re.findall(ip_pattern, text_content))
                    except:
                        pass

                    return list(set(matches))
        except:
            pass
        return []

    def _scrape_source(self, url):
        """Traditional threaded scraping"""
        try:
            headers = {'User-Agent': random.choice(self.user_agents)}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract IP:Port patterns
            text = soup.get_text()
            ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b:\d+'
            matches = re.findall(ip_pattern, text)

            for match in matches:
                if self._is_valid_proxy_format(match):
                    self.proxies.append(match)

        except Exception as e:
            pass

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

    def verify_proxies(self, max_workers=20, include_geo=True):
        """Verify proxies with geo information"""
        self.verified_proxies = []
        self.failed_proxies = []

        if not self.proxies:
            return []

        # Use threading for verification
        queue = Queue()

        for proxy in self.proxies:
            queue.put(proxy)

        threads = []
        for _ in range(min(max_workers, len(self.proxies))):
            thread = threading.Thread(target=self._verify_worker, args=(queue, include_geo))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return self.verified_proxies

    async def verify_proxies_async(self, include_geo=True):
        """Asynchronous proxy verification for maximum speed"""
        if not self.proxies:
            return []

        async def verify_single(proxy):
            result = await self._async_test_proxy(proxy, include_geo)
            return result

        tasks = [verify_single(proxy) for proxy in self.proxies]
        results = await asyncio.gather(*tasks)

        self.verified_proxies = [r for r in results if r and r.get('working')]
        self.failed_proxies = [r for r in results if not r or not r.get('working')]

        return self.verified_proxies

    def _verify_worker(self, queue, include_geo):
        """Worker for threaded verification"""
        while not queue.empty():
            proxy = queue.get()
            result = self._test_proxy(proxy, include_geo)
            if result:
                self.verified_proxies.append(result)
            else:
                self.failed_proxies.append({'proxy': proxy, 'error': 'failed'})
            queue.task_done()

    def _test_proxy(self, proxy, include_geo=True):
        """Test proxy and get details"""
        try:
            proxies = {
                'http': f'socks5://{proxy}',
                'https': f'socks5://{proxy}'
            }

            start_time = time.time()
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxies,
                timeout=15,  # Longer timeout for testing
                headers={'User-Agent': random.choice(self.user_agents)}
            )
            rtt = int((time.time() - start_time) * 1000)

            if response.status_code == 200:
                try:
                    data = response.json()
                    # Handle both dict and string responses
                    if isinstance(data, dict):
                        actual_ip = data.get('origin', '').split(',')[0]
                    elif isinstance(data, str):
                        actual_ip = data.strip().split(',')[0]
                    else:
                        actual_ip = str(data).split(',')[0]
                except:
                    # Fallback: extract IP from response text
                    text = response.text
                    import re
                    ip_match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text)
                    actual_ip = ip_match.group(0) if ip_match else 'unknown'

                result = {
                    'proxy': proxy,
                    'working': True,
                    'rtt_ms': rtt,
                    'actual_ip': actual_ip
                }

                if include_geo:
                    geo = self.get_geo_info_maxmind(actual_ip)
                    result.update(geo)

                return result

        except Exception as e:
            return {'proxy': proxy, 'working': False, 'error': str(e)}

        return None

    async def _async_test_proxy(self, proxy, include_geo=True):
        """Async version of proxy testing"""
        try:
            # Create proxy connector - try aiohttp_socks first
            connector = None

            # Try aiohttp_socks ProxyConnector
            try:
                from aiohttp_socks import ProxyConnector as AioSocksConnector
                if hasattr(AioSocksConnector, 'from_url'):
                    connector = AioSocksConnector.from_url(f'socks5://{proxy}')  # type: ignore
            except (ImportError, AttributeError):
                pass

            # Fallback to aiohttp's ProxyConnector if available
            if connector is None:
                try:
                    from aiohttp import ProxyConnector as AioConnector
                    if hasattr(AioConnector, 'from_url'):
                        connector = AioConnector.from_url(f'socks5://{proxy}')  # type: ignore
                except (ImportError, AttributeError):
                    # Final fallback - basic aiohttp ClientSession without connector
                    connector = None

            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=15)) as session:
                start_time = time.time()
                async with session.get('http://httpbin.org/ip') as response:
                    rtt = int((time.time() - start_time) * 1000)

                    if response.status == 200:
                        data = await response.json()
                        actual_ip = data.get('origin', '').split(',')[0]

                        result = {
                            'proxy': proxy,
                            'working': True,
                            'rtt_ms': rtt,
                            'actual_ip': actual_ip
                        }

                        if include_geo:
                            geo = self.get_geo_info_maxmind(actual_ip)
                            result.update(geo)

                        return result

        except Exception as e:
            return {'proxy': proxy, 'working': False, 'error': str(e)}

        return None

    def get_working_count(self):
        """Get count of working proxies"""
        return len([p for p in self.verified_proxies if p.get('working')])

    def get_proxies_by_country(self, country):
        """Filter proxies by country"""
        return [p for p in self.verified_proxies
                if p.get('country', '').lower() == country.lower()]

    def get_fastest_proxies(self, limit=10):
        """Get fastest working proxies"""
        working = [p for p in self.verified_proxies if p.get('working') and p.get('rtt_ms')]
        working.sort(key=lambda x: x.get('rtt_ms', 99999))
        return working[:limit]

    def scrape_proxies_for_region(self, region_name: str, max_proxies: int = 100):
        """Scrape proxies targeted specifically for a geographic region"""
        if region_name not in self.geographic_sources:
            self.proxies = []
            return []

        sources = self.geographic_sources[region_name]
        self.proxies = []

        self.log_status(f"🔍 Scraping proxies for {region_name} region using {len(sources)} specialized sources...")

        # Scrape from region-specific sources
        threads = []
        for source in sources:
            thread = threading.Thread(target=self._scrape_source, args=(source,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Remove duplicates and validate
        self.proxies = list(set(self.proxies))
        self.proxies = [p for p in self.proxies if self._is_valid_proxy_format(p)][:max_proxies]

        self.log_status(f"✅ Found {len(self.proxies)} potential proxies in {region_name} region")
        return self.proxies

    def get_proxies_for_region(self, region_name: str, country_code: Optional[str] = None, city: Optional[str] = None):
        """Get verified proxies specifically from a geographic region"""
        if not self.verified_proxies:
            return []

        if country_code:
            # Get proxies from specific country
            filtered = [p for p in self.verified_proxies
                       if p.get('country_code', '').upper() == country_code.upper()]
        elif city and region_name in self.continent_mappings:
            # Get proxies from specific city within continent
            continent_codes = self.continent_mappings[region_name]
            filtered = [p for p in self.verified_proxies
                       if p.get('country_code', '').upper() in continent_codes
                       and p.get('city', '').lower() == city.lower()]
        else:
            # Get proxies from entire region
            region_codes = self.continent_mappings.get(region_name, [])
            filtered = [p for p in self.verified_proxies
                       if p.get('country_code', '').upper() in region_codes]

        return filtered

    def get_proxies_by_continent(self, continent: str):
        """Get proxies by continent (shortcut method)"""
        return self.get_proxies_for_region(continent)

    def get_best_proxies_for_target(self, target_country: str, max_results: int = 5):
        """
        Get the best proxies for targeting a specific country.
        Uses regional biasing to find optimal exit points.
        """
        if not target_country.upper() in self.country_mappings:
            return []

        # Find optimal source regions for this target
        source_regions = []

        # Add regional neighbors (better for avoiding detection)
        if target_country.upper() in ['US', 'CA', 'MX']:
            source_regions = ['north_america', 'europe']
        elif target_country.upper() in ['GB', 'FR', 'DE', 'IT', 'ES']:
            source_regions = ['europe', 'east_europe']
        elif target_country.upper() in ['JP', 'KR', 'CN']:
            source_regions = ['asia', 'china']
        elif target_country.upper() in ['BR', 'AR', 'CO']:
            source_regions = ['south_america']
        elif target_country.upper() in ['RU', 'UA']:
            source_regions = ['russia', 'east_europe']
        else:
            # General fallback
            target_region = self.country_mappings.get(target_country.upper(), 'europe')
            source_regions = [target_region, 'europe']  # Europe as fallback

        # Get proxies from optimal regions
        candidates = []
        for region in source_regions:
            candidates.extend(self.get_proxies_by_continent(region))

        # Sort by quality metrics
        candidates.sort(key=lambda x: (x.get('rtt_ms', 99999), -len(x.get('city', ''))))

        return candidates[:max_results]

    def get_proxy_stats_by_region(self):
        """Get statistics about proxies grouped by geographic region"""
        stats = {}

        for proxy in self.verified_proxies:
            if not proxy.get('working'):
                continue

            country_code = proxy.get('country_code', 'UNKNOWN')
            region_name = self.country_mappings.get(country_code.upper(), 'unknown')

            if region_name not in stats:
                stats[region_name] = {
                    'count': 0,
                    'countries': set(),
                    'avg_rtt': [],
                    'working_rate': 0
                }

            stats[region_name]['count'] += 1
            stats[region_name]['countries'].add(country_code)

            if proxy.get('rtt_ms'):
                stats[region_name]['avg_rtt'].append(proxy.get('rtt_ms'))

        # Calculate averages and cleanup
        for region, data in stats.items():
            if data['avg_rtt']:
                data['avg_rtt'] = sum(data['avg_rtt']) / len(data['avg_rtt'])
            else:
                data['avg_rtt'] = 0
            data['countries'] = len(data['countries'])

        return stats

    def target_proxies_by_coordinates(self, target_lat: float, target_lon: float, max_distance_km: float = 500):
        """
        Get proxies within a certain distance from target coordinates.
        Useful for geo-targeting specific locations.
        """
        import math

        def haversine_distance(lat1, lon1, lat2, lon2):
            """Calculate distance between two points on Earth"""
            R = 6371  # Earth radius in kilometers

            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)

            a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)

            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = R * c

            return distance

        nearby_proxies = []
        for proxy in self.verified_proxies:
            if not proxy.get('working'):
                continue

            proxy_lat = proxy.get('lat')
            proxy_lon = proxy.get('lon')

            if proxy_lat and proxy_lon:
                try:
                    distance = haversine_distance(target_lat, target_lon, proxy_lat, proxy_lon)
                    if distance <= max_distance_km:
                        proxy_copy = proxy.copy()
                        proxy_copy['distance_km'] = round(distance, 1)
                        nearby_proxies.append(proxy_copy)
                except:
                    continue

        # Sort by distance
        nearby_proxies.sort(key=lambda x: x.get('distance_km', 9999))
        return nearby_proxies

    def log_status(self, message):
        """Helper method for logging status (can be customized)"""
        print(message)
