#!/bin/bash

echo "==========================================="
echo "🎯 Ultimate Anonymity Toolkit v4.0 Launcher"
echo "==========================================="

# Check for display environment
if [ -z "$DISPLAY" ]; then
    echo ""
    echo "⚠️  DISPLAY environment variable not set"
    echo "📋 GUI Launch Instructions:"
    echo ""
    echo "🔸 For Linux Desktop:"
    echo "   ./launch_gui.sh                 # If in desktop session"
    echo ""
    echo "🔸 For SSH with X11 forwarding:"
    echo '   ssh -X user@host -p port        # Enable X11 forwarding'
    echo ""
    echo "🔸 For VNC/AnyDesk:"
    echo "   export DISPLAY=:0.0            # Basic display"
    echo "   # or"
    echo "   export DISPLAY=:1.0            # VNC display"
    echo ""
    echo "🔸 For Windows WSL:"
    echo '   export DISPLAY=$(ip route | awk '\''NR==1{print $3}'\''):0.0'
    echo ""
    echo "🔸 Alternative: CLI mode"
    echo "   python main.py --cli            # Command line interface"
    echo ""
    echo "==========================================="
    exit 1
fi

# Check if tkinter is available
python -c "import tkinter; print('✅ Tkinter available')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Tkinter not available - install python3-tk"
    echo ""
    echo "Ubuntu/Debian: sudo apt install python3-tk"
    echo "CentOS/RHEL:   sudo yum install tkinter"
    echo "macOS:         brew install python-tk"
    exit 1
fi

# Launch the GUI with logging
echo ""
echo "🚀 Launching GUI..."
echo "🌟 Window title: 'Ultimate Anonymity Toolkit v4.0'"
echo "📊 Features: Proxy scraping, location filtering, cookie management"
echo ""

python main.py 2>&1 | tee gui_log.txt

echo ""
echo "==========================================="
echo "✅ GUI session ended"
echo "📝 Log saved to: gui_log.txt"
echo "==========================================="
