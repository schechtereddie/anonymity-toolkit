#!/bin/bash

# 🔧 MCP Servers Configuration Script
# Creates configuration file for Claude Desktop and other MCP clients
# Date: 2025-10-04

set -e

echo "🔧 Configuring MCP Servers..."
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Detect OS and set config path
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
    echo -e "${BLUE}📍 Detected macOS${NC}"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    CONFIG_DIR="$HOME/.config/Claude"
    echo -e "${BLUE}📍 Detected Linux${NC}"
else
    echo -e "${RED}❌ Unsupported OS${NC}"
    exit 1
fi

CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

# Create config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

echo -e "${BLUE}📝 Creating configuration file...${NC}"
echo -e "${YELLOW}Location: $CONFIG_FILE${NC}"
echo ""

# Create comprehensive configuration
cat > "$CONFIG_FILE" << 'EOF'
{
  "mcpServers": {
    "duckduckgo-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-duckduckgo"],
      "description": "Free web search using DuckDuckGo (NO API KEY)"
    },
    "open-web-search": {
      "command": "npx",
      "args": ["-y", "open-websearch-mcp"],
      "description": "Multi-engine search: Bing, Baidu, DuckDuckGo, Brave (NO API KEY)"
    },
    "arxiv": {
      "command": "uvx",
      "args": ["arxiv-mcp-server"],
      "description": "Search and download academic papers from arXiv (FREE)"
    },
    "pubmed": {
      "command": "uvx",
      "args": ["pubmed-mcp-server"],
      "description": "Search medical and life sciences papers from PubMed (FREE)"
    },
    "wikimedia": {
      "command": "uvx",
      "args": ["wikimedia-mcp"],
      "description": "Access Wikipedia articles and Wikimedia content (FREE)"
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"],
      "description": "Browser automation with Playwright (Microsoft official)"
    },
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
      "description": "Browser automation with Puppeteer"
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_GITHUB_TOKEN_HERE>"
      },
      "description": "GitHub repository management (requires token)"
    },
    "git": {
      "command": "uvx",
      "args": ["git-mcp-server"],
      "description": "Local Git operations"
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/eddie/anon_best"],
      "description": "Access project files"
    },
    "fetch": {
      "command": "uvx",
      "args": ["fetch-mcp-server"],
      "description": "Fetch web content and convert to markdown"
    },
    "gpt-researcher": {
      "command": "uvx",
      "args": ["gpt-researcher-mcp"],
      "description": "Autonomous deep research agent"
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "description": "Long-term memory for AI conversations"
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "description": "Enhanced reasoning and step-by-step thinking"
    }
  }
}
EOF

echo -e "${GREEN}✅ Configuration file created!${NC}"
echo ""

# Create a backup
if [ -f "$CONFIG_FILE.backup" ]; then
    echo -e "${YELLOW}⚠️  Backup already exists, skipping...${NC}"
else
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
    echo -e "${GREEN}✅ Backup created: $CONFIG_FILE.backup${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📋 Configuration Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}✅ FREE Research Servers (No API Keys):${NC}"
echo "  • DuckDuckGo Search"
echo "  • Open Web Search (Multi-engine)"
echo "  • ArXiv (Academic papers)"
echo "  • PubMed (Medical research)"
echo "  • Wikipedia/Wikimedia"
echo ""
echo -e "${GREEN}✅ Browser Automation:${NC}"
echo "  • Playwright"
echo "  • Puppeteer"
echo ""
echo -e "${GREEN}✅ Development Tools:${NC}"
echo "  • GitHub (requires token)"
echo "  • Git (local)"
echo "  • Filesystem"
echo "  • Fetch"
echo ""
echo -e "${GREEN}✅ AI Enhancement:${NC}"
echo "  • GPT Researcher"
echo "  • Memory"
echo "  • Sequential Thinking"
echo ""
echo -e "${YELLOW}⚠️  Optional: Add API Tokens${NC}"
echo ""
echo "To add your GitHub token:"
echo "  1. Create token at: https://github.com/settings/tokens"
echo "  2. Edit: $CONFIG_FILE"
echo "  3. Replace <YOUR_GITHUB_TOKEN_HERE> with your token"
echo ""
echo -e "${BLUE}🔄 Next Steps:${NC}"
echo "  1. Restart Claude Desktop (if using)"
echo "  2. Test servers with: ./test_mcp_servers.sh"
echo "  3. Start using MCP servers in your AI conversations!"
echo ""
echo -e "${GREEN}🎉 Configuration complete!${NC}"

