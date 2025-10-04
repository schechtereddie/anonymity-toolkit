# 🧪 Testing Outside Flatpak - Complete Guide

**Date:** 2025-10-04  
**Purpose:** Verify all features work in native environment  
**Status:** Ready for Testing

---

## 📋 Pre-Testing Checklist

### 1. **System Requirements**
- [ ] Linux system (Ubuntu 20.04+ or Pop!_OS)
- [ ] Node.js v22+ installed
- [ ] Python 3.8+ installed
- [ ] Rust and Cargo installed
- [ ] NOT running inside Flatpak

### 2. **Dependencies Check**
```bash
# Check versions
node --version    # Should be v22+
python3 --version # Should be 3.8+
cargo --version   # Should be installed
rustc --version   # Should be installed

# Check if running in Flatpak
echo $FLATPAK_ID  # Should be empty
```

### 3. **Python Dependencies**
```bash
cd /home/eddie/anon_best/tauri-gui/anonymity-browser/python-backend

# Install required packages
pip3 install --user playwright requests

# Install Playwright browsers
python3 -m playwright install chromium
```

---

## 🚀 Starting the Application

### Method 1: Development Mode (Recommended)
```bash
cd /home/eddie/anon_best/tauri-gui/anonymity-browser

# Start in development mode
npm run tauri dev
```

### Method 2: Build and Run
```bash
cd /home/eddie/anon_best/tauri-gui/anonymity-browser

# Build the application
npm run tauri build

# Run the built application
./src-tauri/target/release/anonymity-browser
```

---

## ✅ Testing Checklist

### **Phase 1: Basic Functionality**

#### 1.1 Application Launch
- [ ] Application window opens
- [ ] UI loads correctly
- [ ] Cyberpunk theme displays properly
- [ ] No console errors
- [ ] Backend status shows "Online"

#### 1.2 Navigation
- [ ] Home tab works
- [ ] Profiles tab works
- [ ] Browser tab works
- [ ] Leak Detection tab works
- [ ] Proxies tab works
- [ ] Settings tab works
- [ ] Tab switching is smooth

---

### **Phase 2: Profile Management**

#### 2.1 Create Profile
- [ ] Click "Create Profile" button
- [ ] Enter profile name: "TestProfile1"
- [ ] Select location: "New York"
- [ ] Profile creates successfully
- [ ] Profile appears in list
- [ ] Profile card shows correct info

#### 2.2 Load Profile
- [ ] Click on a profile card
- [ ] Profile details display
- [ ] Fingerprint information shown
- [ ] User agent displayed
- [ ] Location data correct

#### 2.3 Delete Profile
- [ ] Click delete button on profile
- [ ] Confirmation dialog appears
- [ ] Confirm deletion
- [ ] Profile removed from list

#### 2.4 Search Profiles
- [ ] Enter search term
- [ ] Results filter correctly
- [ ] Clear search works

---

### **Phase 3: Proxy Management**

#### 3.1 Add Proxy
- [ ] Click "Add Proxy" button
- [ ] Fill in proxy details:
  - Name: "Test SOCKS5"
  - Type: SOCKS5
  - Host: 127.0.0.1
  - Port: 1080
- [ ] Proxy saves successfully
- [ ] Proxy appears in list

#### 3.2 Test Proxy
- [ ] Click test button on proxy
- [ ] Testing indicator shows
- [ ] Result displays (active/inactive)
- [ ] Response time shown (if active)

#### 3.3 Delete Proxy
- [ ] Click delete button
- [ ] Confirmation dialog appears
- [ ] Proxy removed from list

---

### **Phase 4: Browser Launching** ⚠️ CRITICAL TEST

#### 4.1 Launch Without Proxy
- [ ] Go to Browser tab
- [ ] Select a profile from dropdown
- [ ] Enter URL: https://www.google.com
- [ ] Click "Launch Browser"
- [ ] Browser window opens
- [ ] Page loads correctly
- [ ] User agent is spoofed
- [ ] Fingerprint applied

#### 4.2 Launch With Proxy
- [ ] Go to Proxies tab
- [ ] Set a proxy as active
- [ ] Go to Browser tab
- [ ] Launch browser with profile
- [ ] Browser opens through proxy
- [ ] IP address is different
- [ ] Verify at: https://httpbin.org/ip

#### 4.3 Multiple Sessions
- [ ] Launch browser with Profile 1
- [ ] Launch browser with Profile 2
- [ ] Both browsers run simultaneously
- [ ] Sessions are isolated
- [ ] Different fingerprints applied

---

### **Phase 5: Leak Detection**

#### 5.1 Run All Tests
- [ ] Go to Leak Detection tab
- [ ] Click "Run All Tests"
- [ ] Tests execute successfully
- [ ] Results display for each test:
  - [ ] WebRTC Leak Test
  - [ ] DNS Leak Test
  - [ ] Canvas Fingerprint Test
  - [ ] WebGL Fingerprint Test
  - [ ] Audio Fingerprint Test
  - [ ] Timezone Leak Test
  - [ ] Automation Detection Test

#### 5.2 Individual Tests
- [ ] Run WebRTC test individually
- [ ] Run DNS test individually
- [ ] Results are accurate
- [ ] Pass/Fail status clear

#### 5.3 Export Results
- [ ] Click "Export Results"
- [ ] JSON file downloads
- [ ] File contains all test data
- [ ] Timestamp is correct

---

### **Phase 6: Settings**

#### 6.1 General Settings
- [ ] Toggle auto-start
- [ ] Toggle minimize to tray
- [ ] Toggle notifications
- [ ] Settings save correctly

#### 6.2 Privacy Settings
- [ ] Toggle clear cookies on exit
- [ ] Toggle clear history on exit
- [ ] Toggle block trackers
- [ ] Toggle block ads

#### 6.3 Automation Settings
- [ ] Enable auto-rotate profiles
- [ ] Set rotation interval: 30 minutes
- [ ] Enable auto leak testing
- [ ] Set test interval: 60 minutes

#### 6.4 Advanced Settings
- [ ] Enable debug mode
- [ ] Change log level to "debug"
- [ ] Set max concurrent browsers: 3
- [ ] Set browser timeout: 300 seconds

#### 6.5 Save Settings
- [ ] Make changes
- [ ] "Unsaved changes" warning appears
- [ ] Click "Save Changes"
- [ ] Settings persist after restart

---

### **Phase 7: Backend Integration**

#### 7.1 Python Sidecar
- [ ] Check sidecar.log file exists
- [ ] Log shows successful startup
- [ ] No error messages
- [ ] Commands logged correctly

#### 7.2 Database Files
- [ ] profiles.db exists
- [ ] proxies.db exists
- [ ] Files are not corrupted
- [ ] Data persists between sessions

#### 7.3 IPC Communication
- [ ] Frontend → Backend commands work
- [ ] Backend → Frontend responses work
- [ ] No timeout errors
- [ ] Error handling works

---

## 🐛 Common Issues & Solutions

### Issue 1: Browser Won't Launch
**Symptoms:** Click "Launch Browser" but nothing happens

**Solutions:**
```bash
# Install Playwright browsers
python3 -m playwright install chromium

# Check if Playwright is installed
python3 -c "from playwright.sync_api import sync_playwright; print('OK')"

# Check logs
tail -f /home/eddie/anon_best/tauri-gui/anonymity-browser/python-backend/sidecar.log
```

### Issue 2: Backend Not Connecting
**Symptoms:** "Backend Offline" status

**Solutions:**
```bash
# Check Python sidecar manually
cd /home/eddie/anon_best/tauri-gui/anonymity-browser/python-backend
python3 main.py

# Test with ping command
echo '{"command":"ping","data":{}}' | python3 main.py
```

### Issue 3: Proxy Test Fails
**Symptoms:** All proxies show as "inactive"

**Solutions:**
```bash
# Install requests library
pip3 install --user requests

# Test proxy manually
curl --proxy socks5://127.0.0.1:1080 https://httpbin.org/ip
```

### Issue 4: Port Already in Use
**Symptoms:** "Port 1420 already in use"

**Solutions:**
```bash
# Kill process on port 1420
lsof -ti:1420 | xargs kill -9

# Or change port in vite.config.ts
```

---

## 📊 Test Results Template

```markdown
## Test Results - [Date]

### Environment:
- OS: Pop!_OS 22.04
- Node: v22.18.0
- Python: 3.12.11
- Flatpak: No

### Phase 1: Basic Functionality
- Application Launch: ✅ PASS
- Navigation: ✅ PASS

### Phase 2: Profile Management
- Create Profile: ✅ PASS
- Load Profile: ✅ PASS
- Delete Profile: ✅ PASS
- Search Profiles: ✅ PASS

### Phase 3: Proxy Management
- Add Proxy: ✅ PASS
- Test Proxy: ⚠️ PARTIAL (needs real proxy)
- Delete Proxy: ✅ PASS

### Phase 4: Browser Launching
- Launch Without Proxy: ✅ PASS / ❌ FAIL
- Launch With Proxy: ✅ PASS / ❌ FAIL
- Multiple Sessions: ✅ PASS / ❌ FAIL

### Phase 5: Leak Detection
- Run All Tests: ✅ PASS / ❌ FAIL
- Individual Tests: ✅ PASS / ❌ FAIL
- Export Results: ✅ PASS / ❌ FAIL

### Phase 6: Settings
- All Settings: ✅ PASS / ❌ FAIL

### Phase 7: Backend Integration
- Python Sidecar: ✅ PASS / ❌ FAIL
- Database Files: ✅ PASS / ❌ FAIL
- IPC Communication: ✅ PASS / ❌ FAIL

### Issues Found:
1. [Issue description]
2. [Issue description]

### Overall Status: ✅ PASS / ⚠️ PARTIAL / ❌ FAIL
```

---

## 🎯 Success Criteria

**Minimum Requirements (Must Pass):**
- ✅ Application launches
- ✅ Backend connects
- ✅ Profile CRUD works
- ✅ Browser launches (critical!)
- ✅ Basic leak tests work

**Nice to Have:**
- ✅ Proxy integration works
- ✅ All leak tests pass
- ✅ Settings persist
- ✅ Multiple browsers work

---

## 📝 Next Steps After Testing

### If All Tests Pass:
1. Document any performance issues
2. Note any UI/UX improvements needed
3. Move to Tor integration
4. Implement automation features

### If Tests Fail:
1. Document exact failure points
2. Collect error logs
3. Fix critical issues first
4. Re-test after fixes

---

**Ready to test! Start with Phase 1 and work through systematically.** 🚀

