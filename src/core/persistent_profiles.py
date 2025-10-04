#!/usr/bin/env python3
"""
Persistent Profile System for Ultimate Anonymity Toolkit
Creates believable, long-term digital identities with consistent fingerprints
"""

import sqlite3
import json
import random
import time
import os
import webbrowser
import asyncio
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
import hashlib
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class GeoLocation:
    """Geographic location data"""
    country: str
    country_code: str
    region: str
    city: str
    latitude: float
    longitude: float
    timezone: str
    isp: str

@dataclass
class HardwareProfile:
    """Hardware characteristics for consistent fingerprinting"""
    cpu_cores: int
    memory_gb: int
    screen_width: int
    screen_height: int
    screen_depth: int
    pixel_ratio: float
    gpu_vendor: str
    gpu_renderer: str
    platform: str
    architecture: str

@dataclass
class BrowserProfile:
    """Browser-specific characteristics"""
    name: str
    version: str
    user_agent: str
    accept_language: str
    accept_encoding: str
    accept_headers: Dict[str, str]
    plugins: List[str]
    fonts: List[str]
    canvas_fingerprint: str
    webgl_fingerprint: str
    audio_fingerprint: str

@dataclass
class BehavioralPattern:
    """User behavioral patterns"""
    active_hours: List[int]  # Hours of day when active (0-23)
    browsing_speed: float  # Pages per minute
    scroll_patterns: Dict[str, float]  # Scroll behavior metrics
    click_patterns: Dict[str, float]  # Click behavior metrics
    typing_speed: float  # Characters per minute
    pause_patterns: List[float]  # Pause durations between actions
    session_duration: Tuple[int, int]  # Min/max session duration in minutes

@dataclass
class InterestProfile:
    """User interests and preferences"""
    categories: List[str]  # Main interest categories
    websites: List[str]  # Frequently visited sites
    search_terms: List[str]  # Common search queries
    social_platforms: List[str]  # Used social media platforms
    shopping_preferences: List[str]  # Shopping categories
    news_sources: List[str]  # Preferred news sites
    entertainment: List[str]  # Entertainment preferences

@dataclass
class UserProfile:
    """Complete persistent user profile"""
    # Core Identity
    profile_id: str
    profile_name: str
    creation_date: datetime
    last_used: datetime
    
    # Demographics
    age_range: str  # "18-25", "26-35", etc.
    gender: str
    education_level: str
    occupation: str
    income_range: str
    
    # Geographic
    location: GeoLocation
    
    # Technical
    hardware: HardwareProfile
    browser: BrowserProfile
    
    # Behavioral
    behavior: BehavioralPattern
    interests: InterestProfile
    
    # Session Data
    browsing_history: List[Dict] = field(default_factory=list)
    cookies: Dict[str, Any] = field(default_factory=dict)
    local_storage: Dict[str, Any] = field(default_factory=dict)
    session_storage: Dict[str, Any] = field(default_factory=dict)
    
    # Evolution tracking
    last_evolution: datetime = field(default_factory=datetime.now)
    evolution_log: List[Dict] = field(default_factory=list)

class ProfileDatabase:
    """Database manager for persistent profiles"""
    
    def __init__(self, db_path: str = "profiles/profiles.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize the profile database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS profiles (
                        profile_id TEXT PRIMARY KEY,
                        profile_name TEXT UNIQUE NOT NULL,
                        profile_data TEXT NOT NULL,
                        creation_date TEXT NOT NULL,
                        last_used TEXT NOT NULL,
                        is_active BOOLEAN DEFAULT 1
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS browsing_sessions (
                        session_id TEXT PRIMARY KEY,
                        profile_id TEXT NOT NULL,
                        start_time TEXT NOT NULL,
                        end_time TEXT,
                        session_data TEXT,
                        FOREIGN KEY (profile_id) REFERENCES profiles (profile_id)
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS profile_evolution (
                        evolution_id TEXT PRIMARY KEY,
                        profile_id TEXT NOT NULL,
                        evolution_date TEXT NOT NULL,
                        changes TEXT NOT NULL,
                        reason TEXT,
                        FOREIGN KEY (profile_id) REFERENCES profiles (profile_id)
                    )
                """)
                
                conn.commit()
                logger.info("Profile database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            traceback.print_exc()
    
    def save_profile(self, profile: UserProfile) -> bool:
        """Save or update a profile in the database"""
        try:
            profile_data = json.dumps(asdict(profile), default=str, indent=2)
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO profiles 
                    (profile_id, profile_name, profile_data, creation_date, last_used)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    profile.profile_id,
                    profile.profile_name,
                    profile_data,
                    profile.creation_date.isoformat(),
                    profile.last_used.isoformat()
                ))
                conn.commit()
                logger.info(f"Profile {profile.profile_name} saved successfully")
                return True
        except Exception as e:
            logger.error(f"Failed to save profile: {e}")
            traceback.print_exc()
            return False
    
    def load_profile(self, profile_id: str) -> Optional[UserProfile]:
        """Load a profile from the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT profile_data FROM profiles WHERE profile_id = ?",
                    (profile_id,)
                )
                row = cursor.fetchone()
                
                if row:
                    profile_data = json.loads(row[0])
                    # Convert datetime strings back to datetime objects
                    profile_data['creation_date'] = datetime.fromisoformat(profile_data['creation_date'])
                    profile_data['last_used'] = datetime.fromisoformat(profile_data['last_used'])
                    profile_data['last_evolution'] = datetime.fromisoformat(profile_data['last_evolution'])
                    
                    # Reconstruct nested objects
                    profile_data['location'] = GeoLocation(**profile_data['location'])
                    profile_data['hardware'] = HardwareProfile(**profile_data['hardware'])
                    profile_data['browser'] = BrowserProfile(**profile_data['browser'])
                    profile_data['behavior'] = BehavioralPattern(**profile_data['behavior'])
                    profile_data['interests'] = InterestProfile(**profile_data['interests'])
                    
                    return UserProfile(**profile_data)
                return None
        except Exception as e:
            logger.error(f"Failed to load profile: {e}")
            traceback.print_exc()
            return None
    
    def list_profiles(self) -> List[Dict[str, str]]:
        """List all available profiles"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT profile_id, profile_name, creation_date, last_used, is_active
                    FROM profiles ORDER BY last_used DESC
                """)
                return [
                    {
                        'profile_id': row[0],
                        'profile_name': row[1],
                        'creation_date': row[2],
                        'last_used': row[3],
                        'is_active': bool(row[4])
                    }
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            logger.error(f"Failed to list profiles: {e}")
            return []
    
    def delete_profile(self, profile_id: str) -> bool:
        """Delete a profile from the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM profiles WHERE profile_id = ?", (profile_id,))
                conn.execute("DELETE FROM browsing_sessions WHERE profile_id = ?", (profile_id,))
                conn.execute("DELETE FROM profile_evolution WHERE profile_id = ?", (profile_id,))
                conn.commit()
                logger.info(f"Profile {profile_id} deleted successfully")
                return True
        except Exception as e:
            logger.error(f"Failed to delete profile: {e}")
            return False

class ProfileGenerator:
    """Generates realistic, believable user profiles"""
    
    def __init__(self):
        self.demographic_data = self._load_demographic_data()
        self.location_data = self._load_location_data()
        self.browser_data = self._load_browser_data()
    
    def _load_demographic_data(self) -> Dict:
        """Load demographic data for realistic profile generation"""
        return {
            'age_ranges': ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
            'genders': ['male', 'female', 'non-binary'],
            'education_levels': ['high_school', 'some_college', 'bachelors', 'masters', 'doctorate'],
            'occupations': [
                'software_engineer', 'teacher', 'nurse', 'manager', 'sales', 'student',
                'consultant', 'designer', 'analyst', 'administrator', 'technician'
            ],
            'income_ranges': ['<30k', '30k-50k', '50k-75k', '75k-100k', '100k-150k', '150k+']
        }
    
    def _load_location_data(self) -> List[GeoLocation]:
        """Load realistic location data"""
        return [
            GeoLocation("United States", "US", "California", "Los Angeles", 34.0522, -118.2437, "America/Los_Angeles", "Comcast"),
            GeoLocation("United States", "US", "New York", "New York", 40.7128, -74.0060, "America/New_York", "Verizon"),
            GeoLocation("United Kingdom", "GB", "England", "London", 51.5074, -0.1278, "Europe/London", "BT"),
            GeoLocation("Germany", "DE", "Bavaria", "Munich", 48.1351, 11.5820, "Europe/Berlin", "Deutsche Telekom"),
            GeoLocation("Canada", "CA", "Ontario", "Toronto", 43.6532, -79.3832, "America/Toronto", "Rogers"),
            GeoLocation("Australia", "AU", "New South Wales", "Sydney", -33.8688, 151.2093, "Australia/Sydney", "Telstra"),
        ]
    
    def _load_browser_data(self) -> Dict:
        """Load browser configuration data"""
        return {
            'chrome_versions': ['120.0.6099.109', '119.0.6045.199', '118.0.5993.117'],
            'firefox_versions': ['121.0', '120.0.1', '119.0'],
            'edge_versions': ['120.0.2210.91', '119.0.2151.97', '118.0.2088.76'],
            'common_fonts': [
                'Arial', 'Times New Roman', 'Helvetica', 'Calibri', 'Verdana',
                'Georgia', 'Trebuchet MS', 'Comic Sans MS', 'Impact', 'Lucida Console'
            ],
            'common_plugins': [
                'Chrome PDF Plugin', 'Chrome PDF Viewer', 'Native Client',
                'Widevine Content Decryption Module', 'Shockwave Flash'
            ]
        }

    def generate_profile(self, profile_name: str, location_preference: Optional[str] = None) -> UserProfile:
        """Generate a complete, believable user profile"""
        profile_id = str(uuid.uuid4())
        now = datetime.now()

        # Select demographics
        age_range = random.choice(self.demographic_data['age_ranges'])
        gender = random.choice(self.demographic_data['genders'])
        education = random.choice(self.demographic_data['education_levels'])
        occupation = random.choice(self.demographic_data['occupations'])
        income = random.choice(self.demographic_data['income_ranges'])

        # Select location
        if location_preference:
            location = next((loc for loc in self.location_data if loc.country_code == location_preference),
                          random.choice(self.location_data))
        else:
            location = random.choice(self.location_data)

        # Generate hardware profile (consistent with demographics)
        hardware = self._generate_hardware_profile(age_range, income)

        # Generate browser profile
        browser = self._generate_browser_profile(hardware, location)

        # Generate behavioral patterns
        behavior = self._generate_behavioral_pattern(age_range, occupation)

        # Generate interests
        interests = self._generate_interests(age_range, occupation)

        return UserProfile(
            profile_id=profile_id,
            profile_name=profile_name,
            creation_date=now,
            last_used=now,
            age_range=age_range,
            gender=gender,
            education_level=education,
            occupation=occupation,
            income_range=income,
            location=location,
            hardware=hardware,
            browser=browser,
            behavior=behavior,
            interests=interests
        )

    def _generate_hardware_profile(self, age_range: str, income_range: str) -> HardwareProfile:
        """Generate hardware specs consistent with demographics"""
        # Younger, higher income = better hardware
        age_factor = 1.0 if '18-25' in age_range or '26-35' in age_range else 0.7
        income_factor = 1.0 if '100k' in income_range or '150k' in income_range else 0.8

        quality_factor = age_factor * income_factor

        # CPU cores
        cpu_cores = random.choice([4, 6, 8, 12, 16]) if quality_factor > 0.8 else random.choice([2, 4, 6])

        # Memory
        memory_gb = random.choice([8, 16, 32]) if quality_factor > 0.8 else random.choice([4, 8, 16])

        # Screen resolution
        resolutions = [
            (1920, 1080), (2560, 1440), (3840, 2160)
        ] if quality_factor > 0.8 else [
            (1366, 768), (1920, 1080), (1600, 900)
        ]
        screen_width, screen_height = random.choice(resolutions)

        # GPU
        gpus = [
            ("NVIDIA Corporation", "NVIDIA GeForce RTX 3080"),
            ("NVIDIA Corporation", "NVIDIA GeForce RTX 3070"),
            ("AMD", "AMD Radeon RX 6800 XT")
        ] if quality_factor > 0.8 else [
            ("Intel Inc.", "Intel(R) UHD Graphics 620"),
            ("NVIDIA Corporation", "NVIDIA GeForce GTX 1650"),
            ("AMD", "AMD Radeon RX 580")
        ]
        gpu_vendor, gpu_renderer = random.choice(gpus)

        # Platform
        platforms = ["Win32", "MacIntel", "Linux x86_64"]
        platform = random.choice(platforms)

        return HardwareProfile(
            cpu_cores=cpu_cores,
            memory_gb=memory_gb,
            screen_width=screen_width,
            screen_height=screen_height,
            screen_depth=24,
            pixel_ratio=random.choice([1.0, 1.25, 1.5, 2.0]),
            gpu_vendor=gpu_vendor,
            gpu_renderer=gpu_renderer,
            platform=platform,
            architecture="x64"
        )

    def _generate_browser_profile(self, hardware: HardwareProfile, location: GeoLocation) -> BrowserProfile:
        """Generate browser profile consistent with hardware and location"""
        # Select browser
        browser_name = random.choice(['Chrome', 'Firefox', 'Edge'])

        if browser_name == 'Chrome':
            version = random.choice(self.browser_data['chrome_versions'])
            user_agent = f"Mozilla/5.0 ({hardware.platform}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36"
        elif browser_name == 'Firefox':
            version = random.choice(self.browser_data['firefox_versions'])
            user_agent = f"Mozilla/5.0 ({hardware.platform}; rv:{version}) Gecko/20100101 Firefox/{version}"
        else:  # Edge
            version = random.choice(self.browser_data['edge_versions'])
            user_agent = f"Mozilla/5.0 ({hardware.platform}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36 Edg/{version}"

        # Language based on location
        language_map = {
            'US': 'en-US,en;q=0.9',
            'GB': 'en-GB,en;q=0.9',
            'DE': 'de-DE,de;q=0.9,en;q=0.8',
            'CA': 'en-CA,en;q=0.9,fr-CA;q=0.8',
            'AU': 'en-AU,en;q=0.9'
        }
        accept_language = language_map.get(location.country_code, 'en-US,en;q=0.9')

        # Generate consistent fingerprints
        canvas_fingerprint = hashlib.sha256(
            f"{user_agent}{hardware.gpu_renderer}{hardware.screen_width}".encode()
        ).hexdigest()[:16]

        webgl_fingerprint = hashlib.sha256(
            f"{hardware.gpu_vendor}{hardware.gpu_renderer}".encode()
        ).hexdigest()[:16]

        audio_fingerprint = hashlib.sha256(
            f"{hardware.platform}{hardware.cpu_cores}".encode()
        ).hexdigest()[:16]

        return BrowserProfile(
            name=browser_name,
            version=version,
            user_agent=user_agent,
            accept_language=accept_language,
            accept_encoding='gzip, deflate, br',
            accept_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': accept_language,
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            },
            plugins=random.sample(self.browser_data['common_plugins'], k=random.randint(3, 5)),
            fonts=random.sample(self.browser_data['common_fonts'], k=random.randint(8, 10)),
            canvas_fingerprint=canvas_fingerprint,
            webgl_fingerprint=webgl_fingerprint,
            audio_fingerprint=audio_fingerprint
        )

    def _generate_behavioral_pattern(self, age_range: str, occupation: str) -> BehavioralPattern:
        """Generate realistic behavioral patterns based on demographics"""
        # Active hours based on age and occupation
        if 'student' in occupation:
            active_hours = list(range(10, 24))  # Students active late
        elif 'engineer' in occupation or 'developer' in occupation:
            active_hours = list(range(9, 23))  # Tech workers flexible hours
        else:
            active_hours = list(range(8, 22))  # Standard work hours

        # Browsing speed varies by age
        if '18-25' in age_range or '26-35' in age_range:
            browsing_speed = random.uniform(3.0, 6.0)  # Faster
            typing_speed = random.uniform(60, 90)
        else:
            browsing_speed = random.uniform(1.5, 3.5)  # Slower
            typing_speed = random.uniform(40, 65)

        return BehavioralPattern(
            active_hours=active_hours,
            browsing_speed=browsing_speed,
            scroll_patterns={
                'avg_scroll_depth': random.uniform(0.6, 0.9),
                'scroll_speed': random.uniform(100, 300),
                'pause_frequency': random.uniform(0.3, 0.7)
            },
            click_patterns={
                'double_click_speed': random.uniform(200, 400),
                'click_accuracy': random.uniform(0.85, 0.98),
                'hover_time': random.uniform(0.5, 2.0)
            },
            typing_speed=typing_speed,
            pause_patterns=[random.uniform(0.5, 3.0) for _ in range(10)],
            session_duration=(random.randint(15, 45), random.randint(60, 180))
        )

    def _generate_interests(self, age_range: str, occupation: str) -> InterestProfile:
        """Generate realistic interests based on demographics"""
        # Base categories
        all_categories = {
            'technology': ['tech_news', 'gadgets', 'software', 'gaming'],
            'news': ['world_news', 'local_news', 'politics', 'business'],
            'entertainment': ['movies', 'tv_shows', 'music', 'books'],
            'social': ['facebook', 'twitter', 'instagram', 'linkedin'],
            'shopping': ['amazon', 'ebay', 'clothing', 'electronics'],
            'education': ['online_courses', 'tutorials', 'research', 'documentation'],
            'lifestyle': ['health', 'fitness', 'cooking', 'travel']
        }

        # Select categories based on demographics
        selected_categories = []
        if '18-25' in age_range or '26-35' in age_range:
            selected_categories.extend(['technology', 'entertainment', 'social'])
        if 'engineer' in occupation or 'developer' in occupation:
            selected_categories.extend(['technology', 'education'])
        if 'student' in occupation:
            selected_categories.extend(['education', 'entertainment', 'social'])

        # Ensure at least 3 categories
        while len(selected_categories) < 3:
            selected_categories.append(random.choice(list(all_categories.keys())))

        # Generate specific interests
        websites = []
        search_terms = []
        for category in set(selected_categories):
            websites.extend(random.sample(all_categories[category], k=min(2, len(all_categories[category]))))
            search_terms.extend([f"{item} tutorial" for item in random.sample(all_categories[category], k=1)])

        return InterestProfile(
            categories=list(set(selected_categories)),
            websites=websites[:10],
            search_terms=search_terms[:15],
            social_platforms=random.sample(['facebook', 'twitter', 'instagram', 'linkedin', 'reddit'], k=random.randint(2, 4)),
            shopping_preferences=random.sample(['electronics', 'clothing', 'books', 'home', 'sports'], k=random.randint(2, 4)),
            news_sources=random.sample(['cnn', 'bbc', 'reuters', 'techcrunch', 'hackernews'], k=random.randint(2, 3)),
            entertainment=random.sample(['netflix', 'youtube', 'spotify', 'twitch', 'hulu'], k=random.randint(2, 4))
        )


class ProfileEvolutionEngine:
    """Manages gradual evolution of profiles over time"""

    def __init__(self, db: ProfileDatabase):
        self.db = db

    def should_evolve(self, profile: UserProfile) -> bool:
        """Determine if profile should evolve based on time elapsed"""
        days_since_evolution = (datetime.now() - profile.last_evolution).days
        # Evolve every 30-90 days
        return days_since_evolution > random.randint(30, 90)

    def evolve_profile(self, profile: UserProfile) -> UserProfile:
        """Gradually evolve profile to simulate natural changes"""
        changes = []

        # Evolve interests (add/remove some)
        if random.random() < 0.3:
            new_interest = random.choice(['cooking', 'photography', 'gardening', 'diy', 'podcasts'])
            if new_interest not in profile.interests.categories:
                profile.interests.categories.append(new_interest)
                changes.append(f"Added interest: {new_interest}")

        # Evolve browsing patterns slightly
        if random.random() < 0.2:
            profile.behavior.browsing_speed *= random.uniform(0.95, 1.05)
            changes.append("Adjusted browsing speed")

        # Add to browsing history
        if random.random() < 0.5:
            new_sites = random.sample(profile.interests.websites, k=min(3, len(profile.interests.websites)))
            for site in new_sites:
                profile.browsing_history.append({
                    'url': f"https://{site}.com",
                    'timestamp': datetime.now().isoformat(),
                    'duration': random.randint(30, 300)
                })
            changes.append(f"Added {len(new_sites)} browsing history entries")

        # Update evolution tracking
        profile.last_evolution = datetime.now()
        profile.evolution_log.append({
            'date': datetime.now().isoformat(),
            'changes': changes,
            'reason': 'natural_evolution'
        })

        logger.info(f"Profile {profile.profile_name} evolved: {', '.join(changes)}")
        return profile

    async def auto_evolve_profiles(self):
        """Automatically evolve all profiles that need it"""
        profiles = self.db.list_profiles()
        for profile_info in profiles:
            if profile_info['is_active']:
                profile = self.db.load_profile(profile_info['profile_id'])
                if profile and self.should_evolve(profile):
                    evolved_profile = self.evolve_profile(profile)
                    self.db.save_profile(evolved_profile)
                    await asyncio.sleep(0.1)  # Small delay between evolutions


class OperationMode:
    """Operation mode enumeration"""
    PROFILE = "profile"  # Persistent identity mode
    STEALTH = "stealth"  # Dynamic randomization mode
    HEADLESS = "headless"  # Automated headless mode
    TESTING = "testing"  # Testing mode


class DualModeManager:
    """Manages switching between Profile and Stealth modes"""

    def __init__(self, db: ProfileDatabase, generator: ProfileGenerator):
        self.db = db
        self.generator = generator
        self.current_mode = OperationMode.PROFILE
        self.active_profile: Optional[UserProfile] = None
        self.stealth_config: Dict[str, Any] = {}

    def set_mode(self, mode: str, profile_id: Optional[str] = None) -> bool:
        """Switch operation mode"""
        try:
            if mode == OperationMode.PROFILE:
                if profile_id:
                    self.active_profile = self.db.load_profile(profile_id)
                    if not self.active_profile:
                        logger.error(f"Profile {profile_id} not found")
                        return False
                    self.current_mode = OperationMode.PROFILE
                    logger.info(f"Switched to PROFILE mode with profile: {self.active_profile.profile_name}")
                    return True
                else:
                    logger.error("Profile ID required for PROFILE mode")
                    return False

            elif mode in [OperationMode.STEALTH, OperationMode.HEADLESS, OperationMode.TESTING]:
                self.current_mode = mode
                self.active_profile = None
                logger.info(f"Switched to {mode.upper()} mode")
                return True

            else:
                logger.error(f"Invalid mode: {mode}")
                return False

        except Exception as e:
            logger.error(f"Failed to switch mode: {e}")
            traceback.print_exc()
            return False

    def get_fingerprint(self) -> Dict[str, Any]:
        """Get fingerprint based on current mode"""
        if self.current_mode == OperationMode.PROFILE and self.active_profile:
            # Return persistent fingerprint from profile
            return self._get_profile_fingerprint()
        else:
            # Return randomized fingerprint
            return self._get_random_fingerprint()

    def _get_profile_fingerprint(self) -> Dict[str, Any]:
        """Get consistent fingerprint from active profile"""
        if not self.active_profile:
            return {}

        profile = self.active_profile
        return {
            'user_agent': profile.browser.user_agent,
            'platform': profile.hardware.platform,
            'language': profile.browser.accept_language,
            'timezone': profile.location.timezone,
            'screen_resolution': f"{profile.hardware.screen_width}x{profile.hardware.screen_height}",
            'hardware_concurrency': profile.hardware.cpu_cores,
            'device_memory': profile.hardware.memory_gb,
            'screen_depth': profile.hardware.screen_depth,
            'pixel_ratio': profile.hardware.pixel_ratio,
            'gpu_vendor': profile.hardware.gpu_vendor,
            'gpu_renderer': profile.hardware.gpu_renderer,
            'fonts': profile.browser.fonts,
            'plugins': profile.browser.plugins,
            'canvas_fingerprint': profile.browser.canvas_fingerprint,
            'webgl_fingerprint': profile.browser.webgl_fingerprint,
            'audio_fingerprint': profile.browser.audio_fingerprint,
            'accept_headers': profile.browser.accept_headers,
            'cookies': profile.cookies,
            'local_storage': profile.local_storage
        }

    def _get_random_fingerprint(self) -> Dict[str, Any]:
        """Generate randomized fingerprint for stealth mode"""
        # Generate temporary profile for randomization
        temp_profile = self.generator.generate_profile(
            profile_name=f"temp_{uuid.uuid4().hex[:8]}",
            location_preference=None
        )

        # Return fingerprint but don't save profile
        return {
            'user_agent': temp_profile.browser.user_agent,
            'platform': temp_profile.hardware.platform,
            'language': temp_profile.browser.accept_language,
            'timezone': temp_profile.location.timezone,
            'screen_resolution': f"{temp_profile.hardware.screen_width}x{temp_profile.hardware.screen_height}",
            'hardware_concurrency': temp_profile.hardware.cpu_cores,
            'device_memory': temp_profile.hardware.memory_gb,
            'screen_depth': temp_profile.hardware.screen_depth,
            'pixel_ratio': temp_profile.hardware.pixel_ratio,
            'gpu_vendor': temp_profile.hardware.gpu_vendor,
            'gpu_renderer': temp_profile.hardware.gpu_renderer,
            'fonts': temp_profile.browser.fonts,
            'plugins': temp_profile.browser.plugins,
            'canvas_fingerprint': temp_profile.browser.canvas_fingerprint,
            'webgl_fingerprint': temp_profile.browser.webgl_fingerprint,
            'audio_fingerprint': temp_profile.browser.audio_fingerprint,
            'accept_headers': temp_profile.browser.accept_headers
        }

    def should_randomize(self, context: str) -> bool:
        """Determine if randomization should be used based on context"""
        # Always randomize in stealth/headless/testing modes
        if self.current_mode != OperationMode.PROFILE:
            return True

        # Check for detection indicators
        detection_keywords = ['captcha', 'bot', 'automated', 'suspicious', 'blocked']
        if any(keyword in context.lower() for keyword in detection_keywords):
            logger.warning(f"Detection suspected in context: {context}")
            return True

        return False

    def update_profile_usage(self):
        """Update profile last used timestamp"""
        if self.active_profile and self.current_mode == OperationMode.PROFILE:
            self.active_profile.last_used = datetime.now()
            self.db.save_profile(self.active_profile)
