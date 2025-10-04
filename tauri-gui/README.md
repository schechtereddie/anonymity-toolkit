# Ultimate Anonymity Toolkit v4.0

A comprehensive anonymity toolkit that combines advanced proxy scraping, geo-location analysis, browser automation, cookie management, and leak detection capabilities for anonymous browsing and online privacy.

## 🎭 NEW: Dual-Mode Operation System

The toolkit now features a revolutionary **Dual-Mode Operation System** that lets you choose between:

- **👤 Profile Mode** - Persistent, believable digital identities for long-term use
  - Consistent fingerprints across sessions
  - Realistic demographics and behavior
  - Natural profile evolution over time
  - Perfect for maintaining accounts and building trust

- **🎭 Stealth Mode** - Random fingerprints for maximum anonymity
  - New identity every session
  - No data persistence
  - Impossible to track
  - Ideal for one-time anonymous tasks

- **🤖 Headless Mode** - Automated operations and scripting
  - No visible browser window
  - Optimized for speed
  - Perfect for automation

**📖 Documentation:**
- [Complete Dual-Mode Guide](DUAL_MODE_GUIDE.md)
- [Interactive HTML Guide](docs/dual_mode_guide.html)
- [Implementation Details](IMPLEMENTATION_SUMMARY.md)

## 🔒 Features

### Core Components
- **🔍 Advanced Proxy Scraper**: Multi-threaded SOCKS5 proxy discovery from multiple sources
- **🌍 Geo-Location Engine**: MaxMind database integration with API fallbacks for precise geo-data
- **🍪 Cookie Management**: Automated real cookie harvesting from top websites
- **🛡️ Leak Detection**: WebRTC, DNS, and canvas fingerprinting protection
- **🌐 Browser Automation**: Selenium-based browser control with anti-detection measures
- **📊 Real-time Monitoring**: Live status updates and comprehensive testing

### Security Features
- SOCKS5 proxy rotation and verification
- User agent randomization and fingerprinting protection
- DNS leak prevention
- WebRTC leak detection
- Canvas fingerprinting countermeasures
- Automated cookie harvesting from legitimate sites

## 🚀 Quick Start

### Prerequisites

**System Requirements:**
- Python 3.8+
- Linux/Windows/macOS
- 2GB+ RAM recommended

**Required Dependencies:**
```bash
pip install -r requirements.txt
```

### Optional Dependencies (for enhanced features):
- MaxMind GeoLite2-City.mmdb database (for offline geo lookups)
- Selenium WebDriver (for automated browser testing)
- SQLite3 (for cookie storage)

### Installation

1. **Clone/download the project**
2. **Install dependencies:**
   ```bash
   cd anon_best
   pip install -r requirements.txt
   ```
3. **Set up GeoLite2 database (optional but recommended):**
   - Download `GeoLite2-City.mmdb` from MaxMind
   - Place it in the project directory
4. **Run the application:**
   ```bash
   python main.py
   ```

## 🎯 Usage

### GUI Mode (Primary Interface)

```bash
python main.py
```

**Available Tabs:**

#### 🔍 Proxy Manager
- **Scrape Proxies**: Automatically discover SOCKS5 proxies from multiple sources
- **Verify Proxies**: Test proxy connectivity and speed with geo-location data
- **Geo Lookup**: Get detailed location information for any IP address
- **Export/Import**: Save verified proxies for later use

#### 🌍 Geo Location
- **IP Lookup**: Lookup any IPv4 address
- **Bulk Processing**: Process multiple IPs simultaneously
- **Current IP Detection**: Find your current public IP

#### 🍪 Cookie Manager
- **User Agent Generation**: Create realistic browser fingerprints
- **Cookie Harvesting**: Collect authentic cookies from top websites
- **Profile Management**: Maintain separate browsing profiles

#### 🌐 Browser Testing
- **Proxy Integration**: Test proxy setups in real browsers
- **Leak Detection**: Comprehensive security assessment
- **IP Verification**: Confirm proxy effectiveness

#### 🛡️ Leak Protection
- **WebRTC Detection**: Prevent IP leakage through WebRTC
- **DNS Monitoring**: Real-time DNS leak protection
- **Canvas Fingerprinting**: Anti-tracking countermeasures

### CLI Mode

For headless/server environments:

```bash
python test_anonymity_system.py
```

### Command Line Scripts

Pre-configured shell scripts for different run modes:

- `run_v1.sh` - Basic toolkit mode
- `run_v2.sh` - Enhanced features
- `run_v3.sh` - Full capabilities
- `run_cli.sh` - CLI-only mode

## 🧪 Testing

### System Self-Test

Run the built-in comprehensive test suite:

```bash
python test_anonymity_system.py
```

This tests:
- Component imports and initialization
- Proxy scraping functionality
- Geo-location services
- GUI framework integrity
- Component integration

### Manual Testing

1. **Proxy Testing**:
   - Scrape proxies from multiple sources
   - Verify connectivity and speed
   - Filter by country/location

2. **Geo Testing**:
   - Test current IP detection
   - Validate geo-database accuracy
   - Check cache performance

3. **Security Testing**:
   - Run browser leak tests
   - Verify fingerprinting protection
   - Test WebRTC blocking

## 🔧 Configuration

### Environment Variables

```bash
export MAXMIND_DB_PATH="/path/to/GeoLite2-City.mmdb"
export PROXY_TIMEOUT=15
export GEO_CACHE_SIZE=1000
```

### Configuration Files

- `cookies.db` - SQLite database for harvested cookies
- `browser_config.json` - Browser automation settings
- `proxies.json` - Exported verified proxy lists

## 🏗️ Architecture

```
Ultimate Anon Toolkit/
├── main.py                 # Main GUI application
├── proxy_scraper.py        # Proxy discovery & verification
├── geo_locator.py          # Geo-IP location services
├── cookie_manager.py       # User agent & cookie management
├── cookie_harvester.py     # Automated cookie collection
├── leak_detector.py        # Security vulnerability detection
├── browser_controller.py   # Selenium-based browser automation
├── test_anonymity_system.py # Comprehensive testing suite
└── requirements.txt        # Python dependencies
```

### Key Classes

- `UltimateAnonToolkit`: Main GUI application controller
- `AdvancedProxyScraper`: Multi-threaded proxy harvesting
- `AdvancedGeoLocator`: Geo-IP database and API integration
- `CookieHarvester`: Real cookie acquisition from websites
- `BrowserController`: Selenium automation with anti-detection

## 🔒 Security Best Practices

### Proxy Usage
- Always verify proxies before use
- Rotate proxies regularly
- Use SOCKS5 over HTTP for better anonymity

### Cookie Management
- Harvest cookies from legitimate sites only
- Clear cookies between sessions when needed
- Use separate profiles for different activities

### Browser Fingerprinting
- Randomize user agents regularly
- Disable WebRTC in supported browsers
- Clear browser data between sessions

## 🐛 Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Geo DB Issues:**
- Ensure MaxMind database is readable
- Check file permissions
- Verify database is not corrupted

**Proxy Connection Failures:**
- Test proxies individually
- Check firewall settings
- Verify SOCKS5 support

**Browser Automation Issues:**
- Ensure Chrome/Firefox drivers are installed
- Check Selenium version compatibility
- Verify browser installation

### Performance Optimization

- Use async operations for bulk processing
- Enable geo-cache for repeated lookups
- Limit concurrent threads based on system resources

## 📊 Performance Metrics

Typical performance on modern hardware:

- **Proxy Scraping**: 50-200 proxies/minute
- **Geo Lookups**: 100+ IPs/second (with cache)
- **Browser Tests**: 10-30 seconds per test
- **Cookie Harvesting**: 5-20 seconds per site

## 🤝 Contributing

This is a comprehensive anonymity toolkit designed for educational and legitimate privacy purposes. Use responsibly and in accordance with applicable laws.

## 📝 License

See individual component licenses for details.

## ⚠️ Disclaimer

This toolkit is for educational purposes and legitimate privacy protection. Users are responsible for complying with all applicable laws and terms of service.

---

**Version**: 4.0
**Last Updated**: October 2025
**Supported Platforms**: Linux, Windows, macOS
