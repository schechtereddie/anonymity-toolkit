#!/usr/bin/env python3
"""
Comprehensive Test Suite for Anonymity Browser Backend
Tests all features: profiles, cookies, proxies, leak detection
"""

import json
import sys
import subprocess
from typing import Dict, Any, List

class BackendTester:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []
    
    def send_command(self, command: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a command to the backend via stdin and get response"""
        if data is None:
            data = {}

        message = json.dumps({"command": command, "data": data})

        try:
            result = subprocess.run(
                ['python3', 'main.py'],
                input=message,
                capture_output=True,
                text=True,
                timeout=30
            )

            # Parse the response - filter out log lines, only get JSON
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                # Find the JSON response (starts with { or [)
                for line in reversed(lines):  # Check from end, JSON is usually last
                    line = line.strip()
                    if line.startswith('{') or line.startswith('['):
                        try:
                            return json.loads(line)
                        except json.JSONDecodeError:
                            continue

                # If no JSON found, return error
                return {"success": False, "error": f"No JSON found in output. stdout: {result.stdout[:200]}"}
            else:
                return {"success": False, "error": f"No output. stderr: {result.stderr}"}
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test(self, name: str, command: str, data: Dict[str, Any] = None, 
             expected_success: bool = True, check_fields: List[str] = None) -> bool:
        """Run a test and check the result"""
        print(f"\n🧪 Testing: {name}")
        print(f"   Command: {command}")
        if data:
            print(f"   Data: {json.dumps(data, indent=2)}")
        
        response = self.send_command(command, data)
        
        # Check if success matches expected
        success = response.get('success', False)
        
        if success != expected_success:
            print(f"   ❌ FAILED: Expected success={expected_success}, got success={success}")
            print(f"   Response: {json.dumps(response, indent=2)}")
            self.tests_failed += 1
            self.test_results.append({"test": name, "status": "FAILED", "reason": "Unexpected success value"})
            return False
        
        # Check required fields
        if check_fields:
            for field in check_fields:
                if field not in response:
                    print(f"   ❌ FAILED: Missing field '{field}' in response")
                    print(f"   Response: {json.dumps(response, indent=2)}")
                    self.tests_failed += 1
                    self.test_results.append({"test": name, "status": "FAILED", "reason": f"Missing field: {field}"})
                    return False
        
        print(f"   ✅ PASSED")
        if response.get('error'):
            print(f"   Note: {response['error']}")
        self.tests_passed += 1
        self.test_results.append({"test": name, "status": "PASSED", "response": response})
        return True
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("=" * 80)
        print("🚀 ANONYMITY BROWSER BACKEND - COMPREHENSIVE TEST SUITE")
        print("=" * 80)
        
        # Test 1: Ping
        self.test(
            "Ping Backend",
            "ping",
            expected_success=True,
            check_fields=["message"]
        )
        
        # Test 2: Get Status
        self.test(
            "Get Backend Status",
            "get_status",
            expected_success=True,
            check_fields=["status"]
        )
        
        # Test 3: Create Profile
        profile_data = {
            "profile_name": "test_profile_automated",
            "demographics": {
                "age": 28,
                "gender": "male",
                "occupation": "software_engineer"
            },
            "location": {
                "country": "United States",
                "city": "San Francisco",
                "timezone": "America/Los_Angeles"
            }
        }
        self.test(
            "Create Profile",
            "create_profile",
            data=profile_data,
            expected_success=True,
            check_fields=["profile_id", "message"]
        )
        
        # Test 4: List Profiles
        self.test(
            "List Profiles",
            "list_profiles",
            expected_success=True,
            check_fields=["profiles"]
        )
        
        # Test 5: Load Profile
        self.test(
            "Load Profile",
            "load_profile",
            data={"profile_id": "test_profile_automated"},
            expected_success=True,
            check_fields=["profile"]
        )
        
        # Test 6: Generate Simple Cookies
        self.test(
            "Generate Simple Cookies",
            "generate_cookies",
            data={"domain": "example.com", "count": 5},
            expected_success=True,
            check_fields=["cookies", "count"]
        )
        
        # Test 7: Generate Realistic Cookies
        self.test(
            "Generate Realistic Cookies",
            "generate_realistic_cookies",
            data={
                "profile_id": "test_profile_automated",
                "session_duration": 30,
                "sites_visited": 10
            },
            expected_success=True,
            check_fields=["cookies", "total_cookies"]
        )
        
        # Test 8: Add Proxy
        self.test(
            "Add Proxy",
            "add_proxy",
            data={
                "id": "test_proxy_1",
                "name": "Test Proxy",
                "host": "127.0.0.1",
                "port": 9050,
                "type": "socks5",
                "username": "",
                "password": ""
            },
            expected_success=True,
            check_fields=["message"]
        )
        
        # Test 9: List Proxies
        self.test(
            "List Proxies",
            "list_proxies",
            expected_success=True,
            check_fields=["proxies"]
        )
        
        # Test 10: Scrape Proxies (may fail if sources are down)
        print("\n⚠️  Note: Proxy scraping may fail if external sources are unavailable")
        self.test(
            "Scrape Proxies",
            "scrape_proxies",
            data={"max_proxies": 5, "type": "socks5", "auto_save": False},
            expected_success=True,  # May fail, but we'll check
            check_fields=["proxies"]
        )
        
        # Test 11: Run Leak Detection
        self.test(
            "Run Leak Detection - All Tests",
            "run_leak_test",
            data={"test_type": "all"},
            expected_success=True,
            check_fields=["results", "total_tests"]
        )
        
        # Test 12: Run Individual Leak Tests
        for test_type in ["webrtc", "dns", "canvas", "webgl", "audio", "timezone"]:
            self.test(
                f"Run Leak Detection - {test_type.upper()}",
                "run_leak_test",
                data={"test_type": test_type},
                expected_success=True,
                check_fields=["results"]
            )
        
        # Test 13: Delete Profile (cleanup)
        self.test(
            "Delete Profile",
            "delete_profile",
            data={"profile_id": "test_profile_automated"},
            expected_success=True,
            check_fields=["message"]
        )
        
        # Print Summary
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_failed}")
        print(f"📈 Success Rate: {(self.tests_passed / (self.tests_passed + self.tests_failed) * 100):.1f}%")
        print("=" * 80)
        
        # Print detailed results
        print("\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            print(f"{status_icon} {result['test']}: {result['status']}")
            if result["status"] == "FAILED":
                print(f"   Reason: {result.get('reason', 'Unknown')}")
        
        print("\n" + "=" * 80)
        
        # Return exit code
        return 0 if self.tests_failed == 0 else 1

def main():
    tester = BackendTester()
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()

