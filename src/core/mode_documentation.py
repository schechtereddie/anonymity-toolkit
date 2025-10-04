#!/usr/bin/env python3
"""
In-App Documentation and Help System for Dual-Mode Operation
Provides clear explanations and guidance to users
"""

import webbrowser
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class ModeDocumentation:
    """Documentation for operation modes"""
    
    PROFILE_MODE_TITLE = "👤 PROFILE MODE - Persistent Identity"
    PROFILE_MODE_SHORT = "Maintain consistent identity across sessions"
    PROFILE_MODE_DESCRIPTION = """
🎯 PROFILE MODE - When to Use:

✅ Normal web browsing as a believable user
✅ Creating and maintaining long-term accounts
✅ Social media, shopping, research
✅ Building trust and reputation on platforms
✅ Appearing as a real, returning user

🔑 How It Works:
• Your digital fingerprint stays EXACTLY THE SAME every session
• Cookies, browsing history, and preferences persist
• All data points remain consistent (browser, hardware, location)
• Profile gradually evolves over time like a real person
• Websites see you as a legitimate, long-term user

📊 Example:
Monday: Login as "John_Tech_Worker"
  - Canvas fingerprint: abc123
  - Location: New York
  - Browsing: Tech news, GitHub

Friday: Login as "John_Tech_Worker" again
  - Canvas fingerprint: abc123 (SAME!)
  - Location: New York (SAME!)
  - Cookies from Monday still present
  - History continues from Monday

⚠️ Important:
• Use the SAME profile for the SAME website/account
• Don't switch profiles mid-session
• Profile data is saved permanently
• Perfect for long-term anonymity with believability
"""

    STEALTH_MODE_TITLE = "🎭 STEALTH MODE - Dynamic Randomization"
    STEALTH_MODE_SHORT = "New random identity every session"
    STEALTH_MODE_DESCRIPTION = """
🎯 STEALTH MODE - When to Use:

✅ Web scraping and automation
✅ One-time anonymous browsing
✅ Bypassing aggressive bot detection
✅ Testing different fingerprints
✅ Emergency anonymity situations
✅ Accessing blocked content

🔑 How It Works:
• Every session generates a COMPLETELY NEW fingerprint
• No data persists between sessions
• No cookies, no history, no consistent identity
• You appear as a different user each time
• Maximum anonymity, impossible to track

📊 Example:
Request 1:
  - Canvas fingerprint: xyz789
  - Location: New York
  - Browser: Chrome 120

Request 2 (5 minutes later):
  - Canvas fingerprint: qwe456 (DIFFERENT!)
  - Location: London (DIFFERENT!)
  - Browser: Firefox 121 (DIFFERENT!)

⚠️ Important:
• Cannot maintain long-term accounts
• Websites may show more CAPTCHAs
• Perfect for one-time tasks
• No session continuity
"""

    HEADLESS_MODE_TITLE = "🤖 HEADLESS MODE - Automated Operations"
    HEADLESS_MODE_SHORT = "Optimized for automated browser tasks"
    HEADLESS_MODE_DESCRIPTION = """
🎯 HEADLESS MODE - When to Use:

✅ Automated testing and QA
✅ Batch web scraping operations
✅ Scheduled data collection
✅ Background monitoring tasks
✅ High-volume automated browsing

🔑 How It Works:
• Runs browser without visible window
• Optimized for speed and efficiency
• Random fingerprints for each operation
• No user interaction required
• Perfect for scripts and automation

⚠️ Important:
• No visual feedback during operation
• Check logs for status updates
• Some websites block headless browsers
• Use with caution on protected sites
"""

    TESTING_MODE_TITLE = "🧪 TESTING MODE - Fingerprint Testing"
    TESTING_MODE_SHORT = "Test different fingerprint configurations"
    TESTING_MODE_DESCRIPTION = """
🎯 TESTING MODE - When to Use:

✅ Testing fingerprint detection systems
✅ Comparing different browser configurations
✅ Verifying anonymity effectiveness
✅ Debugging fingerprint issues
✅ Research and development

🔑 How It Works:
• Generate and test multiple fingerprints
• Compare detection results
• Analyze fingerprint uniqueness
• Test different combinations
• Detailed logging and reporting

⚠️ Important:
• For testing purposes only
• May generate unusual fingerprints
• Not recommended for production use
• Use to find optimal configurations
"""

    COMPARISON_TABLE = """
╔══════════════════╦═══════════════╦═══════════════╦═══════════════╗
║ Feature          ║ Profile Mode  ║ Stealth Mode  ║ Headless Mode ║
╠══════════════════╬═══════════════╬═══════════════╬═══════════════╣
║ Fingerprint      ║ Persistent    ║ Random        ║ Random        ║
║ Cookies          ║ Saved         ║ Cleared       ║ Cleared       ║
║ History          ║ Accumulated   ║ None          ║ None          ║
║ Believability    ║ Very High     ║ Low           ║ Low           ║
║ Anonymity        ║ Medium        ║ Very High     ║ Very High     ║
║ Long-term Use    ║ Yes           ║ No            ║ No            ║
║ Automation       ║ No            ║ Possible      ║ Yes           ║
║ Speed            ║ Normal        ║ Normal        ║ Fast          ║
║ Detection Risk   ║ Low           ║ Medium        ║ High          ║
╚══════════════════╩═══════════════╩═══════════════╩═══════════════╝
"""

    QUICK_START_GUIDE = """
🚀 QUICK START GUIDE

1️⃣ CREATE A PROFILE (First Time Setup)
   • Click "Create New Profile"
   • Enter profile name (e.g., "Work_Browsing")
   • Choose location and demographics
   • Save profile

2️⃣ SELECT PROFILE MODE
   • Click "Profile Mode" button
   • Select your saved profile
   • Start browsing normally

3️⃣ WHEN TO SWITCH TO STEALTH MODE
   • Click "Stealth Mode" button
   • Use for one-time anonymous tasks
   • No profile needed

4️⃣ AUTOMATIC DETECTION
   • System auto-switches if threats detected
   • Watch for mode indicator changes
   • Check notifications for alerts

💡 PRO TIPS:
• Create multiple profiles for different purposes
• Use Profile Mode for 90% of browsing
• Switch to Stealth for sensitive one-time tasks
• Let auto-detection handle emergencies
• Review profile evolution monthly
"""

    FAQ = """
❓ FREQUENTLY ASKED QUESTIONS

Q: Which mode should I use for daily browsing?
A: PROFILE MODE - It's more believable and less likely to trigger CAPTCHAs.

Q: Can I switch modes mid-session?
A: Yes, but you'll lose session continuity. Best to plan ahead.

Q: How many profiles should I create?
A: 3-5 profiles for different purposes (work, personal, shopping, etc.)

Q: Will websites know I'm using anonymity tools?
A: In Profile Mode with good profiles, detection is very difficult.
   In Stealth Mode, some advanced systems may detect randomization.

Q: What happens to my data when I delete a profile?
A: All fingerprints, cookies, and history are permanently deleted.

Q: Can I export/import profiles?
A: Yes! Use the Export/Import buttons in Profile Management.

Q: How often do profiles evolve?
A: Automatically every 30-90 days to simulate natural changes.

Q: What if I get detected?
A: System auto-switches to Stealth Mode and alerts you.

Q: Can I use the same profile on multiple devices?
A: Not recommended - fingerprints include hardware specs.

Q: Is my profile data encrypted?
A: Yes, all profile data is encrypted in the database.
"""

    WARNINGS = """
⚠️ IMPORTANT WARNINGS

🔴 DO NOT:
• Use Profile Mode for illegal activities
• Share profiles between multiple people
• Use same profile for conflicting identities
• Ignore detection warnings
• Mix personal info with fake profiles

🟡 BE CAREFUL:
• Some websites ban anonymity tools
• Advanced fingerprinting can detect inconsistencies
• Profile data is sensitive - protect it
• Don't create unrealistic profiles
• Monitor for detection regularly

🟢 BEST PRACTICES:
• Create believable, consistent profiles
• Use Profile Mode for long-term accounts
• Use Stealth Mode for one-time tasks
• Keep profiles updated and evolved
• Review logs and alerts regularly
• Test profiles before important use
• Backup profiles regularly
"""


class HelpSystem:
    """In-app help and documentation system"""
    
    def __init__(self):
        self.docs = ModeDocumentation()
    
    def get_mode_help(self, mode: str) -> str:
        """Get help text for specific mode"""
        help_map = {
            'profile': self.docs.PROFILE_MODE_DESCRIPTION,
            'stealth': self.docs.STEALTH_MODE_DESCRIPTION,
            'headless': self.docs.HEADLESS_MODE_DESCRIPTION,
            'testing': self.docs.TESTING_MODE_DESCRIPTION
        }
        return help_map.get(mode.lower(), "Mode not found")
    
    def get_mode_title(self, mode: str) -> str:
        """Get title for specific mode"""
        title_map = {
            'profile': self.docs.PROFILE_MODE_TITLE,
            'stealth': self.docs.STEALTH_MODE_TITLE,
            'headless': self.docs.HEADLESS_MODE_TITLE,
            'testing': self.docs.TESTING_MODE_TITLE
        }
        return title_map.get(mode.lower(), "Unknown Mode")
    
    def get_mode_short_description(self, mode: str) -> str:
        """Get short description for tooltips"""
        desc_map = {
            'profile': self.docs.PROFILE_MODE_SHORT,
            'stealth': self.docs.STEALTH_MODE_SHORT,
            'headless': self.docs.HEADLESS_MODE_SHORT,
            'testing': self.docs.TESTING_MODE_SHORT
        }
        return desc_map.get(mode.lower(), "")
    
    def get_comparison_table(self) -> str:
        """Get mode comparison table"""
        return self.docs.COMPARISON_TABLE
    
    def get_quick_start(self) -> str:
        """Get quick start guide"""
        return self.docs.QUICK_START_GUIDE
    
    def get_faq(self) -> str:
        """Get FAQ"""
        return self.docs.FAQ
    
    def get_warnings(self) -> str:
        """Get warnings and best practices"""
        return self.docs.WARNINGS
    
    def open_full_documentation(self):
        """Open full documentation in browser"""
        # This would open a local HTML file or online documentation
        doc_path = "file://docs/dual_mode_guide.html"
        try:
            webbrowser.open(doc_path)
        except Exception as e:
            print(f"Could not open documentation: {e}")


# Tooltip texts for UI elements
TOOLTIPS = {
    'profile_mode_button': "👤 Use persistent identity - Same fingerprint every session. Best for normal browsing.",
    'stealth_mode_button': "🎭 Use random identity - New fingerprint each session. Best for one-time tasks.",
    'headless_mode_button': "🤖 Automated mode - Optimized for scripts and automation.",
    'testing_mode_button': "🧪 Testing mode - Test different fingerprint configurations.",
    'create_profile_button': "Create a new persistent profile with believable identity",
    'load_profile_button': "Load an existing profile to continue with same identity",
    'delete_profile_button': "Permanently delete profile and all associated data",
    'evolve_profile_button': "Manually evolve profile to simulate natural changes",
    'export_profile_button': "Export profile data to file for backup",
    'import_profile_button': "Import profile data from backup file",
    'auto_detect_toggle': "Automatically switch to Stealth Mode when threats detected",
    'mode_indicator': "Current operation mode - Click for details",
    'profile_info': "Active profile information - Click to view full details",
    'fingerprint_viewer': "View current browser fingerprint being used",
    'detection_log': "View detection events and mode switches",
}

