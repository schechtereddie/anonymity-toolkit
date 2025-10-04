#!/usr/bin/env python3
"""
Test script for the Enhanced Ultimate Anonymity Toolkit
Tests all new components and functionality
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported"""
    try:
        from core.profile_fingerprint import ProfileFingerprintManager, BrowserFingerprint
        from core.browser_user import UserStealthBrowser
        from core.status_banner import StatusBanner
        print("✅ All core modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_fingerprint_manager():
    """Test the fingerprint manager"""
    try:
        from core.profile_fingerprint import ProfileFingerprintManager

        manager = ProfileFingerprintManager()

        # Test profile data
        profile_data = {
            'profile_name': 'test_profile',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'screen_resolution': '1920x1080',
            'language': 'en-US,en;q=0.9',
            'timezone': 'America/New_York'
        }

        # Generate fingerprint
        fingerprint = manager.generate_fingerprint(profile_data)
        score = manager.get_fingerprint_score(fingerprint, profile_data)

        print(f"✅ Fingerprint generated successfully (Score: {score}/100)")
        print(f"   User Agent: {fingerprint.user_agent[:50]}...")
        print(f"   Platform: {fingerprint.platform}")
        print(f"   Language: {fingerprint.language}")

        return True

    except Exception as e:
        print(f"❌ Fingerprint manager test failed: {e}")
        return False

def test_status_banner():
    """Test the status banner component"""
    try:
        from core.status_banner import StatusBanner

        # Create a test window
        test_window = tk.Tk()
        test_window.title("Status Banner Test")
        test_window.geometry("600x100")

        # Create status banner
        banner = StatusBanner(test_window)

        # Test status update
        test_status = {
            'anonymity_score': 85,
            'profile_name': 'test_profile',
            'proxy_status': 'Connected',
            'cookie_count': 150,
            'browser_sessions': 1,
            'system_health': 'Good'
        }

        banner.update_status(test_status)
        print("✅ Status banner created and updated successfully")

        # Close test window after 2 seconds
        test_window.after(2000, test_window.destroy)

        return True

    except Exception as e:
        print(f"❌ Status banner test failed: {e}")
        return False

def test_user_browser():
    """Test the user browser component"""
    try:
        from core.browser_user import UserStealthBrowser

        browser = UserStealthBrowser()

        # Test browser detection
        supported_browsers = browser._get_supported_browsers()
        print("✅ Browser detection completed:")
        for browser, available in supported_browsers.items():
            status = "Available" if available else "Not Installed"
            print(f"   {browser}: {status}")

        # Test system resources
        resources = browser._get_system_resources()
        print("✅ System resources checked:")
        print(f"   Memory: {resources.get('memory_available_gb', 'N/A')}GB available")
        print(f"   CPU: {resources.get('cpu_percent', 'N/A')}%")

        return True

    except Exception as e:
        print(f"❌ User browser test failed: {e}")
        return False

def test_enhanced_gui():
    """Test the enhanced GUI (basic initialization)"""
    try:
        from core.enhanced_gui import EnhancedAnonymityGUI

        # Create test window
        test_window = tk.Tk()
        test_window.title("Enhanced GUI Test")
        test_window.geometry("400x300")

        # Create enhanced GUI
        gui = EnhancedAnonymityGUI(test_window)

        print("✅ Enhanced GUI initialized successfully")
        print(f"   Components: {len(gui.status_components)} status components")
        print(f"   Fingerprint Manager: {'Available' if gui.fingerprint_manager else 'Not Available'}")
        print(f"   User Browser: {'Available' if gui.user_browser else 'Not Available'}")

        # Close after 3 seconds
        test_window.after(3000, test_window.destroy)

        return True

    except Exception as e:
        print(f"❌ Enhanced GUI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Enhanced Ultimate Anonymity Toolkit v6.0")
    print("=" * 60)

    tests = [
        ("Import Test", test_imports),
        ("Fingerprint Manager Test", test_fingerprint_manager),
        ("Status Banner Test", test_status_banner),
        ("User Browser Test", test_user_browser),
        ("Enhanced GUI Test", test_enhanced_gui)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        if test_func():
            passed += 1

    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Enhanced system is ready.")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
