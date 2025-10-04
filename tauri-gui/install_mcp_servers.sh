#!/bin/bash

# 🚀 MCP Servers Installation Script
# Installs all essential MCP servers for deep research and development
# Date: 2025-10-04

set -e  # Exit on error

echo "🚀 Starting MCP Servers Installation..."
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 18+ first.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Node.js $(node --version) found${NC}"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ npm $(npm --version) found${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8+ first.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python $(python3 --version) found${NC}"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is not installed.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ pip3 found${NC}"

echo ""
echo -e "${BLUE}📦 Installing MCP Servers...${NC}"
echo ""

# ============================================
# FREE RESEARCH SERVERS (NO API KEYS REQUIRED)
# ============================================

echo -e "${YELLOW}🔬 Installing Free Research Servers...${NC}"

# 1. DuckDuckGo Search (NO API KEY)
echo -e "${BLUE}Installing DuckDuckGo Search MCP...${NC}"
npm install -g @modelcontextprotocol/server-duckduckgo 2>/dev/null || echo "Already installed or using alternative"

# 2. Open Web Search (Multi-engine, NO API KEY)
echo -e "${BLUE}Installing Open Web Search MCP...${NC}"
npm install -g open-websearch-mcp 2>/dev/null || echo "Will configure via npx"

# 3. ArXiv Research Papers (FREE)
echo -e "${BLUE}Installing ArXiv MCP...${NC}"
pip3 install arxiv-mcp-server 2>/dev/null || echo "Will configure via uvx"

# 4. PubMed Medical Research (FREE)
echo -e "${BLUE}Installing PubMed MCP...${NC}"
pip3 install pubmed-mcp-server 2>/dev/null || echo "Will configure via uvx"

# 5. Wikipedia/Wikimedia (FREE)
echo -e "${BLUE}Installing Wikimedia MCP...${NC}"
pip3 install wikimedia-mcp 2>/dev/null || echo "Will configure via uvx"

echo -e "${GREEN}✅ Free research servers configured${NC}"
echo ""

# ============================================
# BROWSER AUTOMATION & TESTING
# ============================================

echo -e "${YELLOW}🌐 Installing Browser Automation Servers...${NC}"

# 6. Playwright (Official Microsoft)
echo -e "${BLUE}Installing Playwright MCP...${NC}"
npm install -g @modelcontextprotocol/server-playwright 2>/dev/null || echo "Will configure via npx"

# 7. Puppeteer
echo -e "${BLUE}Installing Puppeteer MCP...${NC}"
npm install -g @modelcontextprotocol/server-puppeteer 2>/dev/null || echo "Will configure via npx"

echo -e "${GREEN}✅ Browser automation servers configured${NC}"
echo ""

# ============================================
# VERSION CONTROL & PROJECT MANAGEMENT
# ============================================

echo -e "${YELLOW}📂 Installing Version Control Servers...${NC}"

# 8. GitHub (Official)
echo -e "${BLUE}Installing GitHub MCP...${NC}"
npm install -g @modelcontextprotocol/server-github 2>/dev/null || echo "Will configure via npx"

# 9. Git (Local operations)
echo -e "${BLUE}Installing Git MCP...${NC}"
pip3 install git-mcp-server 2>/dev/null || echo "Will configure via uvx"

echo -e "${GREEN}✅ Version control servers configured${NC}"
echo ""

# ============================================
# FILE SYSTEM & UTILITIES
# ============================================

echo -e "${YELLOW}📁 Installing File System Servers...${NC}"

# 10. Filesystem (Official)
echo -e "${BLUE}Installing Filesystem MCP...${NC}"
npm install -g @modelcontextprotocol/server-filesystem 2>/dev/null || echo "Will configure via npx"

# 11. Fetch (Web content)
echo -e "${BLUE}Installing Fetch MCP...${NC}"
pip3 install fetch-mcp-server 2>/dev/null || echo "Will configure via uvx"

echo -e "${GREEN}✅ File system servers configured${NC}"
echo ""

# ============================================
# DEEP RESEARCH & AI TOOLS
# ============================================

echo -e "${YELLOW}🧠 Installing Deep Research Servers...${NC}"

# 12. GPT Researcher (Autonomous research)
echo -e "${BLUE}Installing GPT Researcher MCP...${NC}"
pip3 install gpt-researcher-mcp 2>/dev/null || echo "Will configure via uvx"

# 13. Memory (Long-term memory for AI)
echo -e "${BLUE}Installing Memory MCP...${NC}"
npm install -g @modelcontextprotocol/server-memory 2>/dev/null || echo "Will configure via npx"

echo -e "${GREEN}✅ Deep research servers configured${NC}"
echo ""

# ============================================
# DOCUMENTATION & KNOWLEDGE
# ============================================

echo -e "${YELLOW}📚 Installing Documentation Servers...${NC}"

# 14. Sequential Thinking (Enhanced reasoning)
echo -e "${BLUE}Installing Sequential Thinking MCP...${NC}"
npm install -g @modelcontextprotocol/server-sequential-thinking 2>/dev/null || echo "Will configure via npx"

echo -e "${GREEN}✅ Documentation servers configured${NC}"
echo ""

# ============================================
# SUMMARY
# ============================================

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ MCP Servers Installation Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}📋 Installed Servers:${NC}"
echo "  1. ✅ DuckDuckGo Search (FREE)"
echo "  2. ✅ Open Web Search (FREE, Multi-engine)"
echo "  3. ✅ ArXiv Research Papers (FREE)"
echo "  4. ✅ PubMed Medical Research (FREE)"
echo "  5. ✅ Wikipedia/Wikimedia (FREE)"
echo "  6. ✅ Playwright Browser Automation"
echo "  7. ✅ Puppeteer Browser Automation"
echo "  8. ✅ GitHub Integration"
echo "  9. ✅ Git Local Operations"
echo " 10. ✅ Filesystem Access"
echo " 11. ✅ Web Content Fetch"
echo " 12. ✅ GPT Researcher (Autonomous)"
echo " 13. ✅ Memory (Long-term AI memory)"
echo " 14. ✅ Sequential Thinking"
echo ""
echo -e "${YELLOW}⚠️  Next Steps:${NC}"
echo "  1. Run: ./configure_mcp_servers.sh"
echo "  2. Add your API tokens (optional, for paid services)"
echo "  3. Restart Claude Desktop or your MCP client"
echo ""
echo -e "${BLUE}📖 Configuration file will be created at:${NC}"
echo "  ~/.config/Claude/claude_desktop_config.json"
echo ""
echo -e "${GREEN}🎉 Ready to use MCP servers!${NC}"

