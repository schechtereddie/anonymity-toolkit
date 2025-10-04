#!/usr/bin/env python3
from leak_detector import LeakDetector

print("Testing LeakDetector...")

try:
    ld = LeakDetector()
    print("LeakDetector initialized OK")
    
    leaks = ld.get_leaks()
    print(f"Leak check result: {len(leaks)} leaks detected")
    
    # Test starting leak monitoring (briefly)
    ld.start_leak_protection(None)
    print("Leak protection started")
    
    import time
    time.sleep(2)  # Brief test
    
    ld.stop_leak_protection()
    print("Leak protection stopped")
    
    print("LeakDetector: All tests passed")

except Exception as e:
    print(f"LeakDetector test failed: {e}")
