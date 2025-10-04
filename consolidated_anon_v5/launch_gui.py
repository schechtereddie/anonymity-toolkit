#!/usr/bin/env python3
"""
LAUNCHER FOR CONSOLIDATED ANONYMITY TOOLKIT v5.0
Clean, organized version with all fixes applied
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from enhanced_working_gui import main
    main()
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error launching GUI: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
