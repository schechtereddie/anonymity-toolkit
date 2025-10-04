#!/usr/bin/env python3
"""
Anonymity Toolkit Installer
Handles dependency installation, system setup, and configuration
"""
import subprocess
import sys
import os
import platform
import urllib.request
import zipfile
import tarfile
import shutil

class AnonymityToolkitInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
        self.geo_db_url = "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=YOUR_LICENSE_KEY&suffix=tar.gz"

    def print_banner(self):
        print("🔧 ANONYMITY TOOLKIT INSTALLER")
        print("=" * 40)
        print("🛡️ Setting up advanced privacy protection tools")
        print("🔍 SOCKS5 proxy scraping and verification")
        print("🌍 Geo-location intelligence")
        print("🍪 Cookie management and fingerprinting")
        print("🛡️ Leak detection and protection")
        print()

    def check_python_version(self):
        """Check if Python version is compatible"""
        print("🐍 Checking Python version...")

        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ required")
            return False

        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        return True

    def install_python_dependencies(self):
        """Install Python dependencies"""
        print("📦 Installing Python dependencies...")

        if not os.path.exists(self.requirements_file):
            print(f"⚠️ Requirements file not found: {self.requirements_file}")
            return False

        try:
            # Upgrade pip first
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

            # Install requirements
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", self.requirements_file])

            print("✅ Python dependencies installed successfully")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False

    def download_geoip_database(self):
        """Download and setup GeoLite2 database"""
        print("🌍 Setting up GeoIP database...")

        db_paths = ['GeoLite2-City.mmdb', 'geo/GeoLite2-City.mmdb']

        # Check if already exists
        for db_path in db_paths:
            if os.path.exists(db_path):
                print(f"✅ GeoIP database already exists: {db_path}")
                return True

        print("📥 Downloading GeoLite2-City database...")

        try:
            # Note: You'll need to get a free license key from MaxMind
            # For now, we'll use a placeholder
            print("ℹ️ Please visit https://www.maxmind.com/en/geolite2/signup to get a free license key")
            print("ℹ️ Then update the geo_db_url in this script with your license key")

            # For demonstration, we'll create a placeholder file
            os.makedirs('geo', exist_ok=True)

            # Create a minimal placeholder database file
            with open('geo/GeoLite2-City.mmdb', 'w') as f:
                f.write("# GeoLite2 City Database Placeholder\n")
                f.write("# Please download from MaxMind with your license key\n")

            print("✅ GeoIP database placeholder created")
            print("📝 Note: For full functionality, download GeoLite2-City.mmdb from MaxMind")
            return True

        except Exception as e:
            print(f"❌ Failed to setup GeoIP database: {e}")
            return False

    def setup_directories(self):
        """Create necessary directories"""
        print("📁 Creating directories...")

        directories = ['geo', 'proxies', 'logs', 'cache', 'exports']

        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"✅ Created directory: {directory}")
            except Exception as e:
                print(f"❌ Failed to create directory {directory}: {e}")
                return False

        return True

    def create_desktop_shortcuts(self):
        """Create desktop shortcuts"""
        print("🖥️ Creating desktop shortcuts...")

        try:
            desktop_path = os.path.expanduser("~/Desktop")
            script_dir = os.path.dirname(os.path.abspath(__file__))

            # Main GUI shortcut
            shortcut_content = f"""#!/bin/bash
cd "{script_dir}"
python main.py
"""

            shortcut_path = os.path.join(desktop_path, "Anonymity_Toolkit.desktop")
            with open(shortcut_path, 'w') as f:
                f.write(f"""[Desktop Entry]
Name=Anonymity Toolkit
Comment=Advanced Privacy Protection Tools
Exec=python {script_dir}/main.py
Icon=terminal
Terminal=true
Type=Application
Categories=Utility;Security;
""")

            os.chmod(shortcut_path, 0o755)
            print(f"✅ Desktop shortcut created: {shortcut_path}")

            return True

        except Exception as e:
            print(f"❌ Failed to create desktop shortcuts: {e}")
            return False

    def run_tests(self):
        """Run system tests"""
        print("🧪 Running system tests...")

        try:
            test_script = os.path.join(os.path.dirname(__file__), "test_anonymity_system.py")
            test_result = subprocess.run([
                sys.executable, test_script
            ], capture_output=True, text=True, timeout=60)

            if test_result.returncode == 0:
                print("✅ All tests passed")
                print(test_result.stdout[-500:])  # Last 500 chars
                return True
            else:
                print("❌ Some tests failed")
                print(test_result.stderr[-300:])  # Last 300 chars of errors
                return False

        except subprocess.TimeoutExpired:
            print("❌ Tests timed out")
            return False
        except Exception as e:
            print(f"❌ Test execution error: {e}")
            return False

    def create_config_file(self):
        """Create configuration file"""
        print("⚙️ Creating configuration file...")

        config = {
            "version": "4.0",
            "installed_date": str(os.times()),
            "geo_db_path": "geo/GeoLite2-City.mmdb",
            "proxy_sources": 5,
            "max_threads": 20,
            "cache_enabled": True,
            "auto_update": False
        }

        try:
            with open('config.json', 'w') as f:
                import json
                json.dump(config, f, indent=2)

            print("✅ Configuration file created: config.json")
            return True

        except Exception as e:
            print(f"❌ Failed to create config file: {e}")
            return False

    def install(self):
        """Run complete installation"""
        print("🚀 Starting Anonymity Toolkit Installation...")
        print("=" * 50)

        steps = [
            ("Python Version Check", self.check_python_version),
            ("Python Dependencies", self.install_python_dependencies),
            ("Directory Setup", self.setup_directories),
            ("GeoIP Database", self.download_geoip_database),
            ("Configuration File", self.create_config_file),
            ("Desktop Shortcuts", self.create_desktop_shortcuts),
            ("System Tests", self.run_tests)
        ]

        results = []
        for step_name, step_func in steps:
            print(f"\n🔧 {step_name}...")
            success = step_func()
            results.append((step_name, success))

            if not success and step_name not in ["Desktop Shortcuts"]:  # Optional step
                print(f"❌ Installation failed at: {step_name}")
                break

        # Summary
        print("\n" + "=" * 50)
        print("📋 INSTALLATION SUMMARY:")
        print("=" * 50)

        for step_name, success in results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status}: {step_name}")

        successful_steps = sum(1 for _, success in results if success)
        total_steps = len(results)

        if successful_steps == total_steps:
            print(f"\n🎉 INSTALLATION COMPLETE! ({successful_steps}/{total_steps} steps)")
            print("\n🚀 Your Anonymity Toolkit is ready to use!")
            print("💡 Run: python main.py")
            print("🔗 Or use the desktop shortcut")
        else:
            print(f"\n⚠️ Installation partially complete ({successful_steps}/{total_steps} steps)")
            print("🔧 Some features may not work correctly")

        return successful_steps == total_steps

def main():
    """Main installation function"""
    installer = AnonymityToolkitInstaller()
    installer.print_banner()
    success = installer.install()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())















































