import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Shield, Zap, Eye, Globe, Lock, Activity, CheckCircle, XCircle, User, Chrome, Menu } from "lucide-react";
import { pingSidecar, getSidecarStatus, startSidecar } from "./api";
import ProfileManager from "./components/ProfileManager";
import BrowserLauncher from "./components/BrowserLauncher";
import LeakDetector from "./components/LeakDetector";

type TabType = "home" | "profiles" | "browser" | "leaks";

function App() {
  const [status, setStatus] = useState<string>("Initializing...");
  const [sidecarRunning, setSidecarRunning] = useState<boolean>(false);
  const [connectionStatus, setConnectionStatus] = useState<"connecting" | "connected" | "error">("connecting");
  const [activeTab, setActiveTab] = useState<TabType>("home");

  useEffect(() => {
    // Initialize sidecar on mount
    initializeSidecar();
  }, []);

  async function initializeSidecar() {
    try {
      setStatus("Starting Python backend...");
      await startSidecar();
      setStatus("Testing connection...");

      const response = await pingSidecar();

      if (response.success) {
        setStatus(`Connected! Version: ${response.version || "1.0.0"}`);
        setSidecarRunning(true);
        setConnectionStatus("connected");

        // Get detailed status
        const statusResponse = await getSidecarStatus();
        if (statusResponse.success) {
          console.log("Sidecar status:", statusResponse);
        }
      } else {
        setStatus(`Connection failed: ${response.error}`);
        setConnectionStatus("error");
      }
    } catch (error) {
      console.error("Failed to initialize sidecar:", error);
      setStatus(`Error: ${error}`);
      setConnectionStatus("error");
    }
  }

  async function testConnection() {
    try {
      setStatus("Testing connection...");
      const response = await pingSidecar();

      if (response.success) {
        setStatus(`✅ Connection successful! Message: ${response.message}`);
        setSidecarRunning(true);
        setConnectionStatus("connected");
      } else {
        setStatus(`❌ Connection failed: ${response.error}`);
        setConnectionStatus("error");
      }
    } catch (error) {
      setStatus(`❌ Error: ${error}`);
      setConnectionStatus("error");
    }
  }

  return (
    <div className="min-h-screen bg-dark-bg text-text-primary">
      {/* Header */}
      <header className="border-b border-dark-slate bg-dark-darker/50 backdrop-blur-md">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-3"
            >
              <Shield className="w-8 h-8 text-neon-cyan" />
              <h1 className="text-2xl font-heading font-bold text-glow-cyan">
                ULTIMATE ANONYMITY TOOLKIT
              </h1>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-2"
            >
              {connectionStatus === "connected" && (
                <div className="status-active">
                  <CheckCircle className="w-4 h-4" />
                  <span>Backend Online</span>
                </div>
              )}
              {connectionStatus === "connecting" && (
                <div className="status-indicator bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/30">
                  <Activity className="w-4 h-4 animate-spin" />
                  <span>Connecting...</span>
                </div>
              )}
              {connectionStatus === "error" && (
                <div className="status-warning">
                  <XCircle className="w-4 h-4" />
                  <span>Backend Offline</span>
                </div>
              )}
            </motion.div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="border-b border-dark-slate bg-dark-charcoal/50">
        <div className="container mx-auto px-6">
          <div className="flex gap-1">
            <TabButton
              active={activeTab === "home"}
              onClick={() => setActiveTab("home")}
              icon={Shield}
              label="Home"
            />
            <TabButton
              active={activeTab === "profiles"}
              onClick={() => setActiveTab("profiles")}
              icon={User}
              label="Profiles"
            />
            <TabButton
              active={activeTab === "browser"}
              onClick={() => setActiveTab("browser")}
              icon={Chrome}
              label="Browser"
            />
            <TabButton
              active={activeTab === "leaks"}
              onClick={() => setActiveTab("leaks")}
              icon={Eye}
              label="Leak Detection"
            />
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {activeTab === "home" && (
          <>
            {/* Welcome Section */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="glass-card p-8 mb-6"
            >
              <h2 className="text-3xl font-heading font-bold mb-4 text-neon-cyan">
                Welcome to the Future of Privacy
              </h2>
              <p className="text-text-secondary text-lg mb-6">
                Wall Street meets Cyberpunk - Professional anonymity with cutting-edge technology
              </p>

              <div className="flex gap-4">
                <button
                  onClick={testConnection}
                  className="btn-neon-cyan"
                >
                  <Zap className="inline w-5 h-5 mr-2" />
                  Test Connection
                </button>
                <button
                  onClick={() => setActiveTab("browser")}
                  className="btn-neon-purple"
                >
                  <Globe className="inline w-5 h-5 mr-2" />
                  Launch Browser
                </button>
              </div>

              <div className="mt-4 p-4 bg-dark-darker rounded-md border border-dark-slate">
                <p className="text-sm font-mono text-neon-green">
                  Status: {status}
                </p>
              </div>
            </motion.div>

            {/* Feature Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="glass-card-hover p-6"
          >
            <Shield className="w-12 h-12 text-neon-cyan mb-4" />
            <h3 className="text-xl font-heading font-bold mb-2">
              Profile Mode
            </h3>
            <p className="text-text-secondary">
              Persistent identity with consistent fingerprints for long-term believability
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="glass-card-hover p-6"
          >
            <Eye className="w-12 h-12 text-neon-purple mb-4" />
            <h3 className="text-xl font-heading font-bold mb-2">
              Leak Detection
            </h3>
            <p className="text-text-secondary">
              Comprehensive testing for WebRTC, DNS, Canvas, and WebGL leaks
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="glass-card-hover p-6"
          >
            <Lock className="w-12 h-12 text-neon-pink mb-4" />
            <h3 className="text-xl font-heading font-bold mb-2">
              Stealth Mode
            </h3>
            <p className="text-text-secondary">
              Random fingerprints for maximum anonymity when you need it most
            </p>
          </motion.div>
        </div>

        {/* Security Status */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="glass-card p-6 mt-6"
        >
          <h3 className="text-xl font-heading font-bold mb-4 text-neon-cyan">
            Security Status
          </h3>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-neon-green mb-1">✓</div>
              <div className="text-sm text-text-secondary">WebRTC</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-neon-green mb-1">✓</div>
              <div className="text-sm text-text-secondary">DNS</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-neon-green mb-1">✓</div>
              <div className="text-sm text-text-secondary">Canvas</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-neon-green mb-1">✓</div>
              <div className="text-sm text-text-secondary">Proxy</div>
            </div>
          </div>
        </motion.div>
          </>
        )}

        {activeTab === "profiles" && <ProfileManager />}
        {activeTab === "browser" && <BrowserLauncher />}
        {activeTab === "leaks" && <LeakDetector />}
      </main>

      {/* Footer */}
      <footer className="border-t border-dark-slate mt-12 py-6">
        <div className="container mx-auto px-6 text-center text-text-muted text-sm">
          <p>Ultimate Anonymity Toolkit v1.0.0 - Tauri Edition</p>
          <p className="mt-1">Wall Street meets Cyberpunk</p>
        </div>
      </footer>
    </div>
  );
}

// Tab Button Component
interface TabButtonProps {
  active: boolean;
  onClick: () => void;
  icon: any;
  label: string;
}

function TabButton({ active, onClick, icon: Icon, label }: TabButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`
        relative px-6 py-3 font-heading font-medium transition-all
        flex items-center gap-2
        ${
          active
            ? "text-neon-cyan"
            : "text-text-secondary hover:text-text-primary"
        }
      `}
    >
      <Icon className="w-5 h-5" />
      <span>{label}</span>
      {active && (
        <motion.div
          layoutId="activeTab"
          className="absolute bottom-0 left-0 right-0 h-0.5 bg-neon-cyan shadow-glow-cyan"
        />
      )}
    </button>
  );
}

export default App;
