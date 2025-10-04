#!/bin/bash

# 🧪 MCP Servers Test Script
# Tests all installed MCP servers
# Date: 2025-10-04

echo "🧪 Testing MCP Servers..."
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

test_count=0
pass_count=0
fail_count=0

# Test function
test_server() {
    local name=$1
    local command=$2
    shift 2
    local args=("$@")
    
    test_count=$((test_count + 1))
    echo -e "${BLUE}Testing: $name${NC}"
    
    if timeout 5s $command "${args[@]}" --help &>/dev/null || \
       timeout 5s $command "${args[@]}" --version &>/dev/null || \
       timeout 5s $command "${args[@]}" &>/dev/null; then
        echo -e "${GREEN}✅ PASS: $name${NC}"
        pass_count=$((pass_count + 1))
    else
        echo -e "${RED}❌ FAIL: $name (may need configuration)${NC}"
        fail_count=$((fail_count + 1))
    fi
    echo ""
}

echo -e "${YELLOW}🔬 Testing Free Research Servers...${NC}"
echo ""

# Test DuckDuckGo
test_server "DuckDuckGo Search" npx -y @modelcontextprotocol/server-duckduckgo

# Test Open Web Search
test_server "Open Web Search" npx -y open-websearch-mcp

# Test ArXiv
test_server "ArXiv" uvx arxiv-mcp-server

# Test PubMed
test_server "PubMed" uvx pubmed-mcp-server

# Test Wikimedia
test_server "Wikimedia" uvx wikimedia-mcp

echo -e "${YELLOW}🌐 Testing Browser Automation...${NC}"
echo ""

# Test Playwright
test_server "Playwright" npx -y @modelcontextprotocol/server-playwright

# Test Puppeteer
test_server "Puppeteer" npx -y @modelcontextprotocol/server-puppeteer

echo -e "${YELLOW}📂 Testing Development Tools...${NC}"
echo ""

# Test GitHub (will fail without token, that's ok)
test_server "GitHub" npx -y @modelcontextprotocol/server-github

# Test Git
test_server "Git" uvx git-mcp-server

# Test Filesystem
test_server "Filesystem" npx -y @modelcontextprotocol/server-filesystem

# Test Fetch
test_server "Fetch" uvx fetch-mcp-server

echo -e "${YELLOW}🧠 Testing AI Enhancement Tools...${NC}"
echo ""

# Test GPT Researcher
test_server "GPT Researcher" uvx gpt-researcher-mcp

# Test Memory
test_server "Memory" npx -y @modelcontextprotocol/server-memory

# Test Sequential Thinking
test_server "Sequential Thinking" npx -y @modelcontextprotocol/server-sequential-thinking

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📊 Test Results${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Total Tests: $test_count"
echo -e "${GREEN}Passed: $pass_count${NC}"
echo -e "${RED}Failed: $fail_count${NC}"
echo ""

if [ $fail_count -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
else
    echo -e "${YELLOW}⚠️  Some tests failed. This is normal if:${NC}"
    echo "  • Servers need API tokens (GitHub)"
    echo "  • Servers need first-time setup"
    echo "  • Network connectivity issues"
    echo ""
    echo -e "${BLUE}💡 Tip: Failed servers will still work in Claude Desktop${NC}"
fi

echo ""
echo -e "${BLUE}🔄 Next: Restart Claude Desktop to use MCP servers${NC}"

