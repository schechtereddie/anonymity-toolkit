import { useState, useEffect } from 'react';
import { Settings as SettingsIcon, Save, RotateCcw, Bell, Shield, Zap, Eye, Globe } from 'lucide-react';

interface SettingsData {
  // General Settings
  autoStart: boolean;
  minimizeToTray: boolean;
  notifications: boolean;
  
  // Privacy Settings
  clearCookiesOnExit: boolean;
  clearHistoryOnExit: boolean;
  blockTrackers: boolean;
  blockAds: boolean;
  
  // Automation Settings
  autoRotateProfiles: boolean;
  rotationInterval: number; // minutes
  autoLeakTest: boolean;
  leakTestInterval: number; // minutes
  
  // Advanced Settings
  debugMode: boolean;
  logLevel: 'error' | 'warn' | 'info' | 'debug';
  maxConcurrentBrowsers: number;
  browserTimeout: number; // seconds
}

const defaultSettings: SettingsData = {
  autoStart: false,
  minimizeToTray: true,
  notifications: true,
  clearCookiesOnExit: false,
  clearHistoryOnExit: false,
  blockTrackers: true,
  blockAds: true,
  autoRotateProfiles: false,
  rotationInterval: 30,
  autoLeakTest: false,
  leakTestInterval: 60,
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
        </div>
      </div>

      {/* Privacy Settings */}
      <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
          <Shield className="w-5 h-5 text-purple-400" />
          Privacy
        </h3>
        
        <div className="space-y-4">
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
              label="Rotation interval (minutes)"
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
              label="Test interval (minutes)"
              description="How often to run leak tests"
              value={settings.leakTestInterval}
              min={15}
              max={1440}
              onChange={(value) => updateSetting('leakTestInterval', value)}
            />
          )}
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
    <div className="flex items-start justify-between">
      <div className="flex-1">
        <label className="text-white font-medium">{label}</label>
        <p className="text-gray-400 text-sm mt-1">{description}</p>
      </div>
      <button
        onClick={() => onChange(!checked)}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
          checked ? 'bg-cyan-500' : 'bg-gray-600'
        }`}
      >
        <span
          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
            checked ? 'translate-x-6' : 'translate-x-1'
          }`}
        />
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

