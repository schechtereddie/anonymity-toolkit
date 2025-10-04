#!/bin/bash
# Pre-Test Environment Check Script
# Verifies all dependencies and environment setup before testing

echo "🔍 Anonymity Browser - Pre-Test Environment Check"
echo "=================================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0
WARN=0

# Function to check command
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✅ $1 is installed${NC}"
        ((PASS++))
        return 0
    else
        echo -e "${RED}❌ $1 is NOT installed${NC}"
        ((FAIL++))
        return 1
    fi
}

# Function to check version
check_version() {
    local cmd=$1
    local version=$($cmd 2>&1)
    echo -e "${GREEN}   Version: $version${NC}"
}

echo "1️⃣  Checking System Commands..."
echo "--------------------------------"
check_command "node" && check_version "node --version"
check_command "npm" && check_version "npm --version"
check_command "python3" && check_version "python3 --version"
check_command "pip3" && check_version "pip3 --version"
check_command "cargo" && check_version "cargo --version"
check_command "rustc" && check_version "rustc --version"
echo ""

echo "2️⃣  Checking Flatpak Status..."
echo "--------------------------------"
if [ -z "$FLATPAK_ID" ]; then
    echo -e "${GREEN}✅ NOT running in Flatpak (Good!)${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ Running in Flatpak: $FLATPAK_ID${NC}"
    echo -e "${YELLOW}   ⚠️  Browser launching may not work!${NC}"
    ((FAIL++))
fi
echo ""

echo "3️⃣  Checking Python Packages..."
echo "--------------------------------"
python3 -c "import playwright" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ playwright is installed${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ playwright is NOT installed${NC}"
    echo -e "${YELLOW}   Run: pip3 install --user playwright${NC}"
    ((FAIL++))
fi

python3 -c "import requests" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ requests is installed${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ requests is NOT installed${NC}"
    echo -e "${YELLOW}   Run: pip3 install --user requests${NC}"
    ((FAIL++))
fi

python3 -c "import sqlite3" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ sqlite3 is installed${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ sqlite3 is NOT installed${NC}"
    ((FAIL++))
fi
echo ""

echo "4️⃣  Checking Playwright Browsers..."
echo "--------------------------------"
if [ -d "$HOME/.cache/ms-playwright" ]; then
    echo -e "${GREEN}✅ Playwright browsers directory exists${NC}"
    ((PASS++))
    
    if [ -d "$HOME/.cache/ms-playwright/chromium-"* ]; then
        echo -e "${GREEN}✅ Chromium browser installed${NC}"
        ((PASS++))
    else
        echo -e "${RED}❌ Chromium browser NOT installed${NC}"
        echo -e "${YELLOW}   Run: python3 -m playwright install chromium${NC}"
        ((FAIL++))
    fi
else
    echo -e "${RED}❌ Playwright browsers NOT installed${NC}"
    echo -e "${YELLOW}   Run: python3 -m playwright install chromium${NC}"
    ((FAIL++))
fi
echo ""

echo "5️⃣  Checking Project Files..."
echo "--------------------------------"
if [ -f "package.json" ]; then
    echo -e "${GREEN}✅ package.json exists${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ package.json NOT found${NC}"
    echo -e "${YELLOW}   Are you in the correct directory?${NC}"
    ((FAIL++))
fi

if [ -d "node_modules" ]; then
    echo -e "${GREEN}✅ node_modules exists${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ node_modules NOT found${NC}"
    echo -e "${YELLOW}   Run: npm install${NC}"
    ((FAIL++))
fi

if [ -f "python-backend/main.py" ]; then
    echo -e "${GREEN}✅ Python backend exists${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ Python backend NOT found${NC}"
    ((FAIL++))
fi

if [ -d "src-tauri" ]; then
    echo -e "${GREEN}✅ Tauri backend exists${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ Tauri backend NOT found${NC}"
    ((FAIL++))
fi
echo ""

echo "6️⃣  Checking Ports..."
echo "--------------------------------"
if lsof -Pi :1420 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port 1420 is already in use${NC}"
    echo -e "${YELLOW}   Process: $(lsof -Pi :1420 -sTCP:LISTEN | tail -n 1)${NC}"
    ((WARN++))
else
    echo -e "${GREEN}✅ Port 1420 is available${NC}"
    ((PASS++))
fi
echo ""

echo "7️⃣  Testing Python Backend..."
echo "--------------------------------"
cd python-backend 2>/dev/null
if [ $? -eq 0 ]; then
    echo '{"command":"ping","data":{}}' | timeout 5 python3 main.py 2>/dev/null | grep -q "success"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Python backend responds to ping${NC}"
        ((PASS++))
    else
        echo -e "${YELLOW}⚠️  Python backend ping test inconclusive${NC}"
        ((WARN++))
    fi
    cd ..
else
    echo -e "${RED}❌ Cannot access python-backend directory${NC}"
    ((FAIL++))
fi
echo ""

echo "=================================================="
echo "📊 Test Summary"
echo "=================================================="
echo -e "${GREEN}✅ Passed: $PASS${NC}"
echo -e "${RED}❌ Failed: $FAIL${NC}"
echo -e "${YELLOW}⚠️  Warnings: $WARN${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}🎉 All checks passed! Ready to test!${NC}"
    echo ""
    echo "To start testing, run:"
    echo "  npm run tauri dev"
    echo ""
    exit 0
else
    echo -e "${RED}❌ Some checks failed. Please fix the issues above.${NC}"
    echo ""
    echo "Quick fixes:"
    echo "  1. Install Python packages: pip3 install --user playwright requests"
    echo "  2. Install Playwright browsers: python3 -m playwright install chromium"
    echo "  3. Install Node modules: npm install"
    echo ""
    exit 1
fi

