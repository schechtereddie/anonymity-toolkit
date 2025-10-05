# Quick Fix Guide - Dependency Issues

**Problem:** Buttons showing "dependencies missing" error  
**Solution:** Install missing Python packages

---

## 🚀 Quick Fix (Automatic)

Run this one command to install everything:

```bash
cd /home/eddie/anon_best/tauri-gui/anonymity-browser/python-backend
./install_dependencies.sh
```

This will:
- Install all Python packages from requirements.txt
- Install Playwright browsers (Chromium)
- Verify everything works

---

## 🔧 Manual Fix (If automatic fails)

### Step 1: Install Python Packages

```bash
cd /home/eddie/anon_best/tauri-gui/anonymity-browser/python-backend
pip3 install --user -r requirements.txt
```

This installs:
- `playwright` - Browser automation
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing (for proxy scraper)
- `aiohttp` - Async HTTP (for proxy scraper)
- `maxminddb` - Geolocation (for proxy scraper)
- `fake-useragent` - User agent generation
- `lxml` - XML/HTML parser
- `psutil` - System monitoring

### Step 2: Install Playwright Browsers

```bash
python3 -m playwright install chromium
```

### Step 3: Verify Installation

```bash
cd /home/eddie/anon_best/tauri-gui/anonymity-browser/python-backend
python3 -c "from cookie_manager import CookieManager; from proxy_scraper import AdvancedProxyScraper; print('✅ All imports successful!')"
```

If you see "✅ All imports successful!" - you're good to go!

---

## 🐛 What Was Fixed

### 1. **Profile Statistics** ✅
**Before:**
- Showed fake cookie counts (50-500 random)
- Showed fake domain counts (10-50 random)
- Showed fake leak test results

**After:**
- Shows 0 cookies (accurate - none generated yet)
- Shows 0 domains (accurate)
- No leak test result until you run tests
- Real user agent strength calculation
- Real fingerprint consistency

### 2. **Missing Dependencies** ✅
**Added to requirements.txt:**
- `maxminddb==2.5.0` (needed for proxy scraper geolocation)

**Created:**
- `install_dependencies.sh` - Easy installation script

---

## 🧪 Test After Installing

### Test 1: Cookie Generation
```bash
cd python-backend
echo '{"command":"generate_cookies","data":{"domain":"example.com","count":5}}' | python3 main.py
```

**Expected:** Should return JSON with 5 cookies

### Test 2: Proxy Scraping
```bash
echo '{"command":"scrape_proxies","data":{"max_proxies":5,"type":"socks5","auto_save":false}}' | python3 main.py
```

**Expected:** Should return JSON with proxy list

### Test 3: Run the App
```bash
cd /home/eddie/anon_best/tauri-gui/anonymity-browser
npm run tauri dev
```

Then test:
1. **Profiles Tab** → Create profile → Should show 0 cookies (not fake numbers)
2. **Cookies Tab** → Generate cookies → Should work now
3. **Proxies Tab** → Scrape proxies → Should work now
4. **Leak Detection** → Run tests → Should show real results

---

## 📋 Checklist

After running the installation:

- [ ] Run `./install_dependencies.sh` or manual steps
- [ ] Verify imports work (test command above)
- [ ] Start the app (`npm run tauri dev`)
- [ ] Check profile shows 0 cookies (not fake numbers)
- [ ] Try generating cookies - should work
- [ ] Try scraping proxies - should work
- [ ] Run leak detection - should show real results

---

## ❓ Still Having Issues?

### Issue: "pip3: command not found"
**Solution:** Install Python 3 and pip:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Issue: "Permission denied" when running install script
**Solution:** Make it executable:
```bash
chmod +x install_dependencies.sh
```

### Issue: Imports still failing
**Solution:** Check which package is missing:
```bash
python3 -c "import requests; print('requests OK')"
python3 -c "from bs4 import BeautifulSoup; print('beautifulsoup4 OK')"
python3 -c "import aiohttp; print('aiohttp OK')"
python3 -c "import maxminddb; print('maxminddb OK')"
```

Install missing ones individually:
```bash
pip3 install --user <package-name>
```

### Issue: Cookie generation still not working
**Check:**
1. Backend is running (status indicator should be green)
2. Check browser console (F12) for errors
3. Check backend logs:
   ```bash
   tail -f python-backend/sidecar.log
   ```

---

## 🎉 Summary

**What you need to do:**
1. Run `./install_dependencies.sh` in python-backend folder
2. Restart the app
3. Test the buttons

**What's fixed:**
- ✅ Profile statistics now show real data (0 cookies until generated)
- ✅ Added missing dependency (maxminddb)
- ✅ Created easy installation script
- ✅ Cookie generation will work after installing dependencies
- ✅ Proxy scraping will work after installing dependencies

**Time needed:** 2-5 minutes for installation

---

**Ready to fix it? Run this now:**

```bash
cd /home/eddie/anon_best/tauri-gui/anonymity-browser/python-backend
./install_dependencies.sh
```

Then restart your app and test! 🚀

