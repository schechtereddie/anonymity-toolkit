"""
UI Components Package
Contains modular UI components extracted from the monolithic GUI
"""

# Stage 1: Tab and Status Management
from .tab_manager import TabManager

# Stage 2: Component-specific UI (to be implemented)
# from .status_manager import StatusManager
# from .browser_launcher_ui import BrowserLauncherUI
# from .proxy_manager_ui import ProxyManagerUI
# from .cookie_manager_ui import CookieManagerUI

__all__ = [
    'TabManager',
    # Stage 2 components will be added as implemented
    # 'StatusManager',
    # 'BrowserLauncherUI',
    # 'ProxyManagerUI',
    # 'CookieManagerUI'
]
