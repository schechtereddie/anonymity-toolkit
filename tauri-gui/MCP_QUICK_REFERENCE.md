# 🚀 MCP Servers Quick Reference Card

**Last Updated:** 2025-10-04  
**Status:** ✅ All servers installed and configured

---

## 📋 Quick Commands

```bash
# View configuration
cat ~/.config/Claude/claude_desktop_config.json

# Test all servers
cd /home/eddie/anon_best/tauri-gui
./test_mcp_servers.sh

# Restart Claude Desktop
# Quit and reopen Claude Desktop app
```

---

## 🔍 FREE Research Servers (No API Keys!)

| Server | Purpose | Command |
|--------|---------|---------|
| **DuckDuckGo** | Web search | `npx -y @modelcontextprotocol/server-duckduckgo` |
| **Open Web Search** | Multi-engine search | `npx -y open-websearch-mcp` |
| **ArXiv** | Academic papers | `uvx arxiv-mcp-server` |
| **PubMed** | Medical research | `uvx pubmed-mcp-server` |
| **Wikipedia** | Encyclopedia | `uvx wikimedia-mcp` |
| **GPT Researcher** | Autonomous research | `uvx gpt-researcher-mcp` |

---

## 🎯 How to Use in Claude

### Example 1: Web Search
```
You: "Search DuckDuckGo for latest React 19 features"

Claude will:
- Use DuckDuckGo MCP server
- Return search results
- Summarize findings
```

### Example 2: Academic Research
```
You: "Find recent papers on browser fingerprinting from ArXiv"

Claude will:
- Search ArXiv database
- Return relevant papers
- Provide citations
```

### Example 3: Deep Research
```
You: "Use GPT Researcher to do comprehensive analysis of 
Rust async programming best practices"

Claude will:
- Activate GPT Researcher
- Search multiple sources
- Synthesize findings
- Provide detailed report
```

### Example 4: Multi-Source Research
```
You: "Research WebRTC security using ArXiv, PubMed, 
and web search. Provide a comprehensive report."

Claude will:
- Search ArXiv for academic papers
- Search PubMed for medical/security research
- Search web for recent articles
- Combine all findings
- Generate comprehensive report
```

### Example 5: Browser Testing
```
You: "Use Playwright to navigate to localhost:1420 
and test if WebRTC is blocked"

Claude will:
- Launch browser with Playwright
- Navigate to URL
- Run tests
- Take screenshots
- Report results
```

---

## 🌐 Browser Automation

| Server | Purpose | Command |
|--------|---------|---------|
| **Playwright** | Browser automation | `npx -y @modelcontextprotocol/server-playwright` |
| **Puppeteer** | Chrome automation | `npx -y @modelcontextprotocol/server-puppeteer` |

---

## 📂 Development Tools

| Server | Purpose | API Key? | Command |
|--------|---------|----------|---------|
| **GitHub** | Repo management | ✅ Required | `npx -y @modelcontextprotocol/server-github` |
| **Git** | Local Git ops | ❌ No | `uvx git-mcp-server` |
| **Filesystem** | File operations | ❌ No | `npx -y @modelcontextprotocol/server-filesystem` |
| **Fetch** | Web content | ❌ No | `uvx fetch-mcp-server` |

---

## 🧠 AI Enhancement

| Server | Purpose | Command |
|--------|---------|---------|
| **Memory** | Long-term memory | `npx -y @modelcontextprotocol/server-memory` |
| **Sequential Thinking** | Enhanced reasoning | `npx -y @modelcontextprotocol/server-sequential-thinking` |

---

## 🔧 Configuration File Location

**Linux:** `~/.config/Claude/claude_desktop_config.json`  
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

---

## 📊 Server Status

Run this to check all servers:
```bash
cd /home/eddie/anon_best/tauri-gui
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

## 🎓 Usage Tips

### 1. **Combine Multiple Servers**
```
"Research Tauri security using ArXiv and web search, 
then check our code with Filesystem, and create a 
GitHub issue with recommendations"
```

### 2. **Autonomous Research**
```
"Use GPT Researcher to analyze browser fingerprinting 
techniques. Include sources from ArXiv and PubMed."
```

### 3. **Browser Testing**
```
"Use Playwright to test my app at localhost:1420. 
Check for privacy leaks and take screenshots."
```

### 4. **Code Research**
```
"Search GitHub for Rust proxy implementations, 
then help me implement similar functionality."
```

### 5. **Memory Usage**
```
"Remember that I prefer TypeScript over JavaScript 
and always use Tailwind CSS for styling."

Later: "What are my coding preferences?"
```

---

## 🚨 Troubleshooting

### Servers Not Showing Up?
1. Check config file exists: `cat ~/.config/Claude/claude_desktop_config.json`
2. Restart Claude Desktop completely (Quit + Reopen)
3. Check logs: `tail -f ~/.config/Claude/logs/mcp*.log`

### Server Fails to Start?
1. Test manually: `npx -y @modelcontextprotocol/server-duckduckgo`
2. Check Node.js version: `node --version` (need 18+)
3. Check Python version: `python3 --version` (need 3.8+)
4. Reinstall: `npm install -g <package> --force`

### GitHub Token Setup
1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `read:org`, `read:user`
4. Edit config file and replace `<YOUR_GITHUB_TOKEN_HERE>`

---

## 📚 Documentation

- **Full Guide:** `MCP_SERVERS_GUIDE.md`
- **Research Document:** `MCP_SERVERS_RESEARCH.md`
- **Installation Script:** `install_mcp_servers.sh`
- **Configuration Script:** `configure_mcp_servers.sh`
- **Test Script:** `test_mcp_servers.sh`

---

## ✅ Installed Servers Summary

**Total:** 14 servers  
**Free (No API Keys):** 11 servers  
**Requires API Key:** 1 server (GitHub - optional)

### By Category:
- 🔬 **Research:** 6 servers (all FREE)
- 🌐 **Browser:** 2 servers
- 📂 **Development:** 4 servers (3 FREE)
- 🧠 **AI Enhancement:** 2 servers

---

## 🎉 You're Ready!

All MCP servers are installed and configured. Start using them in Claude Desktop by:

1. **Restart Claude Desktop** (if not already done)
2. **Try a simple query:** "Search DuckDuckGo for Tauri best practices"
3. **Verify servers work:** Look for MCP server responses
4. **Explore capabilities:** Try different combinations

---

**💡 Pro Tip:** Combine multiple servers for powerful workflows!

Example:
```
"Research browser fingerprinting using ArXiv and PubMed, 
search web for recent articles with DuckDuckGo, 
read my current implementation with Filesystem, 
and create a comprehensive improvement plan."
```

This will use 4 MCP servers in one query! 🚀

---

**Need Help?** Check `MCP_SERVERS_GUIDE.md` for detailed instructions.

