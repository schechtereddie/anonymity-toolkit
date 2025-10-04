#!/usr/bin/env python3
"""Simple GUI test to verify Tkinter display capability"""

import tkinter as tk
from tkinter import ttk

def test_gui():
    """Create a simple test GUI"""
    try:
        root = tk.Tk()
        root.title("GUI Test - Ultimate Anonymity Toolkit")
        root.geometry("400x300")

        # Create a simple label
        label = ttk.Label(root, text="✅ GUI WORKING!\nUltimate Anonymity Toolkit v4.0 Ready",
                         font=('Arial', 14, 'bold'), foreground='green')
        label.pack(pady=20)

        # Add some information
        info_text = """
🛡️ GUI Status: FUNCTIONAL
🌍 Features: Proxy scraping, geo-location, cookie management
🔒 Security: Leak detection, traffic monitoring
🎭 Anonymity: Profile-based fingerprint spoofing

GUI will launch if you have:
• X11/Wayland display server
• DISPLAY environment variable set
• GUI environment (desktop, VNC, etc.)
"""

        info_label = ttk.Label(root, text=info_text, justify=tk.LEFT, font=('Courier', 9))
        info_label.pack(pady=10)

        # Exit button
        exit_btn = ttk.Button(root, text="Exit Test", command=root.quit)
        exit_btn.pack(pady=10)

        # Environment info
        env_info = f"DISPLAY={tk.Tk().winfo_screenwidth()}x{tk.Tk().winfo_screenheight()}"
        env_label = ttk.Label(root, text=f"Screen: {env_info}", font=('Arial', 8))
        env_label.pack(pady=5)

        root.mainloop()

    except Exception as e:
        print("=" * 50)
        print("❌ GUI TEST FAILED")
        print("=" * 50)
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check if you have a display server running")
        print("2. Try: export DISPLAY=:0")
        print("3. Try: python -m py_compile main.py")
        print("4. Try: python -c 'import tkinter; tkinter.test()'")
        print("=" * 50)

if __name__ == "__main__":
    test_gui()
