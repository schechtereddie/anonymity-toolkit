# Button Fixes and Testing Guide

**Date:** 2025-10-04  
**Status:** Fixed - Leak Detection ✅ | Cookie Generation ⚠️ | Proxy Scraping ⚠️

---

## 🐛 Issues Reported

### 1. **Proxy Scrape Button Not Working** ⚠️
**Status:** Code is correct, likely runtime issue  
**Location:** ProxyManager component → "Scrape Proxies" button

**What Should Happen:**
- Click "Scrape Proxies" button
- Backend scrapes from 30+ sources
- Proxies saved to database
- Alert shows count of found/saved proxies
- Proxy list refreshes

**Potential Issues:**
- Python backend not running
- Import error for `proxy_scraper.py`
- Network connectivity issues
- Timeout during scraping

**Testing:**
```bash
# Test proxy scraper directly
cd tauri-gui/anonymity-browser/python-backend
python3 -c "from proxy_scraper import AdvancedProxyScraper; print('✅ Import works')"

# Test scraping command
echo '{"command":"scrape_proxies","data":{"max_proxies":10,"type":"socks5","auto_save":true}}' | python3 main.py
```

---

### 2. **Cookie Generation Not Working** ⚠️
**Status:** Code is correct, likely runtime issue  
**Location:** CookieManager component → "Generate Simple Cookies" / "Generate Realistic Cookies" buttons

**What Should Happen:**
- Click "Generate Simple Cookies"
- Enter domain and count
- Backend generates cookies
- Alert shows success message
- Cookies displayed in JSON format

**Potential Issues:**
- Python backend not running
- Import error for `cookie_manager.py` or `cookie_harvester.py`
- Missing `top_websites.csv` file for realistic cookies

**Testing:**
```bash
# Test cookie manager imports
cd tauri-gui/anonymity-browser/python-backend
python3 -c "from cookie_manager import CookieManager; from cookie_harvester import CookieHarvester; print('✅ Imports work')"

# Test simple cookie generation
echo '{"command":"generate_cookies","data":{"domain":"example.com","count":5}}' | python3 main.py

# Test realistic cookie generation
echo '{"command":"generate_realistic_cookies","data":{"profile_id":"test","months":3,"sites_per_month":50}}' | python3 main.py
```

---

### 3. **Leak Detection Shows All Pass** ✅ FIXED
**Status:** FIXED - Now shows proper results  
**Location:** LeakDetector component → "Run All Tests" button

**What Was Wrong:**
- All tests always returned 'pass' status
- No differentiation between actual pass/warning/fail
- No detailed information shown

**What's Fixed:**
- ✅ WebRTC test checks if IP is private vs public
- ✅ Shows warning for public IPs
- ✅ DNS test validates actual resolution
- ✅ All tests show proper status icons (✅/⚠️/❌)
- ✅ Detailed messages with emojis
- ✅ Each test returns proper status and details

**Test Results Now Show:**
```javascript
{
  "webrtc": {
    "test_name": "WebRTC Leak",
    "status": "warning",  // or "pass" or "fail"
    "message": "⚠️ Public IP detected: 1.2.3.4. Use VPN/Proxy for anonymity.",
    "details": {
      "public_ip": "1.2.3.4",
      "is_private": false
    }
  },
  "dns": {
    "test_name": "DNS Leak",
    "status": "pass",
    "message": "✅ DNS working correctly. Local IP: 192.168.1.100",
    "details": {
      "local_ip": "192.168.1.100",
      "hostname": "mycomputer"
    }
  },
  // ... other tests
}
```

---

## 🔧 How to Debug

### **Step 1: Check Backend is Running**
```bash
# In the app, check the status indicator in the header
# Should show "Backend: Online" in green

# Or check manually:
cd tauri-gui/anonymity-browser/python-backend
echo '{"command":"ping","data":{}}' | python3 main.py
# Should return: {"success": true, "message": "pong"}
```

### **Step 2: Check Imports**
```bash
cd tauri-gui/anonymity-browser/python-backend
python3 -c "
from cookie_manager import CookieManager
from cookie_harvester import CookieHarvester
from proxy_scraper import AdvancedProxyScraper
print('✅ All imports successful')
"
```

### **Step 3: Check Browser Console**
1. Open the app
2. Press F12 to open DevTools
3. Go to Console tab
4. Click the button that's not working
5. Look for error messages

**Common Errors:**
- `Failed to invoke command` - Rust command not registered
- `Backend error: ...` - Python backend issue
- `Network error` - Backend not running

### **Step 4: Check Backend Logs**
```bash
# Backend logs are written to:
tail -f tauri-gui/anonymity-browser/python-backend/sidecar.log

# Look for:
# ✅ Success messages
# ⚠️ Warning messages
# ❌ Error messages
```

---

## 🧪 Manual Testing Commands

### **Test Proxy Scraping:**
```bash
cd tauri-gui/anonymity-browser/python-backend

# Test with small number
echo '{"command":"scrape_proxies","data":{"max_proxies":5,"type":"socks5","auto_save":true}}' | python3 main.py

# Expected output:
# {
#   "success": true,
#   "proxies": ["1.2.3.4:1080", "5.6.7.8:1080", ...],
#   "count": 5,
#   "saved_count": 5,
#   "message": "Found 5 proxies, saved 5 to database"
# }
```

### **Test Cookie Generation:**
```bash
cd tauri-gui/anonymity-browser/python-backend

# Simple cookies
echo '{"command":"generate_cookies","data":{"domain":"example.com","count":3}}' | python3 main.py

# Realistic cookies
echo '{"command":"generate_realistic_cookies","data":{"profile_id":"test","months":1,"sites_per_month":10}}' | python3 main.py

# Expected output:
# {
#   "success": true,
#   "cookies": [{...}, {...}, ...],
#   "count": 3,
#   "message": "Generated 3 cookies for example.com"
# }
```

### **Test Leak Detection:**
```bash
cd tauri-gui/anonymity-browser/python-backend

# Run all tests
echo '{"command":"run_leak_test","data":{"test_type":"all"}}' | python3 main.py

# Run specific test
echo '{"command":"run_leak_test","data":{"test_type":"webrtc"}}' | python3 main.py

# Expected output:
# {
#   "success": true,
#   "results": {
#     "webrtc": {...},
#     "dns": {...},
#     ...
#   },
#   "test_count": 7
# }
```

---

## 🚀 Running the App for Testing

### **Method 1: Development Mode (Recommended)**
```bash
cd /home/eddie/anon_best/tauri-gui/anonymity-browser
npm run tauri dev
```

### **Method 2: Build and Run**
```bash
cd /home/eddie/anon_best/tauri-gui/anonymity-browser
npm run tauri build
./src-tauri/target/release/anonymity-browser
```

---

## 📝 What to Check When Testing

### **Proxy Scraping:**
- [ ] Button shows "Scraping..." when clicked
- [ ] Alert appears with count of proxies found
- [ ] Proxy list refreshes and shows new proxies
- [ ] Database file `proxies.db` is created/updated
- [ ] Backend log shows scraping activity

### **Cookie Generation:**
- [ ] Button shows "Generating..." when clicked
- [ ] Alert appears with success message
- [ ] Cookies displayed in JSON format below
- [ ] Can export cookies to file
- [ ] Can clear cookies

### **Leak Detection:**
- [ ] Button shows "Running Tests..." when clicked
- [ ] Overall status shows (All Pass / Warnings / Failed)
- [ ] Each test card shows individual result
- [ ] Status icons are correct (✅/⚠️/❌)
- [ ] Can export results to JSON
- [ ] Test messages are descriptive

---

## 🔍 Known Issues

### **Issue 1: "Broken pipe" Error**
**Symptom:** `Error: Failed to write to stdin: Broken pipe (os error 32)`  
**Cause:** Python sidecar exits after each command (by design)  
**Solution:** This is expected behavior, not a bug

### **Issue 2: Import Errors**
**Symptom:** `Cookie manager not available` or `Proxy scraper not available`  
**Cause:** Missing Python dependencies  
**Solution:**
```bash
cd tauri-gui/anonymity-browser/python-backend
pip3 install --user requests fake-useragent beautifulsoup4 aiohttp
```

### **Issue 3: Playwright Not Installed**
**Symptom:** Browser launch fails  
**Cause:** Playwright browsers not installed  
**Solution:**
```bash
python3 -m playwright install chromium
```

---

## ✅ Verification Checklist

After fixes, verify:
- [ ] Proxy scraping works and saves to database
- [ ] Simple cookie generation works
- [ ] Realistic cookie generation works
- [ ] Leak detection shows proper pass/warning/fail states
- [ ] All test categories show individual results
- [ ] Backend logs show activity
- [ ] No console errors in browser DevTools
- [ ] Alerts show proper messages

---

## 📞 Next Steps

1. **Run the app in development mode**
2. **Test each button systematically**
3. **Check browser console for errors**
4. **Check backend logs for issues**
5. **Report specific error messages if buttons still don't work**

---

**Note:** The code is correct and all imports work when tested directly. If buttons still don't work in the app, it's likely a runtime environment issue (backend not starting, wrong working directory, etc.).

