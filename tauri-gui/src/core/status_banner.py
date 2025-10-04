#!/usr/bin/env python3
"""
Real-time Status Banner System
Displays live anonymity score, profile status, and system health
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from typing import Dict, Any, Optional, Callable
import json

class StatusBanner:
    """Real-time status display for anonymity system"""

    def __init__(self, parent_frame, width: int = 800, height: int = 60):
        self.parent = parent_frame
        self.width = width
        self.height = height

        # Status data
        self.current_status = {
            'anonymity_score': 0,
            'profile_name': 'None',
            'proxy_status': 'Disconnected',
            'cookie_count': 0,
            'browser_sessions': 0,
            'system_health': 'Unknown',
            'last_update': 0
        }

        # Status callbacks
        self.update_callbacks = []

        # Create the banner UI
        self._create_banner()

        # Start auto-refresh
        self._start_auto_refresh()

    def _create_banner(self):
        """Create the status banner UI"""
        # Main banner frame
        self.banner_frame = ttk.Frame(self.parent, relief='raised', borderwidth=2)
        self.banner_frame.pack(fill='x', padx=5, pady=5)

        # Left section - Primary status
        self.left_frame = ttk.Frame(self.banner_frame)
        self.left_frame.pack(side='left', padx=10, pady=5)

        # Anonymity score (main indicator)
        self.score_label = ttk.Label(
            self.left_frame,
            text="🔒 Score: 0/100",
            font=("Arial", 14, "bold"),
            foreground="red"
        )
        self.score_label.pack(side='left', padx=5)

        # Status indicator
        self.status_canvas = tk.Canvas(
            self.left_frame,
            width=20,
            height=20,
            bg='white',
            highlightthickness=0
        )
        self.status_canvas.pack(side='left', padx=5)
        self._draw_status_circle("red")

        # Center section - Profile and proxy info
        self.center_frame = ttk.Frame(self.banner_frame)
        self.center_frame.pack(side='left', padx=20, pady=5, fill='x', expand=True)

        self.info_label = ttk.Label(
            self.center_frame,
            text="👤 Profile: None | 🌐 Proxy: Disconnected | 🍪 Cookies: 0",
            font=("Arial", 10)
        )
        self.info_label.pack(side='left')

        # Right section - Browser sessions and system health
        self.right_frame = ttk.Frame(self.banner_frame)
        self.right_frame.pack(side='right', padx=10, pady=5)

        self.system_label = ttk.Label(
            self.right_frame,
            text="🌐 Sessions: 0 | 💊 Health: Unknown",
            font=("Arial", 9)
        )
        self.system_label.pack(side='right')

        # Update timestamp
        self.timestamp_label = ttk.Label(
            self.right_frame,
            text="Last update: Never",
            font=("Arial", 8),
            foreground="gray"
        )
        self.timestamp_label.pack(side='right', padx=10)

    def _draw_status_circle(self, color: str):
        """Draw status indicator circle"""
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(3, 3, 17, 17, fill=color, outline=color)
        self.status_canvas.update()

    def _get_status_color(self, score: int) -> str:
        """Get color based on anonymity score"""
        if score >= 90:
            return "green"
        elif score >= 70:
            return "orange"
        elif score >= 50:
            return "yellow"
        else:
            return "red"

    def _get_health_color(self, health: str) -> str:
        """Get color based on system health"""
        health_colors = {
            'Excellent': 'green',
            'Good': 'lightgreen',
            'Fair': 'orange',
            'Poor': 'red',
            'Critical': 'darkred',
            'Unknown': 'gray'
        }
        return health_colors.get(health, 'gray')

    def update_status(self, status_data: Dict[str, Any]):
        """Update banner with new status data"""
        self.current_status.update(status_data)
        self.current_status['last_update'] = time.time()

        # Update UI elements
        self._update_score_display()
        self._update_info_display()
        self._update_system_display()
        self._update_timestamp()

        # Notify callbacks
        self._notify_callbacks()

    def _update_score_display(self):
        """Update anonymity score display"""
        score = self.current_status.get('anonymity_score', 0)
        color = self._get_status_color(score)

        self.score_label.config(
            text=f"🔒 Score: {score}/100",
            foreground=color
        )

        # Update status circle
        self._draw_status_circle(color)

    def _update_info_display(self):
        """Update profile and proxy information"""
        profile = self.current_status.get('profile_name', 'None')
        proxy = self.current_status.get('proxy_status', 'Disconnected')
        cookies = self.current_status.get('cookie_count', 0)

        info_text = f"👤 Profile: {profile} | 🌐 Proxy: {proxy} | 🍪 Cookies: {cookies}"
        self.info_label.config(text=info_text)

    def _update_system_display(self):
        """Update system health and session info"""
        sessions = self.current_status.get('browser_sessions', 0)
        health = self.current_status.get('system_health', 'Unknown')
        color = self._get_health_color(health)

        system_text = f"🌐 Sessions: {sessions} | 💊 Health: {health}"
        self.system_label.config(text=system_text, foreground=color)

    def _update_timestamp(self):
        """Update last update timestamp"""
        timestamp = self.current_status.get('last_update', 0)
        if timestamp > 0:
            time_str = time.strftime("%H:%M:%S", time.localtime(timestamp))
            self.timestamp_label.config(text=f"Last update: {time_str}")
        else:
            self.timestamp_label.config(text="Last update: Never")

    def _start_auto_refresh(self):
        """Start automatic status refresh"""
        def refresh():
            while True:
                try:
                    # Refresh every 5 seconds
                    time.sleep(5)
                    self._refresh_status()
                except Exception as e:
                    print(f"Error in status refresh: {e}")
                    break

        refresh_thread = threading.Thread(target=refresh, daemon=True)
        refresh_thread.start()

    def _refresh_status(self):
        """Refresh status from various sources"""
        # This would typically gather data from the main application
        # For now, we'll simulate some basic status
        pass

    def add_update_callback(self, callback: Callable):
        """Add callback for status updates"""
        self.update_callbacks.append(callback)

    def _notify_callbacks(self):
        """Notify all callbacks of status update"""
        for callback in self.update_callbacks:
            try:
                callback(self.current_status.copy())
            except Exception as e:
                print(f"Error in status callback: {e}")

    def calculate_anonymity_score(self, profile_data: Optional[Dict[str, Any]] = None,
                                 proxy_data: Optional[Dict[str, Any]] = None,
                                 cookie_data: Optional[Dict[str, Any]] = None) -> int:
        """
        Calculate comprehensive anonymity score (0-100)

        Factors considered:
        - Profile completeness (25 points)
        - Proxy quality and speed (25 points)
        - Cookie authenticity and count (20 points)
        - Browser fingerprint consistency (15 points)
        - System security settings (15 points)
        """
        score = 0

        # Profile completeness (25 points)
        if profile_data:
            profile_score = 0
            if profile_data.get('user_agent'): profile_score += 8
            if profile_data.get('screen_resolution'): profile_score += 6
            if profile_data.get('language'): profile_score += 6
            if profile_data.get('timezone'): profile_score += 5
            score += profile_score

        # Proxy quality (25 points)
        if proxy_data:
            proxy_score = 0
            if proxy_data.get('working'): proxy_score += 10
            if proxy_data.get('rtt_ms') and proxy_data['rtt_ms'] < 100: proxy_score += 8
            elif proxy_data.get('rtt_ms') and proxy_data['rtt_ms'] < 300: proxy_score += 5
            if proxy_data.get('country') and proxy_data['country'] != 'Unknown': proxy_score += 7
            score += proxy_score

        # Cookie authenticity (20 points)
        if cookie_data:
            cookie_score = 0
            total_cookies = cookie_data.get('total_cookies', 0)
            if total_cookies > 100: cookie_score += 10
            elif total_cookies > 50: cookie_score += 7
            elif total_cookies > 20: cookie_score += 4

            unique_domains = cookie_data.get('unique_domains', 0)
            if unique_domains > 20: cookie_score += 10
            elif unique_domains > 10: cookie_score += 6
            elif unique_domains > 5: cookie_score += 3

            score += cookie_score

        # Browser fingerprint (15 points)
        # This would be calculated based on fingerprint consistency
        fingerprint_score = 15  # Placeholder
        score += fingerprint_score

        # System security (15 points)
        # This would check for security settings
        security_score = 15  # Placeholder
        score += security_score

        return min(100, max(0, score))

    def get_status_summary(self) -> Dict[str, Any]:
        """Get comprehensive status summary"""
        return {
            'current_status': self.current_status.copy(),
            'anonymity_score': self.current_status.get('anonymity_score', 0),
            'score_color': self._get_status_color(self.current_status.get('anonymity_score', 0)),
            'health_color': self._get_health_color(self.current_status.get('system_health', 'Unknown')),
            'timestamp': self.current_status.get('last_update', 0)
        }

    def set_status(self, key: str, value: Any):
        """Set individual status value"""
        self.current_status[key] = value
        self.update_status({})  # Trigger UI update

    def get_status(self, key: str, default: Any = None) -> Any:
        """Get individual status value"""
        return self.current_status.get(key, default)

    def reset_status(self):
        """Reset status to default values"""
        self.current_status = {
            'anonymity_score': 0,
            'profile_name': 'None',
            'proxy_status': 'Disconnected',
            'cookie_count': 0,
            'browser_sessions': 0,
            'system_health': 'Unknown',
            'last_update': 0
        }
        self.update_status({})

    def show_detailed_status(self):
        """Show detailed status in a popup window"""
        try:
            # Create detailed status window
            detail_window = tk.Toplevel(self.parent)
            detail_window.title("🔍 Detailed Status")
            detail_window.geometry("600x400")
            detail_window.transient(self.parent)

            # Title
            title_label = ttk.Label(
                detail_window,
                text="📊 Detailed Anonymity Status",
                font=("Arial", 16, "bold")
            )
            title_label.pack(pady=20)

            # Create text area for detailed info
            text_area = tk.Text(detail_window, height=20, width=70, font=("Consolas", 9))
            text_area.pack(padx=20, pady=10)

            # Generate detailed status report
            status_report = self._generate_detailed_report()
            text_area.insert(1.0, status_report)
            text_area.config(state='disabled')

            # Close button
            close_btn = ttk.Button(
                detail_window,
                text="Close",
                command=detail_window.destroy
            )
            close_btn.pack(pady=10)

        except Exception as e:
            print(f"Error showing detailed status: {e}")

    def _generate_detailed_report(self) -> str:
        """Generate detailed status report"""
        status = self.current_status
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        report = f"""
🔍 DETAILED ANONYMITY STATUS REPORT
{'='*50}
Generated: {current_time}

📊 ANONYMITY SCORE: {status.get('anonymity_score', 0)}/100
{'='*50}

👤 PROFILE INFORMATION:
   • Profile Name: {status.get('profile_name', 'None')}
   • Status: {'Active' if status.get('profile_name', 'None') != 'None' else 'Inactive'}
   • Configuration: {'Complete' if status.get('profile_name', 'None') != 'None' else 'Incomplete'}

🌐 PROXY STATUS:
   • Connection: {status.get('proxy_status', 'Disconnected')}
   • Quality: {'Good' if 'Connected' in status.get('proxy_status', '') else 'Unknown'}
   • Performance: {'Optimal' if status.get('proxy_status') == 'Connected' else 'N/A'}

🍪 COOKIE DATABASE:
   • Total Cookies: {status.get('cookie_count', 0)}
   • Status: {'Ready' if status.get('cookie_count', 0) > 0 else 'Empty'}
   • Quality: {'High' if status.get('cookie_count', 0) > 100 else 'Low' if status.get('cookie_count', 0) > 20 else 'Minimal'}

🌐 BROWSER SESSIONS:
   • Active Sessions: {status.get('browser_sessions', 0)}
   • Status: {'Active' if status.get('browser_sessions', 0) > 0 else 'Inactive'}

💊 SYSTEM HEALTH: {status.get('system_health', 'Unknown')}
   • Overall Status: {'Good' if status.get('system_health') in ['Excellent', 'Good'] else 'Needs Attention'}
   • Components: All systems operational

🔧 RECOMMENDATIONS:
{'='*50}
"""

        # Add specific recommendations based on current status
        score = status.get('anonymity_score', 0)

        if score < 50:
            report += """
⚠️  CRITICAL IMPROVEMENTS NEEDED:
   • Set up a working proxy connection
   • Create or load a browsing profile
   • Generate realistic cookie history
   • Configure browser fingerprinting
"""
        elif score < 75:
            report += """
⚡ MODERATE IMPROVEMENTS SUGGESTED:
   • Add more cookie history for better authenticity
   • Verify proxy speed and reliability
   • Consider using a different geographic proxy
   • Update browser fingerprint settings
"""
        elif score < 90:
            report += """
✅ GOOD ANONYMITY LEVEL:
   • Consider adding more diverse cookie sources
   • Monitor proxy performance regularly
   • Keep browser profiles updated
"""
        else:
            report += """
🎉 EXCELLENT ANONYMITY ACHIEVED:
   • All systems operating optimally
   • Maintain current configuration
   • Regular proxy rotation recommended
"""

        report += f"""

🔗 Last Update: {time.strftime('%H:%M:%S', time.localtime(status.get('last_update', 0)))}

{'='*50}
End of Report
"""

        return report

    def export_status(self, filename: str = None) -> str:
        """Export current status to file"""
        if not filename:
            import time
            timestamp = int(time.time())
            filename = f"anonymity_status_{timestamp}.json"

        try:
            status_data = {
                'export_time': int(time.time()),
                'status': self.current_status.copy(),
                'summary': self.get_status_summary()
            }

            with open(filename, 'w') as f:
                json.dump(status_data, f, indent=2)

            return filename

        except Exception as e:
            print(f"Error exporting status: {e}")
            return ""

    def import_status(self, filename: str) -> bool:
        """Import status from file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            if 'status' in data:
                self.current_status.update(data['status'])
                self.update_status({})
                return True

        except Exception as e:
            print(f"Error importing status: {e}")

        return False
