import { useState, useEffect } from 'react';
import { Settings as SettingsIcon, Save, RotateCcw, Bell, Shield, Zap, Eye, Globe } from 'lucide-react';

interface SettingsData {
  // General Settings
  autoStart: boolean;
  minimizeToTray: boolean;
  notifications: boolean;
  showWelcomeScreen: boolean;
  checkForUpdates: boolean;

  // Privacy Settings
  clearCookiesOnExit: boolean;
  clearHistoryOnExit: boolean;
  clearCacheOnExit: boolean;
  blockTrackers: boolean;
  blockAds: boolean;
  blockWebRTC: boolean;
  disableCanvasFingerprinting: boolean;
  randomizeTimezone: boolean;
  disablePlugins: boolean;
  disableJavaScript: boolean;
  disableImages: boolean;

  // Proxy Settings
  autoRotateProxies: boolean;
  proxyRotationInterval: number; // minutes
  testProxyBeforeUse: boolean;
  autoScrapeProxies: boolean;

  // Automation Settings
  autoRotateProfiles: boolean;
  rotationInterval: number; // minutes
  autoLeakTest: boolean;
  leakTestInterval: number; // minutes
  autoSaveSessions: boolean;

  // Browser Settings
  enableMonitoring: boolean;
  logRequests: boolean;
  collectFingerprints: boolean;
  muteAudio: boolean;
  disableNotifications: boolean;

  // Advanced Settings
  debugMode: boolean;
  logLevel: 'error' | 'warn' | 'info' | 'debug';
  maxConcurrentBrowsers: number;
  browserTimeout: number; // seconds
}

const defaultSettings: SettingsData = {
  // General
  autoStart: false,
  minimizeToTray: true,
  notifications: true,
  showWelcomeScreen: true,
  checkForUpdates: true,
  // Privacy
  clearCookiesOnExit: false,
  clearHistoryOnExit: false,
  clearCacheOnExit: false,
  blockTrackers: true,
  blockAds: true,
  blockWebRTC: true,
  disableCanvasFingerprinting: true,
  randomizeTimezone: false,
  disablePlugins: false,
  disableJavaScript: false,
  disableImages: false,
  // Proxy
  autoRotateProxies: false,
  proxyRotationInterval: 15,
  testProxyBeforeUse: true,
  autoScrapeProxies: false,
  // Automation
  autoRotateProfiles: false,
  rotationInterval: 30,
  autoLeakTest: false,
  leakTestInterval: 60,
  autoSaveSessions: true,
  // Browser
  enableMonitoring: true,
  logRequests: false,
  collectFingerprints: true,
  muteAudio: false,
  disableNotifications: true,
  // Advanced
  debugMode: false,
  logLevel: 'info',
  maxConcurrentBrowsers: 3,
  browserTimeout: 300,
};

export default function Settings() {
  const [settings, setSettings] = useState<SettingsData>(defaultSettings);
  const [hasChanges, setHasChanges] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = () => {
    const stored = localStorage.getItem('app_settings');
    if (stored) {
      try {
        setSettings(JSON.parse(stored));
      } catch (error) {
        console.error('Failed to load settings:', error);
      }
    }
  };

  const saveSettings = async () => {
    setSaving(true);
    try {
      localStorage.setItem('app_settings', JSON.stringify(settings));
      setHasChanges(false);
      // TODO: Send settings to backend if needed
      await new Promise(resolve => setTimeout(resolve, 500)); // Simulate save
    } catch (error) {
      console.error('Failed to save settings:', error);
      alert('Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  const resetSettings = () => {
    if (confirm('Are you sure you want to reset all settings to defaults?')) {
      setSettings(defaultSettings);
      setHasChanges(true);
    }
  };

  const updateSetting = <K extends keyof SettingsData>(key: K, value: SettingsData[K]) => {
    setSettings(prev => ({ ...prev, [key]: value }));
    setHasChanges(true);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <SettingsIcon className="w-6 h-6 text-cyan-400" />
            Settings
          </h2>
          <p className="text-gray-400 mt-1">Configure application preferences</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={resetSettings}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg flex items-center gap-2 transition-colors"
          >
            <RotateCcw className="w-4 h-4" />
            Reset
          </button>
          <button
            onClick={saveSettings}
            disabled={!hasChanges || saving}
            className="px-4 py-2 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg flex items-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Save className="w-4 h-4" />
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </div>

      {hasChanges && (
        <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4">
          <p className="text-yellow-400 text-sm">
            ⚠️ You have unsaved changes. Click "Save Changes" to apply them.
          </p>
        </div>
      )}

      {/* General Settings */}
      <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
          <Zap className="w-5 h-5 text-cyan-400" />
          General
        </h3>

        <div className="space-y-4">
          <SettingToggle
            label="Auto-start on system boot"
            description="Launch the application automatically when your system starts"
            checked={settings.autoStart}
            onChange={(checked) => updateSetting('autoStart', checked)}
          />

          <SettingToggle
            label="Minimize to system tray"
            description="Keep the application running in the background"
            checked={settings.minimizeToTray}
            onChange={(checked) => updateSetting('minimizeToTray', checked)}
          />

          <SettingToggle
            label="Enable notifications"
            description="Show desktop notifications for important events"
            checked={settings.notifications}
            onChange={(checked) => updateSetting('notifications', checked)}
          />

          <SettingToggle
            label="Show welcome screen"
            description="Display welcome screen on application startup"
            checked={settings.showWelcomeScreen}
            onChange={(checked) => updateSetting('showWelcomeScreen', checked)}
          />

          <SettingToggle
            label="Check for updates"
            description="Automatically check for application updates"
            checked={settings.checkForUpdates}
            onChange={(checked) => updateSetting('checkForUpdates', checked)}
          />
        </div>
      </div>

      {/* Privacy Settings */}
      <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
          <Shield className="w-5 h-5 text-purple-400" />
          Privacy & Security
        </h3>

        <div className="space-y-4">
          <div className="text-sm font-medium text-gray-300 mb-2">Cleanup on Exit</div>

          <SettingToggle
            label="Clear cookies on exit"
            description="Automatically delete all cookies when closing the application"
            checked={settings.clearCookiesOnExit}
            onChange={(checked) => updateSetting('clearCookiesOnExit', checked)}
          />

          <SettingToggle
            label="Clear history on exit"
            description="Automatically delete browsing history when closing"
            checked={settings.clearHistoryOnExit}
            onChange={(checked) => updateSetting('clearHistoryOnExit', checked)}
          />

          <SettingToggle
            label="Clear cache on exit"
            description="Automatically delete browser cache when closing"
            checked={settings.clearCacheOnExit}
            onChange={(checked) => updateSetting('clearCacheOnExit', checked)}
          />

          <div className="text-sm font-medium text-gray-300 mb-2 mt-6">Content Blocking</div>

          <SettingToggle
            label="Block trackers"
            description="Block known tracking scripts and pixels"
            checked={settings.blockTrackers}
            onChange={(checked) => updateSetting('blockTrackers', checked)}
          />

          <SettingToggle
            label="Block advertisements"
            description="Block ads and sponsored content"
            checked={settings.blockAds}
            onChange={(checked) => updateSetting('blockAds', checked)}
          />

          <SettingToggle
            label="Block WebRTC"
            description="Prevent WebRTC IP leaks (recommended for anonymity)"
            checked={settings.blockWebRTC}
            onChange={(checked) => updateSetting('blockWebRTC', checked)}
          />

          <div className="text-sm font-medium text-gray-300 mb-2 mt-6">Anti-Fingerprinting</div>

          <SettingToggle
            label="Disable canvas fingerprinting"
            description="Prevent canvas-based browser fingerprinting"
            checked={settings.disableCanvasFingerprinting}
            onChange={(checked) => updateSetting('disableCanvasFingerprinting', checked)}
          />

          <SettingToggle
            label="Randomize timezone"
            description="Use random timezone to prevent location tracking"
            checked={settings.randomizeTimezone}
            onChange={(checked) => updateSetting('randomizeTimezone', checked)}
          />

          <SettingToggle
            label="Disable plugins"
            description="Disable browser plugins (Flash, Java, etc.)"
            checked={settings.disablePlugins}
            onChange={(checked) => updateSetting('disablePlugins', checked)}
          />

          <div className="text-sm font-medium text-gray-300 mb-2 mt-6">Performance vs Privacy</div>

          <SettingToggle
            label="Disable JavaScript"
            description="Block JavaScript execution (may break some websites)"
            checked={settings.disableJavaScript}
            onChange={(checked) => updateSetting('disableJavaScript', checked)}
          />

          <SettingToggle
            label="Disable images"
            description="Don't load images (faster browsing, more private)"
            checked={settings.disableImages}
            onChange={(checked) => updateSetting('disableImages', checked)}
          />
        </div>
      </div>

      {/* Proxy Settings */}
      <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
          <Globe className="w-5 h-5 text-blue-400" />
          Proxy Management
        </h3>

        <div className="space-y-4">
          <SettingToggle
            label="Auto-rotate proxies"
            description="Automatically switch to a different proxy periodically"
            checked={settings.autoRotateProxies}
            onChange={(checked) => updateSetting('autoRotateProxies', checked)}
          />

          {settings.autoRotateProxies && (
            <SettingNumber
              label="Proxy rotation interval (minutes)"
              description="How often to switch proxies"
              value={settings.proxyRotationInterval}
              min={5}
              max={1440}
              onChange={(value) => updateSetting('proxyRotationInterval', value)}
            />
          )}

          <SettingToggle
            label="Test proxy before use"
            description="Verify proxy connectivity before launching browser"
            checked={settings.testProxyBeforeUse}
            onChange={(checked) => updateSetting('testProxyBeforeUse', checked)}
          />

          <SettingToggle
            label="Auto-scrape proxies"
            description="Automatically scrape new proxies when list is low"
            checked={settings.autoScrapeProxies}
            onChange={(checked) => updateSetting('autoScrapeProxies', checked)}
          />
        </div>
      </div>

      {/* Automation Settings */}
      <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
          <Bell className="w-5 h-5 text-green-400" />
          Automation
        </h3>

        <div className="space-y-4">
          <SettingToggle
            label="Auto-rotate profiles"
            description="Automatically switch to a different profile periodically"
            checked={settings.autoRotateProfiles}
            onChange={(checked) => updateSetting('autoRotateProfiles', checked)}
          />

          {settings.autoRotateProfiles && (
            <SettingNumber
              label="Profile rotation interval (minutes)"
              description="How often to switch profiles"
              value={settings.rotationInterval}
              min={5}
              max={1440}
              onChange={(value) => updateSetting('rotationInterval', value)}
            />
          )}

          <SettingToggle
            label="Auto leak testing"
            description="Automatically run leak detection tests periodically"
            checked={settings.autoLeakTest}
            onChange={(checked) => updateSetting('autoLeakTest', checked)}
          />

          {settings.autoLeakTest && (
            <SettingNumber
              label="Leak test interval (minutes)"
              description="How often to run leak tests"
              value={settings.leakTestInterval}
              min={15}
              max={1440}
              onChange={(value) => updateSetting('leakTestInterval', value)}
            />
          )}

          <SettingToggle
            label="Auto-save sessions"
            description="Automatically save browser sessions and state"
            checked={settings.autoSaveSessions}
            onChange={(checked) => updateSetting('autoSaveSessions', checked)}
          />
        </div>
      </div>

      {/* Browser Settings */}
      <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
          <Globe className="w-5 h-5 text-orange-400" />
          Browser Behavior
        </h3>

        <div className="space-y-4">
          <SettingToggle
            label="Enable monitoring"
            description="Monitor browser performance and resource usage"
            checked={settings.enableMonitoring}
            onChange={(checked) => updateSetting('enableMonitoring', checked)}
          />

          <SettingToggle
            label="Log requests"
            description="Log all HTTP/HTTPS requests for debugging"
            checked={settings.logRequests}
            onChange={(checked) => updateSetting('logRequests', checked)}
          />

          <SettingToggle
            label="Collect fingerprints"
            description="Collect and analyze browser fingerprints"
            checked={settings.collectFingerprints}
            onChange={(checked) => updateSetting('collectFingerprints', checked)}
          />

          <SettingToggle
            label="Mute audio"
            description="Disable all audio output in browser"
            checked={settings.muteAudio}
            onChange={(checked) => updateSetting('muteAudio', checked)}
          />

          <SettingToggle
            label="Disable notifications"
            description="Block website notification requests"
            checked={settings.disableNotifications}
            onChange={(checked) => updateSetting('disableNotifications', checked)}
          />
        </div>
      </div>

      {/* Advanced Settings */}
      <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
          <Eye className="w-5 h-5 text-red-400" />
          Advanced
        </h3>

        <div className="space-y-4">
          <SettingToggle
            label="Debug mode"
            description="Enable verbose logging for troubleshooting"
            checked={settings.debugMode}
            onChange={(checked) => updateSetting('debugMode', checked)}
          />

          <SettingSelect
            label="Log level"
            description="Minimum severity level for log messages"
            value={settings.logLevel}
            options={[
              { value: 'error', label: 'Error' },
              { value: 'warn', label: 'Warning' },
              { value: 'info', label: 'Info' },
              { value: 'debug', label: 'Debug' },
            ]}
            onChange={(value) => updateSetting('logLevel', value as any)}
          />

          <SettingNumber
            label="Max concurrent browsers"
            description="Maximum number of browser instances to run simultaneously"
            value={settings.maxConcurrentBrowsers}
            min={1}
            max={10}
            onChange={(value) => updateSetting('maxConcurrentBrowsers', value)}
          />

          <SettingNumber
            label="Browser timeout (seconds)"
            description="Automatically close browser after this duration"
            value={settings.browserTimeout}
            min={60}
            max={3600}
            onChange={(value) => updateSetting('browserTimeout', value)}
          />
        </div>
      </div>
    </div>
  );
}

// Helper Components

interface SettingToggleProps {
  label: string;
  description: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
}

function SettingToggle({ label, description, checked, onChange }: SettingToggleProps) {
  return (
    <div className="flex items-start justify-between gap-4">
      <div className="flex-1">
        <label className="text-white font-medium cursor-pointer" onClick={() => onChange(!checked)}>
          {label}
        </label>
        <p className="text-gray-400 text-sm mt-1">{description}</p>
      </div>
      <button
        onClick={() => onChange(!checked)}
        className={`relative inline-flex h-7 w-14 items-center rounded-full transition-all duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 ${
          checked
            ? 'bg-gradient-to-r from-cyan-500 to-cyan-400 shadow-glow-cyan focus:ring-cyan-500'
            : 'bg-gray-600 hover:bg-gray-500 focus:ring-gray-500'
        }`}
        aria-checked={checked}
        role="switch"
      >
        <span className="sr-only">{label}</span>
        <span
          className={`inline-block h-5 w-5 transform rounded-full bg-white shadow-lg transition-all duration-300 ease-in-out ${
            checked ? 'translate-x-8 scale-110' : 'translate-x-1 scale-100'
          }`}
        >
          {/* Checkmark icon when enabled */}
          {checked && (
            <svg
              className="h-5 w-5 text-cyan-500 animate-fade-in"
              fill="currentColor"
              viewBox="0 0 12 12"
            >
              <path d="M3.707 5.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4a1 1 0 00-1.414-1.414L5 6.586 3.707 5.293z" />
            </svg>
          )}
        </span>
      </button>
    </div>
  );
}

interface SettingNumberProps {
  label: string;
  description: string;
  value: number;
  min: number;
  max: number;
  onChange: (value: number) => void;
}

function SettingNumber({ label, description, value, min, max, onChange }: SettingNumberProps) {
  return (
    <div className="ml-6 border-l-2 border-gray-700 pl-4">
      <label className="text-white font-medium">{label}</label>
      <p className="text-gray-400 text-sm mt-1 mb-2">{description}</p>
      <input
        type="number"
        value={value}
        min={min}
        max={max}
        onChange={(e) => onChange(parseInt(e.target.value) || min)}
        className="w-32 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
      />
    </div>
  );
}

interface SettingSelectProps {
  label: string;
  description: string;
  value: string;
  options: { value: string; label: string }[];
  onChange: (value: string) => void;
}

function SettingSelect({ label, description, value, options, onChange }: SettingSelectProps) {
  return (
    <div>
      <label className="text-white font-medium">{label}</label>
      <p className="text-gray-400 text-sm mt-1 mb-2">{description}</p>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-48 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}

