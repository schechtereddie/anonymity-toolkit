#!/usr/bin/env python3
"""
Simple Launcher for Enhanced Ultimate Anonymity Toolkit v6.0
Launch the complete system with user browser integration and all stealth features
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import logging

def main():
    """Launch the enhanced anonymity toolkit"""
    try:
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('enhanced_anonymity_toolkit.log'),
                logging.StreamHandler()
            ]
        )
        logger = logging.getLogger(__name__)

        logger.info("🚀 Launching Enhanced Ultimate Anonymity Toolkit v6.0")

        # Import the enhanced GUI
        try:
            # Try importing from src directory
            sys.path.insert(0, 'src')
            from core.enhanced_gui import EnhancedAnonymityGUI
            logger.info("✅ Enhanced GUI imported successfully")
        except ImportError:
            logger.error("❌ Failed to import Enhanced GUI from src directory")
            try:
                # Try importing directly from current directory
                from enhanced_gui import EnhancedAnonymityGUI
                logger.info("✅ Enhanced GUI imported from current directory")
            except ImportError as e:
                logger.error(f"❌ Failed to import Enhanced GUI: {e}")
                messagebox.showerror("Import Error",
                    "Failed to import enhanced components.\n\n"
                    "Please ensure you have:\n"
                    "• Python 3.8+\n"
                    "• tkinter (usually included)\n"
                    "• psutil (pip install psutil)\n\n"
                    f"Error: {e}")
                return False

        # Create the main window
        root = tk.Tk()
        root.title("🚀 Enhanced Ultimate Anonymity Toolkit v6.0")

        # Set window size and position
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)

        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Create the enhanced GUI
        try:
            app = EnhancedAnonymityGUI(root)
            logger.info("✅ Enhanced GUI initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Enhanced GUI: {e}")
            messagebox.showerror("Initialization Error",
                "Failed to initialize the enhanced GUI.\n\n"
                f"Error: {e}")
            return False

        # Setup cleanup on exit
        def on_closing():
            try:
                # Save session data
                if hasattr(app, 'save_session'):
                    app.save_session()

                # Cleanup browser sessions
                if hasattr(app, 'user_browser') and app.user_browser:
                    app.user_browser.terminate_all_sessions()

                root.destroy()

            except Exception as e:
                logger.error(f"Error during cleanup: {e}")
                root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        # Start the main loop
        logger.info("🎯 Enhanced system ready - starting main loop")
        root.mainloop()

        return True

    except Exception as e:
        print(f"❌ Critical error launching enhanced system: {e}")
        import traceback
        traceback.print_exc()

        # Show error dialog
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("Critical Error",
                "Failed to launch the Enhanced Ultimate Anonymity Toolkit.\n\n"
                f"Error: {e}\n\n"
                "Please check the logs for more details.")
            root.destroy()
        except:
            pass

        return False

if __name__ == "__main__":
    print("🚀 Enhanced Ultimate Anonymity Toolkit v6.0")
    print("=" * 60)
    print("🎯 Features:")
    print("  ✅ User Browser Integration with Profile-Consistent Fingerprinting")
    print("  ✅ Real-time Status Banner with Anonymity Scoring")
    print("  ✅ Enhanced Proxy Management with 50+ Sources")
    print("  ✅ Smart Cookie System with Domain Validation")
    print("  ✅ Background Processing for Non-blocking Operations")
    print("  ✅ Session Persistence and Auto-save")
    print("  ✅ Professional GUI with Modern Design")
    print("=" * 60)

    success = main()

    if success:
        print("✅ Enhanced system launched successfully!")
        print("🎉 Enjoy your anonymous browsing experience!")
    else:
        print("❌ Failed to launch enhanced system")
        sys.exit(1)
