import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Shield,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Loader,
  Wifi,
  Globe,
  Eye,
  Fingerprint,
  Play,
  Download,
  Info,
} from "lucide-react";
import { runLeakTest } from "../api";

interface LeakTestResult {
  test_name: string;
  status: "pass" | "fail" | "warning" | "running";
  message: string;
  details?: any;
}

interface LeakTestSuite {
  webrtc?: LeakTestResult;
  dns?: LeakTestResult;
  canvas?: LeakTestResult;
  webgl?: LeakTestResult;
  audio?: LeakTestResult;
  timezone?: LeakTestResult;
  automation?: LeakTestResult;
}

export default function LeakDetector() {
  const [testing, setTesting] = useState(false);
  const [results, setResults] = useState<LeakTestSuite | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleRunTests() {
    try {
      setTesting(true);
      setError(null);
      setResults(null);

      const response = await runLeakTest();

      if (response.success) {
        setResults(response.results || {});
      } else {
        setError(response.error || "Failed to run leak tests");
      }
    } catch (err) {
      setError(`Error: ${err}`);
    } finally {
      setTesting(false);
    }
  }

  function exportResults() {
    if (!results) return;

    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `leak-test-${new Date().toISOString()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  }

  const testCategories = [
    {
      id: "webrtc",
      name: "WebRTC Leak",
      icon: Wifi,
      description: "Checks if your real IP is exposed through WebRTC",
    },
    {
      id: "dns",
      name: "DNS Leak",
      icon: Globe,
      description: "Verifies DNS requests are properly routed",
    },
    {
      id: "canvas",
      name: "Canvas Fingerprint",
      icon: Fingerprint,
      description: "Tests canvas fingerprinting protection",
    },
    {
      id: "webgl",
      name: "WebGL Fingerprint",
      icon: Eye,
      description: "Tests WebGL fingerprinting protection",
    },
  ];

  const getOverallStatus = () => {
    if (!results) return null;
    const allResults = Object.values(results);
    if (allResults.some((r) => r.status === "fail")) return "fail";
    if (allResults.some((r) => r.status === "warning")) return "warning";
    if (allResults.every((r) => r.status === "pass")) return "pass";
    return null;
  };

  const overallStatus = getOverallStatus();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-heading font-bold text-neon-cyan">
            Leak Detection
          </h2>
          <p className="text-text-secondary mt-1">
            Test your anonymity and detect potential privacy leaks
          </p>
        </div>
        <div className="flex gap-3">
          {results && (
            <button
              onClick={exportResults}
              className="btn-neon-purple flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Export Results
            </button>
          )}
          <button
            onClick={handleRunTests}
            disabled={testing}
            className="btn-neon-cyan flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {testing ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                Running Tests...
              </>
            ) : (
              <>
                <Play className="w-5 h-5" />
                Run All Tests
              </>
            )}
          </button>
        </div>
      </div>

      {/* Overall Status */}
      {overallStatus && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className={`glass-card p-6 ${
            overallStatus === "pass"
              ? "border-neon-green/50 bg-neon-green/5"
              : overallStatus === "warning"
              ? "border-yellow-500/50 bg-yellow-500/5"
              : "border-red-500/50 bg-red-500/5"
          }`}
        >
          <div className="flex items-center gap-4">
            {overallStatus === "pass" && (
              <>
                <CheckCircle className="w-12 h-12 text-neon-green" />
                <div>
                  <h3 className="text-xl font-heading font-bold text-neon-green">
                    All Tests Passed!
                  </h3>
                  <p className="text-text-secondary">
                    Your anonymity protection is working correctly
                  </p>
                </div>
              </>
            )}
            {overallStatus === "warning" && (
              <>
                <AlertTriangle className="w-12 h-12 text-yellow-500" />
                <div>
                  <h3 className="text-xl font-heading font-bold text-yellow-500">
                    Warnings Detected
                  </h3>
                  <p className="text-text-secondary">
                    Some tests show potential issues that need attention
                  </p>
                </div>
              </>
            )}
            {overallStatus === "fail" && (
              <>
                <XCircle className="w-12 h-12 text-red-500" />
                <div>
                  <h3 className="text-xl font-heading font-bold text-red-500">
                    Tests Failed
                  </h3>
                  <p className="text-text-secondary">
                    Critical privacy leaks detected - review results below
                  </p>
                </div>
              </>
            )}
          </div>
        </motion.div>
      )}

      {/* Error Display */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-4 border-red-500/50 bg-red-500/10"
        >
          <div className="flex items-center gap-2 text-red-400">
            <XCircle className="w-5 h-5" />
            <span>{error}</span>
          </div>
        </motion.div>
      )}

      {/* Test Categories */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <AnimatePresence>
          {testCategories.map((category) => {
            const result = results?.[category.id as keyof LeakTestSuite];
            return (
              <TestCard
                key={category.id}
                category={category}
                result={result}
                testing={testing}
              />
            );
          })}
        </AnimatePresence>
      </div>

      {/* Information Panel */}
      <div className="glass-card p-6 bg-neon-cyan/5">
        <div className="flex items-start gap-3">
          <Info className="w-6 h-6 text-neon-cyan flex-shrink-0 mt-1" />
          <div>
            <h3 className="text-lg font-heading font-bold text-neon-cyan mb-2">
              About Leak Detection
            </h3>
            <div className="space-y-2 text-sm text-text-secondary">
              <p>
                <strong className="text-text-primary">WebRTC Leak:</strong> WebRTC can expose your real IP address even when using a VPN or proxy. We test for this vulnerability.
              </p>
              <p>
                <strong className="text-text-primary">DNS Leak:</strong> DNS requests can reveal your browsing activity. We verify that DNS queries are properly routed through your anonymity network.
              </p>
              <p>
                <strong className="text-text-primary">Fingerprinting:</strong> Canvas, WebGL, and audio APIs can be used to create unique fingerprints. We test that these are properly randomized.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Test Card Component
interface TestCardProps {
  category: {
    id: string;
    name: string;
    icon: any;
    description: string;
  };
  result?: LeakTestResult;
  testing: boolean;
}

function TestCard({ category, result, testing }: TestCardProps) {
  const Icon = category.icon;

  const getStatusConfig = () => {
    if (testing) {
      return {
        icon: Loader,
        color: "text-neon-cyan",
        bg: "bg-neon-cyan/20",
        border: "border-neon-cyan/30",
        label: "Testing...",
      };
    }
    if (!result) {
      return {
        icon: Icon,
        color: "text-text-secondary",
        bg: "bg-text-secondary/20",
        border: "border-text-secondary/30",
        label: "Not tested",
      };
    }
    switch (result.status) {
      case "pass":
        return {
          icon: CheckCircle,
          color: "text-neon-green",
          bg: "bg-neon-green/20",
          border: "border-neon-green/30",
          label: "Passed",
        };
      case "warning":
        return {
          icon: AlertTriangle,
          color: "text-yellow-500",
          bg: "bg-yellow-500/20",
          border: "border-yellow-500/30",
          label: "Warning",
        };
      case "fail":
        return {
          icon: XCircle,
          color: "text-red-500",
          bg: "bg-red-500/20",
          border: "border-red-500/30",
          label: "Failed",
        };
      default:
        return {
          icon: Icon,
          color: "text-text-secondary",
          bg: "bg-text-secondary/20",
          border: "border-text-secondary/30",
          label: "Unknown",
        };
    }
  };

  const config = getStatusConfig();
  const StatusIcon = config.icon;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className={`glass-card p-4 border ${config.border}`}
    >
      <div className="flex items-start gap-3">
        <div className={`w-12 h-12 rounded-lg ${config.bg} flex items-center justify-center flex-shrink-0`}>
          <StatusIcon className={`w-6 h-6 ${config.color} ${testing ? "animate-spin" : ""}`} />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-1">
            <h3 className="font-heading font-bold text-text-primary">
              {category.name}
            </h3>
            <span className={`text-xs font-medium ${config.color}`}>
              {config.label}
            </span>
          </div>
          <p className="text-sm text-text-secondary mb-2">
            {category.description}
          </p>
          {result && result.message && (
            <p className={`text-sm ${config.color}`}>
              {result.message}
            </p>
          )}
        </div>
      </div>
    </motion.div>
  );
}

