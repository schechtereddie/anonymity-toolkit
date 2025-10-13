#!/usr/bin/env python3
"""
False Profile Manager - Persistent Anonymous Identities
Coordinates all fingerprinting countermeasures under unified false identities
"""

import os
import json
import random
import hashlib
import uuid
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path

from .webgl_fingerprint_manager import WebGLFingerprintManager, WebGLProfile
from .canvas_ml_protector import CanvasFingerprintProtector, CanvasFingerprint


@dataclass
class FalseProfile:
    """Complete false identity with all fingerprinting components"""
    profile_id: str
    name: str  # Human-readable identifier like "TechWorker_Alpha"
    category: str  # "professional", "student", "casual_user", etc.

    # Core Fingerprinting Data
    user_agent: str
    screen_resolution: str
    timezone: str
    language: str
    webgl_profile: WebGLProfile
    hardware_concurrency: int
    device_memory: int

    # Behavioral Profile
    browsing_style: str  # "focused", "casual", "technical", "social"
    activity_times: List[str]  # Preferred times of day
    session_duration: Tuple[int, int]  # Min/max session length in minutes

    # Usage Statistics
    sessions_used: int = 0
    last_used: Optional[datetime] = None
    created_at: datetime = None
    detections_encountered: int = 0

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        # Convert datetime objects
        if self.last_used:
            data['last_used'] = self.last_used.isoformat()
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FalseProfile':
        """Create from dictionary"""
        # Convert datetime strings back
        if data.get('last_used'):
            data['last_used'] = datetime.fromisoformat(data['last_used'])
        if data.get('created_at'):
            data['created_at'] = datetime.fromisoformat(data['created_at'])

        return cls(**data)


class FalseProfileManager:
    """
    Master coordinator for persistent false identities.
    Manages complete anonymous personas with consistent fingerprints across sessions.
    """

    def __init__(self):
        self.profiles_directory = "src/data/false_profiles"
        os.makedirs(self.profiles_directory, exist_ok=True)

        # Initialize sub-managers
        self.webgl_manager = WebGLFingerprintManager()
        self.canvas_protector = CanvasFingerprintProtector()

        # Profile storage
        self.profiles: Dict[str, FalseProfile] = {}
        self.active_profiles: Dict[str, Dict[str, Any]] = {}  # profile_id -> session_data

        # Load existing profiles
        self._load_profiles()

        # Profile categories with behavioral templates
        self.category_templates = self._initialize_category_templates()

    def _initialize_category_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize behavioral templates for different profile categories"""
        return {
            'professional': {
                'browsing_style': 'focused',
                'user_agents': [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ],
                'screen_resolutions': ['1920x1080', '2560x1440', '3440x1440'],
                'timezones': ['America/New_York', 'Europe/London', 'America/Los_Angeles'],
                'languages': ['en-US,en;q=0.9', 'en-GB,en;q=0.8'],
                'hardware_profiles': ['high_end', 'high_end', 'mid_range'],  # Weighted
                'session_durations': [(15, 120), (30, 240), (45, 300)],  # Minutes
                'activity_times': ['09:00-12:00', '13:00-17:00', '18:00-20:00']
            },
            'student': {
                'browsing_style': 'casual',
                'user_agents': [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
                ],
                'screen_resolutions': ['1920x1080', '1366x768', '2560x1600'],
                'timezones': ['America/New_York', 'Europe/Berlin', 'America/Chicago', 'Europe/London'],
                'languages': ['en-US,en;q=0.9', 'en,en-US;q=0.8,en;q=0.7'],
                'hardware_profiles': ['mid_range', 'entry_level', 'mid_range'],  # More modest hardware
                'session_durations': [(5, 90), (10, 180), (15, 240)],
                'activity_times': ['08:00-11:00', '12:00-15:00', '17:00-22:00', '00:00-03:00']
            },
            'casual_user': {
                'browsing_style': 'social',
                'user_agents': [
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
                    'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/113.0 Firefox/113.0',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
                ],
                'screen_resolutions': ['414x896', '428x926', '1920x1080', '1366x768'],
                'timezones': ['America/New_York', 'Europe/London', 'America/Los_Angeles', 'America/Denver'],
                'languages': ['en-US,en;q=0.9', 'en,en-US;q=0.8,en;q=0.7'],
                'hardware_profiles': ['mid_range', 'entry_level', 'mid_range'],
                'session_durations': [(2, 45), (5, 90), (10, 120)],
                'activity_times': ['07:00-09:00', '11:00-13:00', '18:00-23:00', '00:00-02:00']
            },
            'technical_user': {
                'browsing_style': 'technical',
                'user_agents': [
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'
                ],
                'screen_resolutions': ['2560x1440', '3440x1440', '1920x1080', '3840x2160'],
                'timezones': ['America/Los_Angeles', 'Europe/Berlin', 'America/New_York', 'Asia/Tokyo'],
                'languages': ['en-US,en;q=0.9', 'en,en-US;q=0.8,en;q=0.7'],
                'hardware_profiles': ['high_end', 'high_end', 'mid_range'],
                'session_durations': [(20, 180), (30, 300), (45, 480)],
                'activity_times': ['08:00-12:00', '13:00-18:00', '20:00-23:00']
            }
        }

    def _load_profiles(self):
        """Load existing false profiles from disk"""
        profiles_path = os.path.join(self.profiles_directory, "profiles.json")
        if os.path.exists(profiles_path):
            try:
                with open(profiles_path, 'r') as f:
                    profiles_data = json.load(f)

                for profile_id, profile_data in profiles_data.items():
                    self.profiles[profile_id] = FalseProfile.from_dict(profile_data)

                print(f"✅ Loaded {len(self.profiles)} existing false profiles")
            except Exception as e:
                print(f"⚠️ Error loading profiles: {e}")

    def save_profiles(self):
        """Save all profiles to disk"""
        profiles_path = os.path.join(self.profiles_directory, "profiles.json")

        # Convert profiles to dictionaries
        profiles_data = {}
        for profile_id, profile in self.profiles.items():
            profiles_data[profile_id] = profile.to_dict()

        try:
            with open(profiles_path, 'w') as f:
                json.dump(profiles_data, f, indent=2, default=str)

            print(f"💾 Saved {len(self.profiles)} false profiles")
        except Exception as e:
            print(f"❌ Error saving profiles: {e}")

    def generate_false_profile(self, name: str, category: str,
                             custom_attributes: Optional[Dict[str, Any]] = None) -> FalseProfile:
        """
        Generate a complete false identity with consistent fingerprinting across all vectors
        """
        if category not in self.category_templates:
            raise ValueError(f"Unknown category: {category}. Available: {list(self.category_templates.keys())}")

        template = self.category_templates[category]

        # Generate unique profile ID
        profile_id = str(uuid.uuid4())[:8]

        # Select attributes from template
        user_agent = random.choice(template['user_agents'])
        screen_resolution = random.choice(template['screen_resolutions'])
        timezone = random.choice(template['timezones'])
        language = random.choice(template['languages'])
        activity_times = random.sample(template['activity_times'], random.randint(2, 4))

        # Generate consistent fingerprinting profile
        system_characteristics = {
            'cpu_brand': self._extract_cpu_from_user_agent(user_agent),
            'ram_gb': self._guess_ram_from_hardware_profile(random.choice(template['hardware_profiles']))
        }

        webgl_profile = self.webgl_manager.generate_webgl_profile(system_characteristics, profile_id)
        hardware_concurrency = self._generate_hardware_concurrency(template['hardware_profiles'])
        device_memory = self._guess_device_memory(profile_id, template['hardware_profiles'])

        # Create the complete false profile
        profile = FalseProfile(
            profile_id=profile_id,
            name=name,
            category=category,
            user_agent=user_agent,
            screen_resolution=screen_resolution,
            timezone=timezone,
            language=language,
            webgl_profile=webgl_profile,
            hardware_concurrency=hardware_concurrency,
            device_memory=device_memory,
            browsing_style=template['browsing_style'],
            activity_times=activity_times,
            session_duration=random.choice(template['session_durations'])
        )

        # Apply custom attributes if provided
        if custom_attributes:
            for attr, value in custom_attributes.items():
                if hasattr(profile, attr):
                    setattr(profile, attr, value)

        # Store the profile
        self.profiles[profile_id] = profile
        self.save_profiles()

        print(f"🎭 Created false profile '{name}' ({category}) with ID: {profile_id}")
        return profile

    def _extract_cpu_from_user_agent(self, ua: str) -> str:
        """Extract CPU architecture hint from user agent"""
        ua_lower = ua.lower()
        if 'intel' in ua_lower or 'windows' in ua_lower:
            return 'intel_i7'  # Default decent Intel
        elif 'mac' in ua_lower:
            return 'intel_i7'  # Apple Silicon might not be in UA
        elif 'linux' in ua_lower:
            return 'amd_ryzen7'  # Common on Linux
        else:
            return 'default'

    def _guess_ram_from_hardware_profile(self, hardware_profile: str) -> int:
        """Guess RAM amount based on hardware profile"""
        if hardware_profile == 'high_end':
            return random.choice([32, 64, 128])
        elif hardware_profile == 'mid_range':
            return random.choice([16, 32])
        else:  # entry_level
            return random.choice([8, 16])

    def _generate_hardware_concurrency(self, hardware_profiles: List[str]) -> int:
        """Generate hardware concurrency based on profile type"""
        profile = random.choice(hardware_profiles)
        if profile == 'high_end':
            return random.choice([16, 20, 24, 32])
        elif profile == 'mid_range':
            return random.choice([6, 8, 12])
        else:  # entry_level
            return random.choice([2, 4, 6])

    def _guess_device_memory(self, profile_id: str, hardware_profiles: List[str]) -> int:
        """Guess device memory (deterministically based on profile)"""
        # Use profile ID for consistent results
        hash_val = int(hashlib.md5(profile_id.encode()).hexdigest(), 16)
        profile = hardware_profiles[hash_val % len(hardware_profiles)]

        if profile == 'high_end':
            return random.choice([16, 32, 64])
        elif profile == 'mid_range':
            return random.choice([8, 16])
        else:  # entry_level
            return random.choice([4, 8])

    def activate_profile(self, profile_id: str, browser_session) -> Dict[str, Any]:
        """
        Activate a false profile in a browser session
        Applies all fingerprinting countermeasures consistently
        """
        if profile_id not in self.profiles:
            raise ValueError(f"Profile {profile_id} not found")

        profile = self.profiles[profile_id]

        print(f"🎭 Activating false profile: {profile.name} ({profile.category})")

        # Apply browser fingerprinting
        self._apply_browser_fingerprinting(profile, browser_session)

        # Apply WebGL fingerprinting
        self._apply_webgl_fingerprinting(profile, browser_session)

        # Apply canvas protection (个性化 based on profile)
        self._apply_canvas_protection(profile, browser_session)

        # Update profile statistics
        profile.sessions_used += 1
        profile.last_used = datetime.now()
        self.save_profiles()

        # Store active session data
        session_data = {
            'profile': profile,
            'activated_at': datetime.now(),
            'browser_session': browser_session,
            'fingerprinting_applied': True
        }

        self.active_profiles[profile_id] = session_data

        print(f"✅ False profile '{profile.name}' activated successfully")
        return session_data

    def _apply_browser_fingerprinting(self, profile: FalseProfile, browser_session):
        """Apply browser-level fingerprinting to match profile"""
        browser_options = [
            # User agent
            '--user-agent=' + profile.user_agent,

            # Language
            '--lang=' + profile.language,

            # Screen resolution (approximated)
            '--window-size=1920,1080',  # Could be made profile-specific

            # Disable automation indicators
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor'
        ]

        # Apply options to browser session
        browser_session.set_browser_options(browser_options)
        browser_session.set_timezone(profile.timezone)

    def _apply_webgl_fingerprinting(self, profile: FalseProfile, browser_session):
        """Apply WebGL fingerprinting to match profile"""
        self.webgl_manager.inject_webgl_protection(browser_session)

    def _apply_canvas_protection(self, profile: FalseProfile, browser_session):
        """Apply canvas protection based on profile characteristics"""
        # Create countermeasures based on profile browsing style
        if profile.browsing_style == 'technical':
            # Technical users might expect canvas operations for code editors, etc.
            countermeasures = {
                'technique': 'selective_canvas_protection',
                'noise_injection': False,  # Don't break technical tools
                'font_substitution': True,
                'timing_jitter': True,
                'affected_operations': ['fillText', 'measureText']
            }
        elif profile.browsing_style == 'social':
            # Social users expect chat, etc.
            countermeasures = {
                'technique': 'aggressive_canvas_protection',
                'noise_injection': True,
                'font_substitution': True,
                'timing_jitter': True,
                'affected_operations': ['getImageData', 'fillText', 'fillRect']
            }
        else:  # casual/professional
            countermeasures = {
                'technique': 'balanced_canvas_protection',
                'noise_injection': True,
                'font_substitution': True,
                'timing_jitter': True,
                'affected_operations': ['getImageData']
            }

        self.canvas_protector.apply_canvas_protection(browser_session, countermeasures)

    def list_profiles(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all available false profiles"""
        profiles_list = []

        for profile_id, profile in self.profiles.items():
            if category and profile.category != category:
                continue

            profiles_list.append({
                'id': profile_id,
                'name': profile.name,
                'category': profile.category,
                'browsing_style': profile.browsing_style,
                'sessions_used': profile.sessions_used,
                'last_used': profile.last_used.isoformat() if profile.last_used else None,
                'created_at': profile.created_at.isoformat(),
                'detections_encountered': profile.detections_encountered
            })

        return sorted(profiles_list, key=lambda x: x['last_used'] or '2000-01-01', reverse=True)

    def get_profile(self, profile_id: str) -> Optional[FalseProfile]:
        """Get a specific profile by ID"""
        return self.profiles.get(profile_id)

    def delete_profile(self, profile_id: str) -> bool:
        """Delete a false profile"""
        if profile_id in self.profiles:
            del self.profiles[profile_id]
            self.save_profiles()
            print(f"🗑️ Deleted false profile: {profile_id}")
            return True

        return False

    def generate_profile_batch(self, category: str, count: int = 5) -> List[FalseProfile]:
        """Generate a batch of profiles for the same category"""
        profiles = []

        for i in range(count):
            adjectives = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Silent', 'Shadow', 'Ghost']
            names = ['User', 'Agent', 'Identity', 'Persona', 'Profile']

            name = f"{random.choice(adjectives)}_{random.choice(names)}_{i+1}"
            profile = self.generate_false_profile(name, category)
            profiles.append(profile)

        print(f"🎭 Generated {count} {category} profiles")
        return profiles

    def get_profile_recommendations(self, target_scenario: str,
                                  risk_level: str = 'medium') -> List[FalseProfile]:
        """
        Recommend profiles based on target scenario and risk level
        """
        recommendations = []

        scenario_mappings = {
            'linkedin_job_search': ['professional', 'technical_user'],
            'social_media_engagement': ['casual_user', 'student'],
            'ecommerce_shopping': ['casual_user', 'professional'],
            'research_academia': ['technical_user', 'student'],
            'corporate_investigation': ['professional', 'technical_user'],
            'social_engineering': ['casual_user', 'student']
        }

        suitable_categories = scenario_mappings.get(target_scenario, ['professional'])

        # Filter profiles by category and usage (prefer less-used profiles for new scenarios)
        suitable_profiles = [
            profile for profile in self.profiles.values()
            if profile.category in suitable_categories and profile.detections_encountered <= 2
        ]

        # Sort by usage frequency (prefer less-used profiles for better anonymity)
        suitable_profiles.sort(key=lambda p: (p.sessions_used, p.detections_encountered))

        return suitable_profiles[:5]  # Return top 5 recommendations

    def record_detection_event(self, profile_id: str, detection_type: str):
        """Record a detection event for a profile"""
        if profile_id in self.profiles:
            profile = self.profiles[profile_id]
            profile.detections_encountered += 1
            self.save_profiles()

            risk_level = 'low' if profile.detections_encountered <= 1 else 'medium' if profile.detections_encountered <= 3 else 'high'

            print(f"⚠️ Detection recorded for profile '{profile.name}': {detection_type}")
            print(f"   Risk level: {risk_level} ({profile.detections_encountered} total detections)")

            if profile.detections_encountered >= 5:
                print("   ⚠️ High-risk profile - consider retirement")

    def get_profile_health_report(self) -> Dict[str, Any]:
        """Generate a health report for all profiles"""
        total_profiles = len(self.profiles)
        active_profiles = len(self.active_profiles)

        # Calculate statistics
        categories = {}
        risky_profiles = 0

        for profile in self.profiles.values():
            # Category statistics
            cat = profile.category
            if cat not in categories:
                categories[cat] = {
                    'count': 0,
                    'total_sessions': 0,
                    'avg_detections': 0.0,
                    'risky_count': 0
                }

            categories[cat]['count'] += 1
            categories[cat]['total_sessions'] += profile.sessions_used
            categories[cat]['avg_detections'] += profile.detections_encountered

            if profile.detections_encountered >= 3:
                categories[cat]['risky_count'] += 1
                risky_profiles += 1

        # Finalize averages
        for cat_data in categories.values():
            if cat_data['count'] > 0:
                cat_data['avg_detections'] = cat_data['avg_detections'] / cat_data['count']

        return {
            'total_profiles': total_profiles,
            'active_profiles': active_profiles,
            'risky_profiles': risky_profiles,
            'categories': categories,
            'generated_at': datetime.now().isoformat(),
            'health_score': self._calculate_health_score(total_profiles, risky_profiles)
        }

    def _calculate_health_score(self, total_profiles: int, risky_profiles: int) -> float:
        """Calculate overall profile health score (0-100)"""
        if total_profiles == 0:
            return 0.0

        # Base score from profile diversity minus risk factor
        diversity_score = min(100, total_profiles * 10)  # Max at 10 profiles
        risk_penalty = (risky_profiles / total_profiles) * 100

        health_score = diversity_score - risk_penalty
        return max(0.0, min(100.0, health_score))

    def cleanup_retired_profiles(self, max_detections: int = 10, max_age_days: int = 365):
        """Clean up profiles that have become too risky or old"""
        current_time = datetime.now()
        retired_profiles = []

        for profile_id, profile in list(self.profiles.items()):
            # Check detection threshold
            if profile.detections_encountered >= max_detections:
                retired_profiles.append(('high_risk', profile_id, profile.name))

            # Check age threshold
            elif profile.created_at and (current_time - profile.created_at).days > max_age_days:
                retired_profiles.append(('expired', profile_id, profile.name))

        # Remove retired profiles
        for reason, profile_id, name in retired_profiles:
            del self.profiles[profile_id]
            print(f"🏁 Retired profile '{name}' ({profile_id}): {reason}")

        if retired_profiles:
            self.save_profiles()
            print(f"🧹 Cleaned up {len(retired_profiles)} profiles")

        return retired_profiles

    def export_profile_set(self, profile_ids: List[str], export_path: str):
        """Export a set of profiles for backup or sharing"""
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'profile_count': len(profile_ids),
            'profiles': {}
        }

        for profile_id in profile_ids:
            if profile_id in self.profiles:
                export_data['profiles'][profile_id] = self.profiles[profile_id].to_dict()

        try:
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)

            print(f"📤 Exported {len(profile_ids)} profiles to {export_path}")

        except Exception as e:
            print(f"❌ Export failed: {e}")
