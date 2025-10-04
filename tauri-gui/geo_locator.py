# geo_locator.py - Advanced Geo Location Component
# Combines MaxMind DB, API fallbacks, and caching

import requests
import os

# Handle optional maxminddb import safely
try:
    import maxminddb
    maxmind_available = True
except ImportError:
    maxminddb = None
    maxmind_available = False

class AdvancedGeoLocator:
    def __init__(self):
        self.maxmind_reader = None
        self.cache = {}
        self._init_maxmind()

    def _init_maxmind(self):
        """Initialize MaxMind database"""
        if not maxmind_available or maxminddb is None:
            return

        # Ensure maxminddb is available for type checker
        assert maxminddb is not None

        # Try multiple possible database paths
        db_paths = ['GeoLite2-City.mmdb', '../geo/GeoLite2-City.mmdb', 'geo/GeoLite2-City.mmdb']
        for db_path in db_paths:
            if os.path.exists(db_path):
                try:
                    self.maxmind_reader = maxminddb.open_database(db_path)
                    break
                except Exception as e:
                    continue

    def get_geo_info(self, ip, use_cache=True):
        """Get comprehensive geo information for IP"""
        if use_cache and ip in self.cache:
            return self.cache[ip]

        # Try MaxMind first
        geo_info = self._get_maxmind_geo(ip)
        if not geo_info or geo_info.get('country') == 'Unknown':
            # Fallback to API
            geo_info = self._get_api_geo(ip)

        # Cache the result
        self.cache[ip] = geo_info
        return geo_info

    def _get_maxmind_geo(self, ip):
        """Get geo info from MaxMind DB"""
        if not self.maxmind_reader:
            return None

        try:
            geo = self.maxmind_reader.get(ip)
            if not geo:
                return None

            return {
                'ip': ip,
                'country': self._safe_get(geo, ['country', 'names', 'en'], 'Unknown'),
                'country_code': self._safe_get(geo, ['country', 'iso_code'], 'Unknown'),
                'region': self._safe_get(geo, ['subdivisions', 0, 'names', 'en'], 'Unknown'),
                'city': self._safe_get(geo, ['city', 'names', 'en'], 'Unknown'),
                'zip': self._safe_get(geo, ['postal', 'code'], 'Unknown'),
                'lat': self._safe_get(geo, ['location', 'latitude'], 0),
                'lon': self._safe_get(geo, ['location', 'longitude'], 0),
                'isp': self._safe_get(geo, ['traits', 'isp'], 'Unknown'),
                'org': self._safe_get(geo, ['traits', 'isp'], 'Unknown'),  # Often same
                'asn': f"AS{self._safe_get(geo, ['traits', 'autonomous_system_number'], 'Unknown')}"
            }
        except Exception:
            return None

    def _safe_get(self, obj, path, default):
        """Safely navigate nested dictionaries/lists"""
        try:
            for key in path:
                if isinstance(key, int) and isinstance(obj, list) and 0 <= key < len(obj):
                    obj = obj[key]
                elif isinstance(obj, dict):
                    obj = obj.get(key, default)
                else:
                    return default
            return obj
        except:
            return default

    def _get_api_geo(self, ip):
        """Fallback to free API"""
        services = [
            ('http://ip-api.com/json/', lambda d: d),
            ('http://api.ipstack.com/', lambda d: {
                'success': True,  # Assume success
                'country': d.get('country_name'),
                'countryCode': d.get('country_code'),
                'regionName': d.get('region_name'),
                'city': d.get('city'),
                'zip': d.get('zip'),
                'lat': d.get('latitude'),
                'lon': d.get('longitude')
            })
        ]

        for service_url, transformer in services:
            try:
                response = requests.get(f"{service_url}{ip}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if transformer:
                        data = transformer(data)

                    if data.get('status') == 'success' or data.get('country'):
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
            except Exception:
                continue

        return {
            'ip': ip,
            'country': 'Unknown',
            'country_code': 'Unknown',
            'region': 'Unknown',
            'city': 'Unknown',
            'zip': 'Unknown',
            'lat': 0,
            'lon': 0,
            'isp': 'Unknown',
            'org': 'Unknown',
            'asn': 'Unknown'
        }

    def get_current_ip(self):
        """Get current public IP"""
        services = [
            'http://httpbin.org/ip',
            'http://icanhazip.com',
            'http://ipinfo.io/ip',
            'http://api.ipify.org',
            'http://checkip.amazonaws.com'
        ]

        for service in services:
            try:
                response = requests.get(service, timeout=10)
                if response.status_code == 200:
                    ip = response.text.strip()
                    # Clean up response (some services add extra text)
                    if ' ' in ip:
                        ip = ip.split()[0]
                    if self._is_valid_ip(ip):
                        return ip
            except Exception:
                continue

        return 'Unknown'

    def _is_valid_ip(self, ip):
        """Validate IP address format"""
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            return all(0 <= int(p) <= 255 for p in parts)
        except:
            return False

    def bulk_geo_lookup(self, ip_list):
        """Lookup multiple IPs efficiently"""
        results = []
        for ip in ip_list:
            results.append(self.get_geo_info(ip))
        return results

    def clear_cache(self):
        """Clear the geo cache"""
        self.cache.clear()

    def get_country_count(self):
        """Get count of unique countries in cache"""
        countries = set()
        for geo in self.cache.values():
            if geo.get('country') != 'Unknown':
                countries.add(geo['country'])
        return len(countries)

    def get_fastest_response_time(self):
        """Get fastest response time from cache"""
        response_times = []
        for geo in self.cache.values():
            if geo.get('response_time'):
                response_times.append(geo['response_time'])
        return min(response_times) if response_times else None

    def get_geo_stats(self):
        """Get statistics about cached geo data"""
        total = len(self.cache)
        countries = self.get_country_count()
        return {
            'total_lookups': total,
            'unique_countries': countries,
            'cache_hit_rate': (total - countries) / total if total > 0 else 0
        }
