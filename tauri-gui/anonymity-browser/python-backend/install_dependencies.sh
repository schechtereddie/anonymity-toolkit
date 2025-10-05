#!/bin/bash
# Install Python dependencies for Anonymity Browser backend

echo "🔧 Installing Python dependencies for Anonymity Browser..."
echo ""

# Check if pip3 is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install Python 3 and pip first."
    exit 1
fi

echo "📦 Installing packages from requirements.txt..."
pip3 install --user -r requirements.txt

echo ""
echo "🎭 Installing Playwright browsers..."
python3 -m playwright install chromium

echo ""
echo "✅ All dependencies installed!"
echo ""
echo "📝 Installed packages:"
echo "  - playwright (browser automation)"
echo "  - requests (HTTP requests)"
echo "  - beautifulsoup4 (HTML parsing)"
echo "  - aiohttp (async HTTP)"
echo "  - maxminddb (geolocation for proxy scraper)"
echo "  - fake-useragent (user agent generation)"
echo "  - and more..."
echo ""
echo "🚀 You can now run the application!"
echo ""
echo "To test if everything works:"
echo "  cd $(pwd)"
echo "  python3 -c 'from cookie_manager import CookieManager; from proxy_scraper import AdvancedProxyScraper; print(\"✅ All imports successful!\")'"

