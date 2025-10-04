# 📖 User Guide

**Anonymity Browser - Tauri Edition**  
**Version:** 1.0.0

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Profile Management](#profile-management)
3. [Browser Launcher](#browser-launcher)
4. [Leak Detection](#leak-detection)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## Getting Started

### Installation

1. **Install Dependencies**
   ```bash
   cd /home/eddie/anon_best/tauri-gui/anonymity-browser
   npm install
   ```

2. **Install Python Dependencies**
   ```bash
   cd python-backend
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Run the Application**
   ```bash
   npm run tauri dev
   ```

### First Launch

When you first launch the application:

1. The Python backend will start automatically
2. You'll see a "Backend Online" status in the header
3. The home screen will display with three main sections:
   - **Profiles**: Manage your anonymous identities
   - **Browser**: Launch anonymous browsers
   - **Leak Detection**: Test your privacy protection

---

## Profile Management

### What is a Profile?

A profile is a persistent anonymous identity with:
- **Unique fingerprint**: Canvas, WebGL, audio signatures
- **Consistent user agent**: Browser identification
- **Location data**: Timezone, language, geolocation
- **Persistent storage**: Reuse the same identity across sessions

### Creating a Profile

1. Click the **"Profiles"** tab
2. Click **"Create Profile"** button
3. Enter a profile name (e.g., "Work Profile", "Shopping")
4. Optionally enter a location hint (e.g., "New York", "London")
5. Click **"Create Profile"**

The system will automatically generate:
- Realistic user agent
- Matching timezone and language
- Randomized fingerprints
- Unique profile ID

### Managing Profiles

**View Profiles:**
- All profiles are displayed as cards
- Shows profile name, location, and last used date
- Active profiles have a green checkmark

**Load Profile:**
- Click on any profile card to view details
- See full fingerprint information
- View location and browser settings

**Delete Profile:**
- Click the trash icon on a profile card
- Confirm deletion
- Profile is permanently removed

**Search Profiles:**
- Use the search bar to filter by name
- Real-time filtering as you type

---

## Browser Launcher

### Launching an Anonymous Browser

1. Click the **"Browser"** tab
2. Select a profile from the dropdown
3. Enter a starting URL (optional, defaults to Google)
4. Click **"Launch Anonymous Browser"**

The browser will open with:
- ✅ Profile's fingerprint applied
- ✅ WebRTC blocking enabled
- ✅ Automation flags removed
- ✅ Canvas/WebGL randomization active

### Browser Features

**Anti-Detection:**
- `navigator.webdriver` is hidden
- Automation flags removed
- Realistic plugin list
- Proper language settings

**Fingerprint Protection:**
- Canvas fingerprint randomized
- WebGL fingerprint randomized
- Audio fingerprint randomized
- Consistent per profile

**Privacy Features:**
- WebRTC IP leak prevention
- DNS leak protection
- Timezone spoofing
- User agent spoofing

### Active Sessions

The "Active Sessions" panel shows:
- Profile name
- Browser status (Launching, Running, Stopped, Error)
- Process ID (PID)
- Current URL

---

## Leak Detection

### Running Tests

1. Click the **"Leak Detection"** tab
2. Click **"Run All Tests"**
3. Wait for tests to complete (1-3 seconds)
4. Review results

### Test Categories

#### 🌐 WebRTC Leak
**What it tests:** Whether your real IP is exposed through WebRTC

**Pass criteria:** No IP leak detected

**What to do if it fails:**
- Ensure WebRTC blocking is enabled
- Check browser settings
- Verify proxy/VPN configuration

#### 🔍 DNS Leak
**What it tests:** Whether DNS requests reveal your location

**Pass criteria:** DNS queries routed through anonymity network

**What to do if it fails:**
- Check DNS settings
- Verify VPN/proxy DNS
- Use custom DNS servers

#### 🎨 Canvas Fingerprint
**What it tests:** Canvas API fingerprinting protection

**Pass criteria:** Randomization enabled

**What to do if it fails:**
- Ensure profile is loaded
- Check browser launch settings

#### 👁️ WebGL Fingerprint
**What it tests:** WebGL API fingerprinting protection

**Pass criteria:** Randomization enabled

**What to do if it fails:**
- Verify profile settings
- Check WebGL support

#### 🔊 Audio Fingerprint
**What it tests:** Audio API fingerprinting protection

**Pass criteria:** Randomization enabled

#### 🕐 Timezone Leak
**What it tests:** Whether timezone reveals your location

**Pass criteria:** Timezone matches profile location

#### 🤖 Automation Detection
**What it tests:** Whether browser appears automated

**Pass criteria:** Automation flags hidden

### Understanding Results

**Status Indicators:**
- 🟢 **Pass**: Test passed, no issues
- 🟡 **Warning**: Potential issue, review details
- 🔴 **Fail**: Critical issue, action required

**Overall Status:**
- **All Tests Passed**: Your anonymity is protected
- **Warnings Detected**: Some issues need attention
- **Tests Failed**: Critical leaks detected

### Exporting Results

Click **"Export Results"** to save test results as JSON:
- Timestamp included
- All test details
- Can be shared for troubleshooting

---

## Best Practices

### Profile Usage

1. **Use Different Profiles for Different Activities**
   - Work profile for professional browsing
   - Shopping profile for e-commerce
   - Research profile for general browsing

2. **Don't Reuse Profiles Across Contexts**
   - Each profile should have a specific purpose
   - Avoid mixing activities in one profile

3. **Regularly Update Profiles**
   - Delete old profiles
   - Create fresh profiles periodically
   - Update location hints as needed

### Browser Usage

1. **Always Run Leak Tests First**
   - Test before important activities
   - Verify protection is working
   - Check after configuration changes

2. **Use HTTPS Everywhere**
   - Prefer HTTPS sites
   - Avoid HTTP when possible
   - Check for SSL/TLS

3. **Combine with VPN/Proxy**
   - Use VPN for network-level protection
   - Configure SOCKS5 proxy if needed
   - Test for DNS leaks

### Privacy Hygiene

1. **Clear Browser Data Regularly**
   - Close browser when done
   - Don't save passwords in browser
   - Use incognito/private mode

2. **Avoid Logging Into Personal Accounts**
   - Don't mix anonymous and personal browsing
   - Use separate profiles for logged-in activities
   - Be aware of tracking cookies

3. **Monitor for Leaks**
   - Run leak tests regularly
   - Check for new leak types
   - Stay updated on privacy news

---

## Troubleshooting

### Backend Not Connecting

**Symptoms:** "Backend Offline" status

**Solutions:**
1. Check Python is installed: `python3 --version`
2. Verify dependencies: `pip list | grep playwright`
3. Restart the application
4. Check logs in `python-backend/sidecar.log`

### Browser Won't Launch

**Symptoms:** Error when clicking "Launch Browser"

**Solutions:**
1. Install Playwright browsers: `playwright install chromium`
2. Check profile exists
3. Verify Python backend is running
4. Check system resources (RAM, CPU)

### Leak Tests Failing

**Symptoms:** Red "Failed" status on tests

**Solutions:**
1. Check internet connection
2. Verify VPN/proxy is active
3. Restart browser
4. Create new profile

### Profile Creation Fails

**Symptoms:** Error when creating profile

**Solutions:**
1. Check profile name is unique
2. Verify database permissions
3. Check disk space
4. Restart Python backend

---

## FAQ

### Q: How many profiles can I create?
**A:** Unlimited. Profiles are stored in a SQLite database with minimal disk usage.

### Q: Can I export/import profiles?
**A:** Not yet. This feature is planned for v2.0.

### Q: Does this work with Tor?
**A:** Yes! You can configure Tor as a SOCKS5 proxy.

### Q: Is this 100% anonymous?
**A:** No tool provides 100% anonymity. This tool reduces fingerprinting and leaks, but you should combine it with VPN/Tor and good privacy practices.

### Q: Can websites detect I'm using this?
**A:** The tool removes common automation flags and randomizes fingerprints, but sophisticated detection is always possible.

### Q: What browsers are supported?
**A:** Currently Chromium via Playwright. Firefox support planned for v2.0.

### Q: Can I use this on mobile?
**A:** Not yet. Desktop only (Windows, macOS, Linux).

### Q: Is my data encrypted?
**A:** Profile data is stored locally in SQLite. For encryption, use full-disk encryption on your system.

### Q: How do I update?
**A:** Pull latest code and run `npm install`. Database migrations are automatic.

### Q: Can I contribute?
**A:** Yes! See CONTRIBUTING.md for guidelines.

---

## Keyboard Shortcuts

- **Ctrl+1**: Home tab
- **Ctrl+2**: Profiles tab
- **Ctrl+3**: Browser tab
- **Ctrl+4**: Leak Detection tab
- **Ctrl+N**: New profile
- **Ctrl+T**: Run leak tests
- **Ctrl+L**: Launch browser
- **Ctrl+R**: Refresh profiles

*(Shortcuts coming in v1.1)*

---

## Support

**Issues:** https://github.com/your-repo/issues  
**Discussions:** https://github.com/your-repo/discussions  
**Email:** support@anonymity-browser.com

---

## Privacy Notice

This tool is designed to enhance your privacy, but:
- No tool provides perfect anonymity
- Always combine with VPN/Tor
- Be aware of your threat model
- Don't rely solely on technical tools
- Practice good operational security

**Remember:** The best privacy tool is awareness and good practices.

---

**Happy Anonymous Browsing! 🎭**

