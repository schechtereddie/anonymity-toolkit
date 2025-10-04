import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Globe,
  Play,
  Square,
  Chrome,
  Firefox,
  Shield,
  Zap,
  ExternalLink,
  AlertCircle,
  CheckCircle,
  Loader,
} from "lucide-react";
import { launchBrowser, listProfiles } from "../api";
import type { Profile } from "../api";

interface BrowserSession {
  profile_id: string;
  profile_name: string;
  browser_type: string;
  status: "launching" | "running" | "stopped" | "error";
  url?: string;
  pid?: number;
}

export default function BrowserLauncher() {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [selectedProfile, setSelectedProfile] = useState<string>("");
  const [url, setUrl] = useState("https://www.google.com");
  const [sessions, setSessions] = useState<BrowserSession[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadProfiles();
  }, []);

  async function loadProfiles() {
    try {
      const response = await listProfiles();
      if (response.success) {
        setProfiles(response.profiles || []);
        if (response.profiles?.length > 0 && !selectedProfile) {
          setSelectedProfile(response.profiles[0].profile_id);
        }
      }
    } catch (err) {
      console.error("Failed to load profiles:", err);
    }
  }

  async function handleLaunchBrowser() {
    if (!selectedProfile) {
      setError("Please select a profile first");
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Add session to UI immediately
      const newSession: BrowserSession = {
        profile_id: selectedProfile,
        profile_name: profiles.find((p) => p.profile_id === selectedProfile)?.profile_name || "Unknown",
        browser_type: "chromium",
        status: "launching",
        url,
      };
      setSessions([...sessions, newSession]);

      const response = await launchBrowser(selectedProfile, url);

      if (response.success) {
        // Update session status
        setSessions((prev) =>
          prev.map((s) =>
            s.profile_id === selectedProfile && s.status === "launching"
              ? { ...s, status: "running", pid: response.pid }
              : s
          )
        );
      } else {
        setError(response.error || "Failed to launch browser");
        setSessions((prev) =>
          prev.map((s) =>
            s.profile_id === selectedProfile && s.status === "launching"
              ? { ...s, status: "error" }
              : s
          )
        );
      }
    } catch (err) {
      setError(`Error: ${err}`);
      setSessions((prev) =>
        prev.map((s) =>
          s.profile_id === selectedProfile && s.status === "launching"
            ? { ...s, status: "error" }
            : s
        )
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-heading font-bold text-neon-cyan">
          Browser Launcher
        </h2>
        <p className="text-text-secondary mt-1">
          Launch anonymous browsers with profile-based fingerprinting
        </p>
      </div>

      {/* Launch Controls */}
      <div className="glass-card p-6">
        <div className="space-y-4">
          {/* Profile Selection */}
          <div>
            <label className="block text-sm font-medium text-text-primary mb-2">
              Select Profile
            </label>
            <select
              value={selectedProfile}
              onChange={(e) => setSelectedProfile(e.target.value)}
              className="w-full px-4 py-2 bg-dark-darker border border-neon-cyan/20 rounded-lg
                       text-text-primary focus:outline-none focus:border-neon-cyan/50 transition-colors"
            >
              <option value="">-- Select a profile --</option>
              {profiles.map((profile) => (
                <option key={profile.profile_id} value={profile.profile_id}>
                  {profile.profile_name}
                  {profile.location && ` (${profile.location.city}, ${profile.location.country})`}
                </option>
              ))}
            </select>
          </div>

          {/* URL Input */}
          <div>
            <label className="block text-sm font-medium text-text-primary mb-2">
              Starting URL
            </label>
            <div className="relative">
              <Globe className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-text-secondary" />
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://example.com"
                className="w-full pl-10 pr-4 py-2 bg-dark-darker border border-neon-cyan/20 rounded-lg
                         text-text-primary placeholder-text-secondary
                         focus:outline-none focus:border-neon-cyan/50 transition-colors"
              />
            </div>
          </div>

          {/* Launch Button */}
          <button
            onClick={handleLaunchBrowser}
            disabled={loading || !selectedProfile}
            className="btn-neon-cyan w-full flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                Launching Browser...
              </>
            ) : (
              <>
                <Play className="w-5 h-5" />
                Launch Anonymous Browser
              </>
            )}
          </button>

          {/* Error Display */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="p-3 bg-red-500/10 border border-red-500/50 rounded-lg"
            >
              <div className="flex items-center gap-2 text-red-400 text-sm">
                <AlertCircle className="w-4 h-4" />
                <span>{error}</span>
              </div>
            </motion.div>
          )}
        </div>
      </div>

      {/* Features Info */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card p-4">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-neon-cyan/20 flex items-center justify-center">
              <Shield className="w-5 h-5 text-neon-cyan" />
            </div>
            <h3 className="font-heading font-bold text-text-primary">
              Fingerprint Protection
            </h3>
          </div>
          <p className="text-sm text-text-secondary">
            Canvas, WebGL, and audio fingerprints are randomized per profile
          </p>
        </div>

        <div className="glass-card p-4">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-neon-purple/20 flex items-center justify-center">
              <Zap className="w-5 h-5 text-neon-purple" />
            </div>
            <h3 className="font-heading font-bold text-text-primary">
              WebRTC Blocking
            </h3>
          </div>
          <p className="text-sm text-text-secondary">
            Prevents IP leaks through WebRTC connections
          </p>
        </div>

        <div className="glass-card p-4">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-neon-green/20 flex items-center justify-center">
              <Chrome className="w-5 h-5 text-neon-green" />
            </div>
            <h3 className="font-heading font-bold text-text-primary">
              Real Browser
            </h3>
          </div>
          <p className="text-sm text-text-secondary">
            Full Chromium browser with all features enabled
          </p>
        </div>
      </div>

      {/* Active Sessions */}
      {sessions.length > 0 && (
        <div className="glass-card p-6">
          <h3 className="text-xl font-heading font-bold text-text-primary mb-4">
            Active Sessions
          </h3>
          <div className="space-y-3">
            {sessions.map((session, index) => (
              <SessionCard key={index} session={session} />
            ))}
          </div>
        </div>
      )}

      {/* Quick Start Guide */}
      <div className="glass-card p-6 bg-neon-cyan/5">
        <h3 className="text-lg font-heading font-bold text-neon-cyan mb-3">
          🚀 Quick Start Guide
        </h3>
        <ol className="space-y-2 text-sm text-text-secondary">
          <li className="flex items-start gap-2">
            <span className="text-neon-cyan font-bold">1.</span>
            <span>Select a profile or create a new one in the Profile Manager</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-neon-cyan font-bold">2.</span>
            <span>Enter the URL you want to visit (optional)</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-neon-cyan font-bold">3.</span>
            <span>Click "Launch Anonymous Browser" to start browsing</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-neon-cyan font-bold">4.</span>
            <span>Your fingerprint is automatically applied and protected</span>
          </li>
        </ol>
      </div>
    </div>
  );
}

// Session Card Component
interface SessionCardProps {
  session: BrowserSession;
}

function SessionCard({ session }: SessionCardProps) {
  const statusConfig = {
    launching: {
      icon: Loader,
      color: "text-neon-cyan",
      bg: "bg-neon-cyan/20",
      label: "Launching...",
    },
    running: {
      icon: CheckCircle,
      color: "text-neon-green",
      bg: "bg-neon-green/20",
      label: "Running",
    },
    stopped: {
      icon: Square,
      color: "text-text-secondary",
      bg: "bg-text-secondary/20",
      label: "Stopped",
    },
    error: {
      icon: AlertCircle,
      color: "text-red-400",
      bg: "bg-red-400/20",
      label: "Error",
    },
  };

  const config = statusConfig[session.status];
  const StatusIcon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className="flex items-center justify-between p-3 bg-dark-darker rounded-lg border border-neon-cyan/20"
    >
      <div className="flex items-center gap-3">
        <div className={`w-8 h-8 rounded-lg ${config.bg} flex items-center justify-center`}>
          <StatusIcon className={`w-4 h-4 ${config.color} ${session.status === "launching" ? "animate-spin" : ""}`} />
        </div>
        <div>
          <div className="font-medium text-text-primary">{session.profile_name}</div>
          <div className="text-xs text-text-secondary flex items-center gap-2">
            <span className={config.color}>{config.label}</span>
            {session.pid && <span>• PID: {session.pid}</span>}
          </div>
        </div>
      </div>
      {session.url && (
        <div className="flex items-center gap-2 text-sm text-text-secondary">
          <ExternalLink className="w-4 h-4" />
          <span className="max-w-xs truncate">{session.url}</span>
        </div>
      )}
    </motion.div>
  );
}

