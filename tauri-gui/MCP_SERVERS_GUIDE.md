# 🚀 MCP Servers Complete Setup Guide

**Date:** 2025-10-04  
**Purpose:** Complete guide to install, configure, and use MCP servers for deep research and development

---

## 📋 Quick Start (3 Steps)

```bash
# 1. Install all MCP servers
cd /home/eddie/anon_best/tauri-gui
chmod +x install_mcp_servers.sh
./install_mcp_servers.sh

# 2. Configure for Claude Desktop
chmod +x configure_mcp_servers.sh
./configure_mcp_servers.sh

# 3. Test installation
chmod +x test_mcp_servers.sh
./test_mcp_servers.sh

# 4. Restart Claude Desktop
# Then start using MCP servers!
```

---

## 🎯 What You Get

### **FREE Research Servers (No API Keys Required)**

1. **DuckDuckGo Search** 🔍
   - Free web search
   - No rate limits
   - Privacy-focused
   - **Use:** "Search DuckDuckGo for latest React best practices"

2. **Open Web Search** 🌐
   - Multi-engine: Bing, Baidu, DuckDuckGo, Brave
   - No API keys needed
   - Aggregated results
   - **Use:** "Search multiple engines for Tauri security best practices"

3. **ArXiv** 📚
   - Academic research papers
   - Computer science, physics, math
   - Free full-text access
   - **Use:** "Find recent papers on browser fingerprinting from ArXiv"

4. **PubMed** 🏥
   - Medical and life sciences research
   - 35+ million citations
   - Free access
   - **Use:** "Search PubMed for privacy research papers"

5. **Wikipedia/Wikimedia** 📖
   - Encyclopedia articles
   - Structured knowledge
   - Free access
   - **Use:** "Get Wikipedia article on WebRTC"

### **Browser Automation**

6. **Playwright** 🎭
   - Microsoft official
   - Chromium, Firefox, WebKit
   - Screenshots, automation
   - **Use:** "Navigate to browserleaks.com and take a screenshot"

7. **Puppeteer** 🎪
   - Google Chrome automation
   - Headless browser
   - **Use:** "Test my website with Puppeteer"

### **Development Tools**

8. **GitHub** 🐙
   - Repository management
   - Issues, PRs, code search
   - Requires token (free)
   - **Use:** "Create a new issue in my repo"

9. **Git** 📂
   - Local Git operations
   - Commit, branch, status
   - **Use:** "Show me the git status"

10. **Filesystem** 📁
    - Read/write files
    - Directory operations
    - **Use:** "Read the contents of App.tsx"

11. **Fetch** 🌍
    - Download web content
    - Convert to markdown
    - **Use:** "Fetch and summarize this URL"

### **AI Enhancement**

12. **GPT Researcher** 🔬
    - Autonomous research agent
    - Multi-source aggregation
    - **Use:** "Do deep research on Rust async programming"

13. **Memory** 🧠
    - Long-term conversation memory
    - Context retention
    - **Use:** "Remember that I prefer TypeScript over JavaScript"

14. **Sequential Thinking** 🤔
    - Enhanced reasoning
    - Step-by-step analysis
    - **Use:** "Think through this architecture decision step by step"

---

## 🛠️ Installation Details

### Prerequisites

```bash
# Check Node.js (need 18+)
node --version

# Check Python (need 3.8+)
python3 --version

# Check npm
npm --version

# Check pip
pip3 --version
```

### Install uvx (for Python MCP servers)

```bash
# Install pipx first
pip3 install --user pipx
pipx ensurepath

# Install uvx
pipx install uvx

# Verify
uvx --version
```

### Manual Installation (if scripts fail)

```bash
# Research servers
npm install -g @modelcontextprotocol/server-duckduckgo
pip3 install arxiv-mcp-server
pip3 install pubmed-mcp-server
pip3 install wikimedia-mcp

# Browser automation
npm install -g @modelcontextprotocol/server-playwright
npm install -g @modelcontextprotocol/server-puppeteer

# Development tools
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-filesystem
pip3 install git-mcp-server
pip3 install fetch-mcp-server

# AI enhancement
pip3 install gpt-researcher-mcp
npm install -g @modelcontextprotocol/server-memory
npm install -g @modelcontextprotocol/server-sequential-thinking
```

---

## ⚙️ Configuration

### Claude Desktop Configuration

**Location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**The configuration script creates this automatically!**

### Adding GitHub Token (Optional)

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:org`, `read:user`
4. Copy token
5. Edit config file:
```json
"github": {
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_actual_token_here"
  }
}
```

---

## 🎓 Usage Examples

### Example 1: Deep Research on a Topic

```
You: "I need to research browser fingerprinting techniques. Use ArXiv, 
PubMed, and DuckDuckGo to find the latest information."

Claude: [Uses multiple MCP servers]
- Searches ArXiv for academic papers
- Searches PubMed for related research
- Searches DuckDuckGo for recent articles
- Synthesizes findings with citations
```

### Example 2: Automated Testing

```
You: "Use Playwright to test my anonymity browser at localhost:1420. 
Check if WebRTC is blocked."

Claude: [Uses Playwright MCP]
- Navigates to localhost:1420
- Runs WebRTC leak test
- Takes screenshots
- Reports results
```

### Example 3: Code Research & Implementation

```
You: "Research how to implement proxy rotation in Rust, then help me 
code it for my project."

Claude: [Uses multiple MCPs]
- Searches DuckDuckGo for Rust proxy examples
- Searches GitHub for similar implementations
- Reads your project files via Filesystem MCP
- Generates code with context
```

### Example 4: Architecture Planning

```
You: "Help me design the proxy management system. Research best 
practices, create a plan, and remember the decisions."

Claude: [Uses multiple MCPs]
- Researches via ArXiv and web search
- Uses Sequential Thinking for analysis
- Stores decisions in Memory MCP
- Can recall later: "What did we decide about proxies?"
```

---

## 🔍 Troubleshooting

### MCP Servers Not Showing Up

1. **Check config file exists:**
```bash
cat ~/.config/Claude/claude_desktop_config.json
# or on macOS:
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. **Restart Claude Desktop completely:**
   - Quit Claude Desktop (Cmd+Q on Mac)
   - Wait 5 seconds
   - Reopen Claude Desktop

3. **Check Claude Desktop logs:**
```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp*.log

# Linux
tail -f ~/.config/Claude/logs/mcp*.log
```

### Server Fails to Start

1. **Test manually:**
```bash
npx -y @modelcontextprotocol/server-duckduckgo
# Should show help or version info
```

2. **Check Node.js version:**
```bash
node --version  # Should be 18+
```

3. **Reinstall specific server:**
```bash
npm install -g @modelcontextprotocol/server-duckduckgo --force
```

### Python Servers Not Working

1. **Install uvx:**
```bash
pip3 install --user pipx
pipx install uvx
```

2. **Test Python server:**
```bash
uvx arxiv-mcp-server
```

3. **Check Python version:**
```bash
python3 --version  # Should be 3.8+
```

---

## 📊 Server Status Check

Run this to verify all servers:

```bash
./test_mcp_servers.sh
```

Expected output:
```
✅ PASS: DuckDuckGo Search
✅ PASS: Open Web Search
✅ PASS: ArXiv
✅ PASS: PubMed
✅ PASS: Wikimedia
✅ PASS: Playwright
✅ PASS: Puppeteer
⚠️  WARN: GitHub (needs token)
✅ PASS: Git
✅ PASS: Filesystem
✅ PASS: Fetch
✅ PASS: GPT Researcher
✅ PASS: Memory
✅ PASS: Sequential Thinking
```

---

## 🚀 Advanced Usage

### Combining Multiple Servers

```
You: "Research Tauri security best practices using ArXiv and web search, 
then check our current implementation in the codebase using Filesystem, 
and create a GitHub issue with recommendations."

Claude will:
1. Search ArXiv for academic papers
2. Search web for recent articles
3. Read your code files
4. Analyze findings
5. Create GitHub issue
```

### Autonomous Research Workflow

```
You: "Use GPT Researcher to do a comprehensive analysis of browser 
fingerprinting prevention techniques. Include academic sources from 
ArXiv and PubMed."

Claude will:
1. Activate GPT Researcher MCP
2. Query multiple sources automatically
3. Synthesize findings
4. Provide comprehensive report with citations
```

---

## 📚 Additional Resources

- **MCP Documentation:** https://modelcontextprotocol.io/
- **Awesome MCP Servers:** https://github.com/punkpeye/awesome-mcp-servers
- **Claude Desktop:** https://claude.ai/download

---

## ✅ Checklist

- [ ] Installed all MCP servers (`./install_mcp_servers.sh`)
- [ ] Configured Claude Desktop (`./configure_mcp_servers.sh`)
- [ ] Tested servers (`./test_mcp_servers.sh`)
- [ ] Restarted Claude Desktop
- [ ] Added GitHub token (optional)
- [ ] Tested with a simple query
- [ ] Verified servers appear in Claude

---

**🎉 You're ready to use MCP servers for deep research and development!**

**Try it now:** "Search ArXiv for recent papers on browser privacy"

