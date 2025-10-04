#!/usr/bin/env python3
"""
Advanced Cookie Harvester - Realistic Browser History Simulation
Creates comprehensive cookie profiles that mimic genuine browsing behavior with temporal patterns,
cross-site relationships, and authentic cookie characteristics
"""
import asyncio
import aiohttp
import random
import json
import time
import sqlite3
import os
import csv
from typing import List, Dict, Tuple, Optional, Any
from urllib.parse import urljoin
import requests
from datetime import datetime, timedelta
import hashlib
import uuid

# Database path
DB = "cookies.db"

class CookieHarvester:
    def __init__(self):
        # Load top 1000 sites from CSV file as primary source
        self.top1000_sites = self._load_top1000_csv()

        # Fallback: Comprehensive website list for different categories (expanded for better coverage)
        self.site_categories = {
            'search_engines': [
                "google.com", "bing.com", "duckduckgo.com", "yahoo.com", "yandex.ru", "startpage.com",
                "baidu.com", "ecosia.org", "brave.com", "qwant.com", "swisscows.com", "metager.org"
            ],
            'social_media': [
                "facebook.com", "twitter.com", "instagram.com", "linkedin.com", "reddit.com", "tiktok.com",
                "snapchat.com", "pinterest.com", "threads.net", "mastodon.social", "bluesky.app", "flickr.com",
                "tumblr.com", "vk.com", "weibo.com", "discord.com"
            ],
            'tech_sites': [
                "github.com", "stackoverflow.com", "wikipedia.org", "medium.com", "dev.to",
                "hackernoon.com", "digitalocean.com", "linode.com", "aws.amazon.com", "azure.microsoft.com",
                "vercel.com", "netlify.com", "heroku.com", "gitlab.com", "bitbucket.org", "jetbrains.com"
            ],
            'shopping': [
                "amazon.com", "ebay.com", "paypal.com", "etsy.com", "shopify.com", "alibaba.com",
                "taobao.com", "walmart.com", "target.com", "bestbuy.com", "costco.com", "wayfair.com",
                "mercari.com", "poshmark.com", "depothomegoods.com"
            ],
            'entertainment': [
                "youtube.com", "netflix.com", "spotify.com", "twitch.tv", "hulu.com", "disneyplus.com",
                "hbomax.com", "primevideo.com", "vimeo.com", "dailymotion.com", "soundcloud.com",
                "pandora.com", "tidal.com", "crunchyroll.com", "funimation.com"
            ],
            'news': [
                "bbc.com", "cnn.com", "nytimes.com", "theguardian.com", "reuters.com", "foxnews.com",
                "nbcnews.com", "abcnews.go.com", "cbsnews.com", "npr.org", "theatlantic.com", "bloomberg.com",
                "forbes.com", "wsj.com", "economist.com", "aljazeera.com", "bbc.co.uk", "lemonde.fr"
            ],
            'productivity': [
                "canva.com", "dropbox.com", "slack.com", "zoom.us", "notion.com", "gmail.com",
                "outlook.com", "icloud.com", "onedrive.live.com", "drive.google.com", "docs.google.com",
                "figma.com", "adobe.com", "trello.com", "asana.com", "basecamp.com"
            ],
            'crypto_finance': [
                "coinbase.com", "binance.com", "kraken.com", "coinmarketcap.com", "coingecko.com",
                "uniswap.org", "sushiswap.org", "pancakeswap.finance", "compound.finance", "aave.com"
            ],
            'gaming': [
                "steam.com", "origin.com", "epicgames.com", "battlenet.com", "riotgames.com",
                "rockstargames.com", "ubisoft.com", "minecraft.net", "roblox.com", "twitch.tv"
            ],
            'education': [
                "coursera.org", "udemy.com", "edx.org", "khanacademy.org", "codecademy.com",
                "mozilla.org", "w3schools.com", "freecodecamp.org", "mit.edu", "stanford.edu",
                "harvard.edu", "berkeley.edu"
            ],
            'sports': [
                "espn.com", "foxsports.com", "nfl.com", "nba.com", "mlb.com", "soccer.com",
                "fifa.com", "uefa.com", "transfermarkt.com", "basketball-reference.com"
            ]
        }

        # Primary site list: use top1000.csv, fallback to categories
        if self.top1000_sites:
            self.top_sites = list(self.top1000_sites.values())
            print(f"✅ Loaded {len(self.top_sites)} top websites from CSV")
        else:
            # Fallback to categories if CSV loading fails
            self.top_sites = []
            for category_sites in self.site_categories.values():
                self.top_sites.extend(category_sites)
            print(f"⚠️ Using {len(self.top_sites)} fallback sites from categories (CSV not available)")

        # User agents for harvesting
        self.harvest_user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0"
        ]

    async def harvest_for_profile(self, profile_id: str, proxy: Optional[str] = None, count: int = 25, headless: bool = True) -> Tuple[int, List[Dict]]:
        """
        Harvest real cookies from top websites using profile's proxy and fingerprint
        Returns: (total_cookies_collected, list_of_successful_sites)
        """
        if count > len(self.top_sites):
            count = len(self.top_sites)

        # Select random sites to visit
        sites_to_visit = random.sample(self.top_sites, count)
        successful_sites = []
        total_cookies = 0

        # Setup proxy connector if proxy provided
        connector = None
        if proxy:
            try:
                from aiohttp_socks import ProxyConnector
                connector = ProxyConnector.from_url(f'socks5://{proxy}')
            except ImportError:
                print("Warning: aiohttp_socks not available, harvesting without proxy")

        # Create session with random user agent
        headers = {
            'User-Agent': random.choice(self.harvest_user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        timeout = aiohttp.ClientTimeout(total=30)

        try:
            async with aiohttp.ClientSession(connector=connector, timeout=timeout, headers=headers) as session:
                for i, site in enumerate(sites_to_visit):
                    try:
                        url = f"https://{site}"
                        print(f"Harvesting cookies from: {site} ({i+1}/{count})")

                        # Add random delay to appear human-like
                        await asyncio.sleep(random.uniform(2, 5))

                        async with session.get(url) as response:
                            if response.status == 200:
                                # Get cookies from response
                                cookies = response.cookies
                                site_cookies = []

                                for cookie in cookies.values():
                                    cookie_data = {
                                        'domain': cookie.get('domain', f".{site}"),
                                        'name': cookie.key,
                                        'value': cookie.value,
                                        'path': cookie.get('path', '/'),
                                        'expires': cookie.get('expires'),
                                        'secure': cookie.get('secure', False),
                                        'httponly': cookie.get('httponly', False),
                                        'samesite': cookie.get('samesite'),
                                        'harvested_from': site,
                                        'harvested_at': int(time.time())
                                    }
                                    site_cookies.append(cookie_data)

                                if site_cookies:
                                    # Store cookies in database
                                    self._store_harvested_cookies(profile_id, site_cookies)
                                    total_cookies += len(site_cookies)
                                    successful_sites.append({
                                        'site': site,
                                        'cookies': len(site_cookies),
                                        'status': response.status
                                    })

                                    print(f"  ✅ {site}: {len(site_cookies)} cookies harvested")
                                else:
                                    print(f"  ⚠️ {site}: No cookies collected")
                            else:
                                print(f"  ❌ {site}: HTTP {response.status}")

                    except Exception as e:
                        print(f"  ❌ {site}: Error - {e}")
                        continue

        except Exception as e:
            print(f"Session error: {e}")

        return total_cookies, successful_sites

    async def harvest_for_profile_concurrent(self, profile_id: str, proxy: Optional[str] = None,
                                            count: int = 25, max_concurrent: int = 10,
                                            headless: bool = True) -> Tuple[int, List[Dict]]:
        """
        Harvest real cookies from top websites concurrently using multi-threading
        Much faster than sequential harvesting

        Args:
            profile_id: Profile identifier for storing cookies
            proxy: Optional SOCKS5 proxy (ip:port format)
            count: Number of sites to visit
            max_concurrent: Maximum concurrent requests
            headless: Whether to run headless (currently unused)

        Returns:
            Tuple of (total_cookies_collected, successful_sites_list)
        """
        if count > len(self.top_sites):
            count = len(self.top_sites)

        # Select random sites to visit
        sites_to_visit = random.sample(self.top_sites, count)
        print(f"🚀 Starting concurrent cookie harvesting for {len(sites_to_visit)} sites (max {max_concurrent} concurrent)")

        # Split sites into batches for concurrent processing
        batches = []
        batch_size = max(1, len(sites_to_visit) // max_concurrent)
        for i in range(0, len(sites_to_visit), batch_size):
            batch = sites_to_visit[i:i + batch_size]
            batches.append(batch)

        # Setup proxy connector
        connector = None
        if proxy:
            try:
                from aiohttp_socks import ProxyConnector
                connector = ProxyConnector.from_url(f'socks5://{proxy}')
            except ImportError:
                print("⚠️ aiohttp_socks not available, harvesting without proxy")

        headers = {
            'User-Agent': random.choice(self.harvest_user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        timeout = aiohttp.ClientTimeout(total=20)  # Shorter timeout for concurrent operations

        async def harvest_batch(batch_sites: List[str]) -> Tuple[int, List[Dict]]:
            """Harvest cookies from a batch of sites concurrently"""
            batch_cookies = 0
            batch_successful = []

            try:
                async with aiohttp.ClientSession(connector=connector, timeout=timeout, headers=headers) as session:
                    # Create concurrent tasks for this batch
                    tasks = []
                    for site in batch_sites:
                        task = self._harvest_single_site(session, site, profile_id)
                        tasks.append(task)

                    # Execute batch concurrently
                    results = await asyncio.gather(*tasks, return_exceptions=True)

                    # Process results
                    for site, result in zip(batch_sites, results):
                        if isinstance(result, Exception):
                            print(f"  ❌ {site}: Exception - {result}")
                            continue

                        # Ensure result is properly unpacked
                        if isinstance(result, tuple) and len(result) == 2:
                            cookies_collected, site_info = result
                            if site_info:
                                batch_cookies += cookies_collected
                                batch_successful.append(site_info)

            except Exception as batch_error:
                print(f"  ⚠️ Batch error: {batch_error}")

            return batch_cookies, batch_successful

        # Process all batches concurrently (but not all sites at once due to memory constraints)
        total_cookies = 0
        all_successful_sites = []

        # Limit concurrent batches to manage memory
        semaphore = asyncio.Semaphore(min(3, len(batches)))  # Max 3 concurrent batches

        async def process_batch_with_semaphore(batch: List[str]):
            async with semaphore:
                return await harvest_batch(batch)

        # Run all batches with semaphore control
        batch_tasks = [process_batch_with_semaphore(batch) for batch in batches]
        batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)

        # Aggregate results
        for i, result in enumerate(batch_results):
            if isinstance(result, Exception):
                print(f"⚠️ Batch {i+1} failed: {result}")
                continue

            batch_cookies, batch_successful = result
            total_cookies += batch_cookies
            all_successful_sites.extend(batch_successful)

        # Final summary
        print(f"✅ Concurrent harvesting complete: {total_cookies} total cookies from {len(all_successful_sites)} sites")
        return total_cookies, all_successful_sites

    async def _harvest_single_site(self, session: aiohttp.ClientSession, site: str,
                                  profile_id: str) -> Tuple[int, Optional[Dict]]:
        """
        Harvest cookies from a single site
        Returns (cookies_count, site_info_dict) or (0, None) on failure
        """
        try:
            url = f"https://{site}"
            site_cookies = []

            # Add small random delay between requests (more human-like)
            await asyncio.sleep(random.uniform(0.5, 1.5))

            async with session.get(url) as response:
                if response.status == 200:
                    # Extract cookies from response
                    for cookie in response.cookies.values():
                        cookie_data = {
                            'domain': cookie.get('domain', f".{site}"),
                            'name': cookie.key,
                            'value': cookie.value,
                            'path': cookie.get('path', '/'),
                            'expires': cookie.get('expires'),
                            'secure': cookie.get('secure', False),
                            'httponly': cookie.get('httponly', False),
                            'samesite': cookie.get('samesite'),
                            'harvested_from': site,
                            'harvested_at': int(time.time())
                        }
                        site_cookies.append(cookie_data)

                    if site_cookies:
                        # Store cookies in database
                        self._store_harvested_cookies(profile_id, site_cookies)

                        site_info = {
                            'site': site,
                            'cookies': len(site_cookies),
                            'status': response.status
                        }

                        return len(site_cookies), site_info
                    else:
                        return 0, None
                else:
                    return 0, None

        except Exception as e:
            # Don't print individual errors in concurrent mode
            return 0, None

    def _store_harvested_cookies(self, profile_id: str, cookies: List[Dict]):
        """Store harvested cookies in SQLite database"""
        try:
            import sqlite3

            with sqlite3.connect(DB) as conn:
                # Create harvested_cookies table if it doesn't exist
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS harvested_cookies (
                        profile_id TEXT,
                        domain TEXT,
                        name TEXT,
                        value TEXT,
                        path TEXT,
                        expires INTEGER,
                        secure INTEGER,
                        httponly INTEGER,
                        samesite TEXT,
                        harvested_from TEXT,
                        harvested_at INTEGER,
                        PRIMARY KEY (profile_id, domain, name)
                    )
                ''')

                # Insert cookies
                for cookie in cookies:
                    conn.execute('''
                        INSERT OR REPLACE INTO harvested_cookies
                        (profile_id, domain, name, value, path, expires, secure, httponly, samesite, harvested_from, harvested_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        profile_id,
                        cookie['domain'],
                        cookie['name'],
                        cookie['value'],
                        cookie['path'],
                        cookie['expires'],
                        1 if cookie['secure'] else 0,
                        1 if cookie['httponly'] else 0,
                        cookie['samesite'],
                        cookie['harvested_from'],
                        cookie['harvested_at']
                    ))

                conn.commit()

        except Exception as e:
            print(f"Error storing cookies: {e}")

    def create_realistic_cookie_history(self, profile_id: str, months: int = 6) -> List[Dict]:
        """
        Create hyper-realistic cookie history that mimics actual browser usage patterns.
        Generates cookies with temporal patterns, cross-site relationships, and behavioral authenticity.
        """
        print(f"🔄 Creating realistic {months}-month cookie history for profile '{profile_id}'")
        current_time = int(time.time())

        # Initialize behavioral patterns
        behavioral_patterns = self._initialize_behavioral_patterns()

        # Generate temporal distribution of cookie creation
        temporal_distribution = self._generate_temporal_distribution(months, profile_id)

        # Generate comprehensive cookie set
        comprehensive_cookies = []

        # 1. Core website cookies (primary browsing destinations)
        print("  📊 Generating core website cookies...")
        core_cookies = self._generate_core_site_cookies(profile_id, temporal_distribution, behavioral_patterns)
        comprehensive_cookies.extend(core_cookies)

        # 2. Third-party tracking cookies (advertising networks, analytics)
        print("  🕵️ Generating tracking and analytics cookies...")
        tracking_cookies = self._generate_tracking_cookies(profile_id, temporal_distribution)
        comprehensive_cookies.extend(tracking_cookies)

        # 3. Social media embedded cookies (likes, shares, comments)
        print("  👥 Generating social media integration cookies...")
        social_cookies = self._generate_social_integration_cookies(profile_id, temporal_distribution)
        comprehensive_cookies.extend(social_cookies)

        # 4. Session management cookies (login states, session persistence)
        print("  🔐 Generating session and authentication cookies...")
        auth_cookies = self._generate_authentication_cookies(profile_id, temporal_distribution)
        comprehensive_cookies.extend(auth_cookies)

        # 5. CDN and performance cookies (delivery networks, caching)
        print("  🚀 Generating CDN and performance cookies...")
        cdn_cookies = self._generate_infrastructure_cookies(profile_id, temporal_distribution)
        comprehensive_cookies.extend(cdn_cookies)

        # 6. Browser-specific preference cookies (settings, themes, languages)
        print("  🎨 Generating browser preference cookies...")
        preference_cookies = self._generate_preference_cookies(profile_id, temporal_distribution)
        comprehensive_cookies.extend(preference_cookies)

        # 7. Cross-site relationship cookies (user journey tracking)
        print("  🌐 Generating cross-site relationship cookies...")
        relationship_cookies = self._generate_cross_site_relationships(profile_id, comprehensive_cookies, temporal_distribution)
        comprehensive_cookies.extend(relationship_cookies)

        # 8. Age and decay simulation (cookies naturally expire)
        print("  ⏰ Applying age decay and renewal patterns...")
        aged_cookies = self._apply_aging_and_decay(comprehensive_cookies, months, current_time)

        print(f"  🔥 Generated {len(aged_cookies)} realistic cookies with behavioral patterns")
        return aged_cookies

    def _initialize_behavioral_patterns(self) -> Dict[str, Any]:
        """Initialize patterns that mimic real browsing behavior"""
        return {
            'daily_visit_patterns': {
                # More active during work hours and evenings
                'morning_boost': 1.4,  # 9-12 PM
                'lunch_boost': 1.2,    # 12-2 PM
                'evening_boost': 1.8,  # 6-10 PM
                'weekend_boost': 1.6,  # Saturdays/Sundays
                'weekday_penalty': 0.85 # Weekdays less browsing
            },
            'browsing_habits': {
                # Site category preferences
                'search_preference': 0.85,  # Users search multiple times
                'social_amount': random.choice(['heavy', 'moderate', 'light']),
                'shopping_frequency': random.choice(['frequent', ' occasional', 'rare']),
                'Entertainment_preference': random.randrange(0, 100) / 100
            },
            'cookie_types': {
                'session_only': 0.15,     # 15% are session cookies
                'short_term': 0.45,       # 45% expire within 1-7 days
                'medium_term': 0.30,      # 30% expire within 1-4 weeks
                'long_term': 0.10         # 10% are persistent >1 month
            },
            'technical_behavior': {
                'javascript_enabled': random.choice([True, True, True, False]),  # 75% have JS
                'plugins_enabled': random.choice([True, False, False]),  # 33% have plugins
                'do_not_track': random.choice([False, False, False, True]),  # 25% have DNT
                'cookie_consent': random.choice(['accepted', 'accepted', 'declined', 'custom'])  # Mostly accepted
            }
        }

    def _generate_temporal_distribution(self, months: int, profile_id: str) -> Dict[int, Dict[str, Any]]:
        """Generate temporal distribution of browsing activity"""
        temporal_data = {}
        current_time = int(time.time())
        months_ago = current_time - (months * 30 * 24 * 3600)

        # Generate activity for each day over the period
        for day_offset in range(months * 30):
            timestamp = months_ago + (day_offset * 24 * 3600)

            # Determine activity level for this day
            activity_level = self._calculate_daily_activity(day_offset, months)

            temporal_data[timestamp] = {
                'activity_level': activity_level,
                'weekday': datetime.fromtimestamp(timestamp).weekday(),
                'browsing_hours': self._generate_browsing_hours(activity_level),
                'concurrent_sessions': random.randint(1, 3) if activity_level > 0.5 else 1
            }

        return temporal_data

    def _calculate_daily_activity(self, day_offset: int, total_months: int) -> float:
        """Calculate activity level for a specific day (0.0 to 1.0)"""
        current_time = int(time.time())
        target_time = current_time - (total_months * 30 * 24 * 3600) + (day_offset * 24 * 3600)
        weekday = datetime.fromtimestamp(target_time).weekday()

        # Base activity level
        base_activity = 0.3

        # Weekend bonus
        if weekday >= 5:  # Saturday/Sunday
            base_activity *= 1.6

        # Gradually increase activity towards present (people browse more recently)
        progress_ratio = day_offset / (total_months * 30)
        recency_boost = 0.5 * (1 + progress_ratio)  # More recent = more activity
        base_activity *= recency_boost

        # Seasonal variations
        month = datetime.fromtimestamp(target_time).month
        if month in [6, 7, 8]:  # Summer
            base_activity *= 1.3
        elif month in [11, 12, 1]:  # Winter holidays
            base_activity *= 0.9

        # Add random variation
        variation = random.uniform(0.7, 1.3)
        base_activity *= variation

        return min(1.0, max(0.1, base_activity))

    def _generate_browsing_hours(self, activity_level: float) -> List[int]:
        """Generate list of hours when browsing occurred"""
        hours_active = max(1, int(activity_level * 12))  # 1-12 hours of activity

        # Bias towards evening hours if high activity
        if activity_level > 0.7:
            hour_preferences = [18, 19, 20, 21, 17, 22, 12, 13, 14, 15, 16, 23, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        else:
            hour_preferences = list(range(24))

        return random.sample(hour_preferences, min(hours_active, 24))

    def _generate_core_site_cookies(self, profile_id: str, temporal_data: Dict[int, Dict[str, Any]],
                                   behavioral_patterns: Dict[str, Any]) -> List[Dict]:
        """Generate cookies from primary browsing destinations"""
        core_cookies = []

        # Focus on top 200 sites for realism
        sites_to_generate = random.sample(self.top_sites, min(200, len(self.top_sites)))

        for site in sites_to_generate:
            # Generate realistic cookie creation patterns for this site
            site_cookies = self._generate_site_specific_cookies(
                site, profile_id, temporal_data, behavioral_patterns
            )
            core_cookies.extend(site_cookies)

        return core_cookies

    def _generate_site_specific_cookies(self, site: str, profile_id: str, temporal_data: Dict[int, Dict[str, Any]],
                                       behavioral_patterns: Dict[str, Any]) -> List[Dict]:
        """Generate realistic cookie set for a specific website"""
        cookies = []
        site_hash = hashlib.md5(site.encode()).hexdigest()[:8]

        # Determine site category for behavior
        site_category = self._categorize_site(site)

        # Set default behavioral patterns if missing
        if not behavioral_patterns or 'technical_behavior' not in behavioral_patterns:
            behavioral_patterns = self._initialize_behavioral_patterns()

        # Generate different types of cookies this site would set
        cookie_types = [
            # Session/Visit tracking
            [self._generate_session_cookie(site, site_hash, temporal_data)],

            # Preference cookies
            [self._generate_preference_cookie(site, site_hash, temporal_data)],

            # Analytics cookies (if consent given)
            (self._generate_analytics_cookies(site, site_hash, temporal_data)
              if behavioral_patterns.get('technical_behavior', {}).get('cookie_consent') == 'accepted' else []),

            # Authentication tokens (if social/login site)
            (self._generate_auth_cookies(site, site_hash, temporal_data)
              if site_category in ['social', 'tech', 'shopping'] else [])
        ]

        # Flatten and filter
        for cookie_set in cookie_types:
            if cookie_set:
                if isinstance(cookie_set, list):
                    cookies.extend(cookie_set)
                else:
                    cookies.append(cookie_set)  # Handle any non-list returns

        return [c for c in cookies if c]  # Remove None values

    def _generate_session_cookie(self, site: str, site_hash: str, temporal_data: Dict[int, Dict[str, Any]]) -> Dict:
        """Generate session/visiting pattern cookies"""
        # Select realistic timestamps for visits
        if not temporal_data:
            # Fallback: generate synthetic timestamps for testing
            current_time = int(time.time())
            visit_timestamps = [current_time - i * 24 * 3600 for i in range(random.randint(3, 12))]
        else:
            active_days = [ts for ts, data in temporal_data.items() if data.get('activity_level', 0.5) > random.random()]

            if not active_days:
                active_days = list(temporal_data.keys())

            visit_count = min(len(active_days), random.randint(3, 12))
            visit_timestamps = random.sample(active_days, visit_count) if active_days else []

            # Final fallback if still empty
            if not visit_timestamps:
                current_time = int(time.time())
                visit_timestamps = [current_time - i * 24 * 3600 for i in range(random.randint(3, 12))]

        expiration_time = int(random.choice(visit_timestamps)) + random.randint(1800, 7200)

        return {
            'domain': f'.{site}',
            'name': 'session_id' if random.random() > 0.3 else f'visitor_{site_hash}',
            'value': str(uuid.uuid4())[:8],
            'path': '/',
            'expires': expiration_time,
            'secure': random.random() > 0.2,
            'httponly': random.random() > 0.6,
            'samesite': random.choice(['Lax', 'Strict', None]),
            'visits': visit_timestamps,
            'category': 'session'
        }

    def _generate_preference_cookie(self, site: str, site_hash: str, temporal_data: Dict[int, Dict[str, Any]]) -> Dict:
        """Generate user preference/settings cookies"""
        preferences = [
            ('theme', ['light', 'dark', 'auto']),
            ('lang', ['en', 'es', 'fr', 'de']),
            ('region', ['US', 'EU', 'ASIA', 'LATAM']),
            ('currency', ['USD', 'EUR', 'GBP', 'JPY'])
        ]

        pref_type, pref_options = random.choice(preferences)

        # Fallback for empty temporal data
        if not temporal_data:
            current_time = int(time.time())
            expiration_time = current_time + random.randint(30*24*3600, 365*24*3600)
        else:
            expiration_time = int(random.choice(list(temporal_data.keys()))) + random.randint(30*24*3600, 365*24*3600)

        return {
            'domain': f'.{site}',
            'name': f'{pref_type}_pref',
            'value': random.choice(pref_options),
            'path': '/',
            'expires': expiration_time,
            'secure': False,
            'httponly': False,
            'samesite': 'Lax',
            'category': 'preference'
        }

    def _generate_analytics_cookies(self, site: str, site_hash: str, temporal_data: Dict[int, Dict[str, Any]]) -> List[Dict]:
        """Generate analytics cookies (Google Analytics, etc.)"""
        analytics_providers = [
            ('_ga', str(random.randint(10**12, 10**13 - 1))),
            ('_gid', str(random.randint(10**12, 10**13 - 1))),
            ('_gat', '1'),
            ('_utma', f"{random.randint(10**9, 10**10)}.{random.randint(10**9, 10**10)}.{random.randint(10**9, 10**10)}"
                      f".{random.randint(10**9, 10**10)}.{random.randint(10**9, 10**10)}.1"),
            ('_utmz', f"{random.randint(10**9, 10**10)}.1.1.utm_medium=(none)")
        ]

        cookies = []
        selected_providers = random.sample(analytics_providers, random.randint(1, 3))

        for cookie_name, base_value in selected_providers:
            cookies.append({
                'domain': f'.{site}',
                'name': cookie_name,
                'value': base_value,
                'path': '/',
                'expires': int(random.choice(list(temporal_data.keys()))) + random.randint(63072000, 157680000),  # 2-5 years
                'secure': False,
                'httponly': False,
                'samesite': None,
                'category': 'analytics'
            })

        return cookies

    def _generate_auth_cookies(self, site: str, site_hash: str, temporal_data: Dict[int, Dict[str, Any]]) -> List[Dict]:
        """Generate authentication/session cookies for login-capable sites"""
        # Only generate if site supports authentication
        if random.random() > 0.6:  # 60% chance of having login cookies
            return []

        auth_cookies = [
            {
                'domain': f'.{site}',
                'name': 'auth_token',
                'value': hashlib.sha256(f"{site_hash}{random.randint(1000, 9999)}".encode()).hexdigest(),
                'path': '/',
                'expires': int(random.choice(list(temporal_data.keys()))) + random.randint(86400, 604800),  # 1-7 days
                'secure': True,
                'httponly': True,
                'samesite': 'Strict',
                'category': 'auth'
            }
        ]

        # Add remember-me cookie sometimes
        if random.random() > 0.5:
            auth_cookies.append({
                'domain': f'.{site}',
                'name': 'remember_user',
                'value': str(random.randint(10**12, 10**13 - 1)),
                'path': '/',
                'expires': int(random.choice(list(temporal_data.keys()))) + random.randint(30*24*3600, 90*24*3600),  # 30-90 days
                'secure': True,
                'httponly': True,
                'samesite': 'Strict',
                'category': 'auth'
            })

        return auth_cookies

    def _generate_tracking_cookies(self, profile_id: str, temporal_data: Dict[int, Dict[str, Any]]) -> List[Dict]:
        """Generate third-party tracking and advertising cookies"""
        tracking_cookies = []

        # Common tracking domains and their cookie patterns
        tracking_networks = {
            'doubleclick.net': [
                'test_cookie',
                'id',
                '_drt_',
                'DSID'
            ],
            'googlesyndication.com': [
                '_gads',
                '_gac_UA-'
            ],
            'facebook.com': [
                'fr',
                '_fbp',
                'sb'
            ],
            'ads.twitter.com': [
                'personalization_id'
            ],
            'linkedin.com': [
                'UserMatchHistory',
                'liap',
                'lidc'
            ]
        }

        # Generate tracking cookies based on visits to parent sites
        for network, cookies in tracking_networks.items():
            # Only include networks that would be loaded based on site visits
            if random.random() > 0.4:  # 60% chance of having a tracking network's cookies
                for cookie_name in random.sample(cookies, random.randint(1, len(cookies))):
                    # Generate realistic value
                    if 'id' in cookie_name or 'personalization' in cookie_name:
                        value = str(random.randint(10**15, 10**18))
                    elif cookie_name.startswith('_g'):
                        value = str(random.randint(10**12, 10**15))
                    else:
                        value = hashlib.md5(f"{network}{cookie_name}{random.randint(1000, 9999)}".encode()).hexdigest()[:16]

                    tracking_cookies.append({
                        'domain': f'.{network}',
                        'name': cookie_name,
                        'value': value,
                        'path': '/',
                        'expires': int(random.choice(list(temporal_data.keys()))) + random.randint(63072000, 157680000),  # 2-5 years
                        'secure': random.random() > 0.5,
                        'httponly': False,
                        'samesite': random.choice([None, 'Lax']),
                        'category': 'tracking'
                    })

        return tracking_cookies

    def _generate_social_integration_cookies(self, profile_id: str, temporal_data: Dict[int, Dict[str, Any]]) -> List[Dict]:
        """Generate social media integration cookies (likes, shares, embeds)"""
        social_cookies = []

        social_domains = {
            'facebook.com': ['act', 'c_user', 'datr', 'fr', 'presence'],
            'twitter.com': ['auth_token', 'ct0', 'guest_id', 'lang'],
            'instagram.com': ['sessionid', 'csrftoken', 'ds_user_id']
        }

        # Generate social cookies based on integrated browsing
        for domain, cookie_names in social_domains.items():
            if random.random() > 0.55:  # 45% chance of social integration cookies
                selected_cookies = random.sample(cookie_names, random.randint(1, 3))

                for cookie_name in selected_cookies:
                    social_cookies.append({
                        'domain': f'.{domain}',
                        'name': cookie_name,
                        'value': hashlib.sha256(f"{domain}{cookie_name}{random.randint(1000, 9999)}".encode()).hexdigest(),
                        'path': '/',
                        'expires': int(random.choice(list(temporal_data.keys()))) + random.randint(7*24*3600, 30*24*3600),  # 1 week - 1 month
                        'secure': True if cookie_name in ['sessionid', 'auth_token'] else False,
                        'httponly': False,
                        'samesite': 'Lax' if random.random() > 0.7 else None,
                        'category': 'social'
                    })

        return social_cookies

    def _generate_authentication_cookies(self, profile_id: str, temporal_data: Dict[int, Dict[str, Any]]) -> List[Dict]:
        """Generate authentication and session management cookies"""
        auth_cookies = []

        # Get recently active domains for authentication
        active_timestamps = sorted(temporal_data.keys(), reverse=True)[:10]  # Last 10 active days

        # Generate realistic auth patterns
        for i, timestamp in enumerate(random.sample(active_timestamps, min(5, len(active_timestamps)))):
            # Pick an auth-capable site
            auth_sites = ['github.com', 'stackoverflow.com', 'dropbox.com', 'slack.com', 'notion.com']
            if self.top_sites:
                auth_sites = [site for site in self.top_sites[:50] if any(x in site for x in ['github', 'stack', 'dropbox', 'slack', 'notion'])][:5]
                device_types = ['mobile', 'desktop', 'tablet', 'desktop', 'mobile']  # Bias toward mobile/desktop

                auth_cookies.append({
                    'domain': f'.{random.choice(auth_sites)}',
                    'name': f'auth_session_{i}',
                    'value': str(uuid.uuid4()),
                    'path': '/',
                    'expires': int(timestamp) + random.randint(3600, 86400),  # 1-24 hour sessions
                    'secure': True,
                    'httponly': True,
                    'samesite': 'Strict',
                    'device_type': random.choice(device_types),
                    'category': 'auth'
                })

        return auth_cookies

    def _generate_infrastructure_cookies(self, profile_id: str, temporal_data: Dict[int, Dict[str, Any]]) -> List[Dict]:
        """Generate cookies from CDN and infrastructure providers"""
        infra_cookies = []

        cdn_providers = {
            'cloudflare.com': ['__cfduid', 'cf_ob_info', 'cf_use_ob'],
            'fastly.com': ['fastly_cdn_check', 'fastly_sessions'],
            'cloudfront.net': ['amzn_cf_session', 'amzn_cfAuth'],
            'akamai.net': ['AKA_A2', 'akamai_generated'],
            'jsdelivr.net': ['jsdelivr_user', 'jsdelivr_cache']
        }

        # Generate infrastructure cookies for frequently visited content
        for provider, cookies in cdn_providers.items():
            if random.random() > 0.6:  # 40% chance of having a provider's cookies
                selected_cookies = random.sample(cookies, random.randint(1, len(cookies)))

                for cookie_name in selected_cookies:
                    infra_cookies.append({
                        'domain': f'.{provider}',
                        'name': cookie_name,
                        'value': hashlib.md5(f"{provider}{cookie_name}{random.randint(1000, 9999)}".encode()).hexdigest()[:12],
                        'path': '/',
                        'expires': int(random.choice(list(temporal_data.keys()))) + random.randint(86400, 604800),  # 1 day - 1 week
                        'secure': True,
                        'httponly': False,
                        'samesite': None,
                        'category': 'infrastructure'
                    })

        return infra_cookies

    def _generate_preference_cookies(self, profile_id: str, temporal_data: Dict[int, Dict[str, Any]]) -> List[Dict]:
        """Generate browser and site preference cookies"""
        preference_cookies = []

        # User preference patterns
        preference_sets = [
            ('theme', ['dark', 'light', 'auto', 'system']),
            ('autoplay', ['enabled', 'disabled', 'wifi_only']),
            ('notifications', ['granted', 'denied', 'default']),
            ('language', ['en-US', 'en-GB', 'es-ES', 'fr-FR', 'de-DE', 'pt-BR']),
            ('timezone', ['America/New_York', 'Europe/London', 'America/Los_Angeles', 'Asia/Tokyo']),
            ('currency', ['USD', 'EUR', 'GBP', 'BRL', 'JPY']),
            ('search_engine', ['google', 'bing', 'duckduckgo', 'yahoo'])
        ]

        # Generate preference cookies across multiple sites
        num_sites = min(15, len(self.top_sites))
        preference_sites = random.sample(self.top_sites, num_sites)

        for site in preference_sites:
            # Each site gets a random preference
            pref_type, pref_options = random.choice(preference_sets)

            # Get expiration time with fallback
            if temporal_data:
                expiration_time = int(random.choice(list(temporal_data.keys()))) + random.randint(30*24*3600, 365*24*3600)
            else:
                current_time = int(time.time())
                expiration_time = current_time + random.randint(30*24*3600, 365*24*3600)

            preference_cookies.append({
                'domain': f'.{site}',
                'name': f'{pref_type}_user',
                'value': random.choice(pref_options),
                'path': '/',
                'expires': expiration_time,
                'secure': False,
                'httponly': False,
                'samesite': 'Lax',
                'category': 'user_preference'
            })

        return preference_cookies

    def _categorize_site(self, site: str) -> str:
        """Categorize a site based on common patterns"""
        site_lower = site.lower()
        for category, sites in self.site_categories.items():
            if site_lower in sites:
                return category

        # Fallback categorization
        if any(domain in site_lower for domain in ['google', 'bing', 'yahoo']):
            return 'search_engines'
        elif any(domain in site_lower for domain in ['facebook', 'twitter', 'instagram']):
            return 'social_media'
        elif any(domain in site_lower for domain in ['github', 'stackoverflow']):
            return 'tech_sites'
        elif any(domain in site_lower for domain in ['amazon', 'ebay']):
            return 'shopping'
        else:
            return 'general'

    def _generate_cross_site_relationships(self, profile_id: str, existing_cookies: List[Dict],
                                         temporal_data: Dict[int, Dict[str, Any]]) -> List[Dict]:
        """Generate cookies that show cross-site browsing relationships"""
        relationship_cookies = []

        # Common relationship patterns
        relationships = {
            'search_to_social': ['google.com', 'facebook.com', 'twitter.com'],
            'social_to_shopping': ['facebook.com', 'instagram.com', 'amazon.com'],
            'tech_to_news': ['github.com', 'stackoverflow.com', 'bbc.com'],
            'shopping_to_social': ['amazon.com', 'facebook.com', 'pinterest.com']
        }

        for relationship_name, site_sequence in relationships.items():
            if random.random() > 0.7:  # 30% chance of having cross-site relationships
                continue

            # Create interconnected cookies across the sites
            for i, site in enumerate(site_sequence[:-1]):
                next_site = site_sequence[i + 1]
                relationship_cookies.append({
                    'domain': f'.{next_site}',
                    'name': f'referral_from_{site.replace(".", "_")}',
                    'value': hashlib.md5(f"{site}_{next_site}_{random.randint(1000, 9999)}".encode()).hexdigest()[:12],
                    'path': '/',
                    'expires': int(random.choice(list(temporal_data.keys()))) + random.randint(7*24*3600, 30*24*3600),
                    'secure': True,
                    'httponly': False,
                    'samesite': 'Lax',
                    'relationship': f'{site}_to_{next_site}',
                    'category': 'cross_reference'
                })

        return relationship_cookies

    def _apply_aging_and_decay(self, cookies: List[Dict], months: int, current_time: int) -> List[Dict]:
        """Apply realistic aging and natural cookie decay patterns"""
        aged_cookies = []

        for cookie in cookies:
            # Ensure cookie is a dictionary
            if not isinstance(cookie, dict):
                print(f"⚠️ Skipping invalid cookie data: {type(cookie)}")
                continue

            # Skip already aged cookies
            if cookie.get('aged'):
                aged_cookies.append(cookie)
                continue

            # Calculate age-based expiration
            months_ago = current_time - (months * 30 * 24 * 3600)

            # Apply natural cookie decay (some cookies expire naturally)
            decay_probability = 0.7  # 70% chance cookie has naturally expired
            if random.random() < decay_probability:
                # Set expiration somewhere in the history period
                cookie['expires'] = months_ago + random.randint(1, months * 30 * 24 * 3600)
                cookie['expired'] = True
            else:
                # Cookie is still valid
                cookie['expires'] = current_time + random.randint(24*3600, 365*24*3600)  # 1 day to 1 year

            cookie['aged'] = True
            cookie['aging_applied'] = months

            aged_cookies.append(cookie)

        return aged_cookies

    def create_aged_cookies(self, profile_id: str, months: int = 6) -> List[Dict]:
        """
        Create aged cookie timeline from harvested cookies
        Returns list of cookies with back-dated expiration times
        """
        try:
            import sqlite3

            with sqlite3.connect(DB) as conn:
                # Get harvested cookies for this profile
                cursor = conn.execute('''
                    SELECT domain, name, value, path, expires, secure, httponly, samesite, harvested_from
                    FROM harvested_cookies
                    WHERE profile_id = ?
                ''', (profile_id,))

                harvested_cookies = cursor.fetchall()

            if not harvested_cookies:
                print("No harvested cookies found, using synthetic timeline")
                # Generate synthetic cookies if none harvested
                return self.create_realistic_cookie_history(profile_id, months)

            # Create aged timeline
            aged_cookies = []
            current_time = int(time.time())

            for cookie_data in harvested_cookies:
                domain, name, value, path, expires, secure, httponly, samesite, harvested_from = cookie_data

                # Calculate back-dated expiration (months ago)
                months_ago = current_time - (months * 30 * 24 * 3600)

                # Create aged cookie
                aged_cookie = {
                    'domain': domain,
                    'name': name,
                    'value': value,
                    'path': path,
                    'expires': months_ago,
                    'secure': bool(secure),
                    'httponly': bool(httponly),
                    'samesite': samesite,
                    'harvested_from': harvested_from,
                    'aged': True,
                    'aging_period': months
                }

                aged_cookies.append(aged_cookie)

            print(f"Created aged timeline with {len(aged_cookies)} cookies from {len(harvested_cookies)} harvested cookies")
            return aged_cookies

        except Exception as e:
            print(f"Error creating aged cookies: {e}")
            return []

    def get_harvest_stats(self, profile_id: str) -> Dict:
        """Get statistics about harvested cookies for a profile"""
        try:
            import sqlite3

            with sqlite3.connect(DB) as conn:
                # Get harvest statistics
                cursor = conn.execute('''
                    SELECT
                        COUNT(*) as total_cookies,
                        COUNT(DISTINCT harvested_from) as unique_sites,
                        COUNT(DISTINCT domain) as unique_domains,
                        MIN(harvested_at) as first_harvest,
                        MAX(harvested_at) as last_harvest
                    FROM harvested_cookies
                    WHERE profile_id = ?
                ''', (profile_id,))

                stats = cursor.fetchone()

                if stats and stats[0] > 0:
                    return {
                        'total_cookies': stats[0],
                        'unique_sites': stats[1],
                        'unique_domains': stats[2],
                        'first_harvest': stats[3],
                        'last_harvest': stats[4],
                        'harvest_period_days': (stats[4] - stats[3]) / (24 * 3600) if stats[3] and stats[4] else 0
                    }

        except Exception as e:
            print(f"Error getting harvest stats: {e}")

        return {'total_cookies': 0, 'unique_sites': 0, 'unique_domains': 0}

    def clear_harvested_cookies(self, profile_id: Optional[str] = None):
        """Clear harvested cookies for a profile or all profiles"""
        try:
            import sqlite3

            with sqlite3.connect(DB) as conn:
                if profile_id:
                    conn.execute('DELETE FROM harvested_cookies WHERE profile_id = ?', (profile_id,))
                else:
                    conn.execute('DELETE FROM harvested_cookies')

                conn.commit()
                print(f"Cleared harvested cookies for profile: {profile_id or 'ALL'}")

        except Exception as e:
            print(f"Error clearing harvested cookies: {e}")

    def generate_comprehensive_cookie_history(self, profile_id: str, proxy: Optional[str] = None,
                                              include_categories: Optional[List[str]] = None) -> Dict[str, List[Dict]]:
        """
        Generate comprehensive cookie history with 3-month, 6-month, and 12-month timelines.
        Visits multiple websites and creates aged cookie histories for realistic browser profiles.

        Args:
            profile_id (str): Unique identifier for this browsing profile
            proxy (Optional[str]): SOCKS5 proxy to use (format: ip:port)
            include_categories (List[str]): Categories of sites to visit (default: all)

        Returns:
            Dict containing cookie histories for different time periods
        """
        # Use all categories if none specified
        if include_categories is None:
            include_categories = list(self.site_categories.keys())

        # Collect sites from selected categories
        sites_to_visit = []
        for category in include_categories:
            if category in self.site_categories:
                sites_to_visit.extend(self.site_categories[category])

        if not sites_to_visit:
            print("❌ No sites available for selected categories")
            return {}

        # Batch size for processing
        batch_size = min(50, len(sites_to_visit))
        print(f"🎯 Starting comprehensive cookie generation for profile '{profile_id}'")
        print(f"📋 Categories: {', '.join(include_categories)}")
        print(f"🌐 Total sites to visit: {batch_size}")

        try:
            # Step 1: Harvest fresh cookies from websites
            print("\n🍪 PHASE 1: Collecting fresh cookies from websites...")
            total_cookies, successful_sites = asyncio.run(
                self.harvest_for_profile(profile_id, proxy, batch_size, headless=True)
            )

            if total_cookies == 0:
                print("❌ No cookies could be harvested from any sites")
                return {}

            print(f"✅ Successfully harvested {total_cookies} cookies from {len(successful_sites)} sites")

            # Step 2: Generate different time-based cookie histories
            histories = {}
            time_periods = [(3, "3_month"), (6, "6_month"), (12, "12_month")]

            print("\n📅 PHASE 2: Creating aged cookie timelines...")

            for months, key_name in time_periods:
                print(f"  📊 Generating {months}-month cookie history...")
                aged_cookies = self.create_aged_cookies(profile_id, months)

                if aged_cookies:
                    histories[key_name] = aged_cookies
                    print(f"    ✅ Created {len(aged_cookies)} aged cookies for {months}-month timeline")
                else:
                    print(f"    ⚠️ No aged cookies created for {months}-month timeline")

            # Step 3: Save comprehensive cookie profile
            self._save_comprehensive_profile(profile_id, histories, successful_sites)

            print(f"\n🎉 Cookie generation complete!")
            print(f"📊 Profile '{profile_id}' ready with multiple timelines")
            print("=" * 60)

            return histories

        except Exception as e:
            print(f"❌ Cookie generation failed: {e}")
            return {}

    def create_3_month_history(self, profile_id: str, proxy: Optional[str] = None) -> List[Dict]:
        """Generate a 3-month cookie browsing history"""
        return self.create_aged_cookies(profile_id, months=3)

    def create_6_month_history(self, profile_id: str, proxy: Optional[str] = None) -> List[Dict]:
        """Generate a 6-month cookie browsing history"""
        return self.create_aged_cookies(profile_id, months=6)

    def create_12_month_history(self, profile_id: str, proxy: Optional[str] = None) -> List[Dict]:
        """Generate a 12-month cookie browsing history"""
        return self.create_aged_cookies(profile_id, months=12)

    def create_multilayer_history(self, profile_id: str, proxy: Optional[str] = None) -> Dict[str, List[Dict]]:
        """
        Create a multi-layered browsing history with different types of cookies
        """
        print(f"🔄 Creating multi-layered browsing history for profile '{profile_id}'")

        # First, harvest comprehensive cookie set
        comprehensive_history = self.generate_comprehensive_cookie_history(
            profile_id, proxy, include_categories=['search_engines', 'social_media', 'tech_sites']
        )

        if not comprehensive_history:
            return {}

        # Enhance each timeline with additional logic
        enhanced_histories = {}

        for period_key, cookies in comprehensive_history.items():
            # Add session cookies and other realistic elements
            enhanced_cookies = self._enhance_cookie_history(cookies, period_key)
            enhanced_histories[f"{period_key}_enhanced"] = enhanced_cookies

            print(f"  ✨ Enhanced {period_key} timeline: {len(enhanced_cookies)} cookies")

        return {**comprehensive_history, **enhanced_histories}

    def _load_top1000_csv(self) -> Dict[int, str]:
        """
        Load top 1000 websites from CSV file
        Returns dict with rank as key and domain as value
        """
        csv_sites = {}
        csv_file = "top1000.csv"

        try:
            if not os.path.exists(csv_file):
                print(f"⚠️ CSV file '{csv_file}' not found")
                return {}

            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                # Check if expected columns exist
                headers = reader.fieldnames
                if not headers or 'rank' not in headers or 'domain' not in headers:
                    print(f"⚠️ CSV file missing required columns (rank, domain). Found: {headers}")
                    return {}

                for row in reader:
                    try:
                        rank = int(row['rank'])
                        domain = row['domain'].strip()
                        score = float(row.get('score', 0))

                        # Basic domain validation
                        if domain and '.' in domain and len(domain) > 3:
                            csv_sites[rank] = domain

                    except (ValueError, KeyError) as e:
                        print(f"⚠️ Skipping invalid CSV row: {row} - {e}")
                        continue

            print(f"✅ Loaded {len(csv_sites)} websites from CSV")
            return csv_sites

        except Exception as e:
            print(f"❌ Error loading CSV file: {e}")
            return {}

    def _enhance_cookie_history(self, cookies: List[Dict], period: str) -> List[Dict]:
        """Enhance cookie history with additional realistic elements"""
        enhanced_cookies = cookies.copy()
        current_time = int(time.time())

        # Add some default browser cookies that websites commonly set
        default_cookies = {
            '3_month': [{
                'domain': '.google.com',
                'name': 'PREF',
                'value': 'TZ=America/Denver',
                'path': '/',
                'secure': True,
                'httponly': False,
                'samesite': 'Lax'
            }],
            '6_month': [{
                'domain': '.wikipedia.org',
                'name': 'language',
                'value': 'en',
                'path': '/',
                'secure': False,
                'httponly': False,
                'samesite': None
            }],
            '12_month': [{
                'domain': '.github.com',
                'name': 'color_mode',
                'value': '{"color_mode":"auto"}',
                'path': '/',
                'secure': True,
                'httponly': False,
                'samesite': 'Lax'
            }]
        }

        if period in default_cookies:
            for cookie in default_cookies[period]:
                cookie_copy = cookie.copy()
                cookie_copy['expires'] = current_time - (int(period.split('_')[0]) * 30 * 24 * 3600)
                cookie_copy['harvested_from'] = cookie_copy['domain'].lstrip('.')
                cookie_copy['aged'] = True
                enhanced_cookies.append(cookie_copy)

        return enhanced_cookies

    def _save_comprehensive_profile(self, profile_id: str, histories: Dict[str, List[Dict]], sites_visited: List[Dict]):
        """Save comprehensive profile data for later use"""
        try:
            profile_data = {
                'profile_id': profile_id,
                'created_at': int(time.time()),
                'sites_visited': sites_visited,
                'histories': {k: len(v) for k, v in histories.items()},
                'total_cookies': sum(len(cookies) for cookies in histories.values())
            }

            # Save to JSON file
            profile_file = f"profiles/{profile_id}_profile.json"
            os.makedirs('profiles', exist_ok=True)

            with open(profile_file, 'w') as f:
                json.dump(profile_data, f, indent=2)

            print(f"💾 Profile saved: {profile_file}")

        except Exception as e:
            print(f"⚠️ Could not save profile data: {e}")

    def get_profile_info(self, profile_id: str) -> Dict:
        """Get information about a cookie profile"""
        try:
            profile_file = f"profiles/{profile_id}_profile.json"
            if os.path.exists(profile_file):
                with open(profile_file, 'r') as f:
                    return json.load(f)

            # Fallback: get basic info from database
            stats = self.get_harvest_stats(profile_id)
            return {
                'profile_id': profile_id,
                'total_cookies': stats['total_cookies'],
                'unique_sites': stats['unique_sites'],
                'created_from_db': True
            }

        except Exception as e:
            print(f"Error getting profile info: {e}")
            return {}

# Synchronous wrapper for threading
def harvest_for_profile_sync(profile_id: str, proxy: Optional[str] = None, count: int = 25, headless: bool = True):
    """Synchronous wrapper for cookie harvesting"""
    harvester = CookieHarvester()
    return asyncio.run(harvester.harvest_for_profile(profile_id, proxy, count, headless))
