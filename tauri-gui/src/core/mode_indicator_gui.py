#!/usr/bin/env python3
"""
Visual Mode Indicator and Help Dialog System
Provides clear visual feedback about current operation mode
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Optional, Callable
from datetime import datetime
import json

from .mode_documentation import HelpSystem, TOOLTIPS, ModeDocumentation


class ModeIndicator(tk.Frame):
    """Visual indicator showing current operation mode"""
    
    def __init__(self, parent, help_callback: Optional[Callable] = None):
        super().__init__(parent, relief=tk.RAISED, borderwidth=2)
        self.help_callback = help_callback
        self.current_mode = "profile"
        self.current_profile = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the mode indicator UI"""
        # Mode icon and text
        self.mode_frame = tk.Frame(self, bg='#2c3e50')
        self.mode_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Mode icon (emoji/symbol)
        self.icon_label = tk.Label(
            self.mode_frame,
            text="👤",
            font=('Arial', 24),
            bg='#2c3e50',
            fg='white'
        )
        self.icon_label.pack(side=tk.LEFT, padx=10)
        
        # Mode info
        info_frame = tk.Frame(self.mode_frame, bg='#2c3e50')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.mode_label = tk.Label(
            info_frame,
            text="PROFILE MODE",
            font=('Arial', 12, 'bold'),
            bg='#2c3e50',
            fg='#3498db'
        )
        self.mode_label.pack(anchor=tk.W)
        
        self.status_label = tk.Label(
            info_frame,
            text="Persistent Identity Active",
            font=('Arial', 9),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        self.status_label.pack(anchor=tk.W)
        
        self.profile_label = tk.Label(
            info_frame,
            text="No profile loaded",
            font=('Arial', 8, 'italic'),
            bg='#2c3e50',
            fg='#95a5a6'
        )
        self.profile_label.pack(anchor=tk.W)
        
        # Help button
        self.help_button = tk.Button(
            self.mode_frame,
            text="❓",
            font=('Arial', 16),
            bg='#34495e',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.show_mode_help
        )
        self.help_button.pack(side=tk.RIGHT, padx=5)
        
        # Bind click to show details
        self.mode_frame.bind('<Button-1>', lambda e: self.show_mode_details())
        self.icon_label.bind('<Button-1>', lambda e: self.show_mode_details())
        self.mode_label.bind('<Button-1>', lambda e: self.show_mode_details())
        
        # Add tooltips
        self.add_tooltip(self.mode_frame, TOOLTIPS['mode_indicator'])
        self.add_tooltip(self.help_button, "Click for detailed help about current mode")
    
    def update_mode(self, mode: str, profile_name: Optional[str] = None):
        """Update the mode indicator"""
        self.current_mode = mode.lower()
        self.current_profile = profile_name
        
        # Mode configurations
        mode_config = {
            'profile': {
                'icon': '👤',
                'title': 'PROFILE MODE',
                'status': 'Persistent Identity Active',
                'color': '#3498db',
                'bg': '#2c3e50'
            },
            'stealth': {
                'icon': '🎭',
                'title': 'STEALTH MODE',
                'status': 'Random Identity Active',
                'color': '#e74c3c',
                'bg': '#34495e'
            },
            'headless': {
                'icon': '🤖',
                'title': 'HEADLESS MODE',
                'status': 'Automated Operations',
                'color': '#9b59b6',
                'bg': '#2c3e50'
            },
            'testing': {
                'icon': '🧪',
                'title': 'TESTING MODE',
                'status': 'Fingerprint Testing',
                'color': '#f39c12',
                'bg': '#2c3e50'
            }
        }
        
        config = mode_config.get(self.current_mode, mode_config['profile'])
        
        # Update UI
        self.icon_label.config(text=config['icon'])
        self.mode_label.config(text=config['title'], fg=config['color'])
        self.status_label.config(text=config['status'])
        self.mode_frame.config(bg=config['bg'])
        self.icon_label.config(bg=config['bg'])
        self.mode_label.config(bg=config['bg'])
        self.status_label.config(bg=config['bg'])
        self.profile_label.config(bg=config['bg'])
        
        # Update profile info
        if profile_name and self.current_mode == 'profile':
            self.profile_label.config(text=f"Profile: {profile_name}")
        else:
            self.profile_label.config(text="No persistent profile")
    
    def show_mode_details(self):
        """Show detailed information about current mode"""
        ModeDetailsDialog(self, self.current_mode, self.current_profile)
    
    def show_mode_help(self):
        """Show help for current mode"""
        if self.help_callback:
            self.help_callback(self.current_mode)
        else:
            ModeHelpDialog(self, self.current_mode)
    
    def add_tooltip(self, widget, text):
        """Add tooltip to widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(
                tooltip,
                text=text,
                background='#ffffcc',
                relief=tk.SOLID,
                borderwidth=1,
                font=('Arial', 9)
            )
            label.pack()
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)


class ModeDetailsDialog(tk.Toplevel):
    """Dialog showing detailed mode information"""
    
    def __init__(self, parent, mode: str, profile_name: Optional[str] = None):
        super().__init__(parent)
        self.mode = mode
        self.profile_name = profile_name
        
        self.title(f"Mode Details - {mode.upper()}")
        self.geometry("600x500")
        self.resizable(True, True)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        # Header
        header = tk.Frame(self, bg='#34495e', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        help_system = HelpSystem()
        title = help_system.get_mode_title(self.mode)
        
        tk.Label(
            header,
            text=title,
            font=('Arial', 14, 'bold'),
            bg='#34495e',
            fg='white'
        ).pack(pady=15)
        
        # Content area with tabs
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Description
        desc_frame = tk.Frame(notebook)
        notebook.add(desc_frame, text="Description")
        
        desc_text = scrolledtext.ScrolledText(
            desc_frame,
            wrap=tk.WORD,
            font=('Courier', 10),
            bg='#ecf0f1'
        )
        desc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        desc_text.insert('1.0', help_system.get_mode_help(self.mode))
        desc_text.config(state=tk.DISABLED)
        
        # Tab 2: Comparison
        comp_frame = tk.Frame(notebook)
        notebook.add(comp_frame, text="Mode Comparison")
        
        comp_text = scrolledtext.ScrolledText(
            comp_frame,
            wrap=tk.NONE,
            font=('Courier', 9),
            bg='#ecf0f1'
        )
        comp_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        comp_text.insert('1.0', help_system.get_comparison_table())
        comp_text.config(state=tk.DISABLED)
        
        # Tab 3: Current Status
        status_frame = tk.Frame(notebook)
        notebook.add(status_frame, text="Current Status")
        
        status_text = scrolledtext.ScrolledText(
            status_frame,
            wrap=tk.WORD,
            font=('Courier', 10),
            bg='#ecf0f1'
        )
        status_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        status_info = f"""
CURRENT MODE: {self.mode.upper()}
TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
PROFILE: {self.profile_name if self.profile_name else 'None (Random Identity)'}

STATUS:
"""
        if self.mode == 'profile' and self.profile_name:
            status_info += f"""
✅ Persistent fingerprint active
✅ Cookies and history being saved
✅ Profile: {self.profile_name}
✅ Identity consistent across sessions
"""
        elif self.mode == 'stealth':
            status_info += """
✅ Random fingerprint active
✅ No data persistence
✅ Maximum anonymity mode
✅ New identity each session
"""
        elif self.mode == 'headless':
            status_info += """
✅ Headless browser mode
✅ Optimized for automation
✅ Random fingerprints
✅ No visual interface
"""
        else:
            status_info += """
✅ Testing mode active
✅ Fingerprint testing enabled
✅ Detailed logging active
"""
        
        status_text.insert('1.0', status_info)
        status_text.config(state=tk.DISABLED)
        
        # Close button
        tk.Button(
            self,
            text="Close",
            command=self.destroy,
            bg='#3498db',
            fg='white',
            font=('Arial', 10),
            cursor='hand2'
        ).pack(pady=10)


class ModeHelpDialog(tk.Toplevel):
    """Comprehensive help dialog"""
    
    def __init__(self, parent, initial_mode: str = 'profile'):
        super().__init__(parent)
        self.title("Dual-Mode Operation System - Help")
        self.geometry("800x600")
        self.resizable(True, True)
        
        self.help_system = HelpSystem()
        self.setup_ui(initial_mode)
    
    def setup_ui(self, initial_mode: str):
        """Setup the help dialog UI"""
        # Header
        header = tk.Frame(self, bg='#2c3e50', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🎭 Dual-Mode Operation System",
            font=('Arial', 16, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=10)
        
        tk.Label(
            header,
            text="Complete Guide to Profile and Stealth Modes",
            font=('Arial', 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack()
        
        # Tabbed interface
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Quick Start tab
        self.add_text_tab(notebook, "Quick Start", self.help_system.get_quick_start())
        
        # Mode descriptions
        self.add_text_tab(notebook, "Profile Mode", self.help_system.get_mode_help('profile'))
        self.add_text_tab(notebook, "Stealth Mode", self.help_system.get_mode_help('stealth'))
        self.add_text_tab(notebook, "Headless Mode", self.help_system.get_mode_help('headless'))
        
        # Comparison
        self.add_text_tab(notebook, "Comparison", self.help_system.get_comparison_table())
        
        # FAQ
        self.add_text_tab(notebook, "FAQ", self.help_system.get_faq())
        
        # Warnings
        self.add_text_tab(notebook, "Warnings", self.help_system.get_warnings())
        
        # Close button
        tk.Button(
            self,
            text="Close",
            command=self.destroy,
            bg='#3498db',
            fg='white',
            font=('Arial', 10),
            cursor='hand2'
        ).pack(pady=10)
    
    def add_text_tab(self, notebook, title: str, content: str):
        """Add a text tab to the notebook"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text=title)
        
        text_widget = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            font=('Courier', 10),
            bg='#ecf0f1'
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text_widget.insert('1.0', content)
        text_widget.config(state=tk.DISABLED)

