import { useState, useEffect } from 'react';
import { Cookie, Download, Upload, Trash2, RefreshCw, Sparkles, FileJson } from 'lucide-react';
import { generateCookies, generateRealisticCookies, clearCookies, exportCookies, importCookies } from '../api';

interface CookieData {
  domain: string;
  name: string;
  value: string;
  path?: string;
  expires?: number;
  secure?: boolean;
  httponly?: boolean;
  samesite?: string;
}

export default function CookieManager() {
  const [loading, setLoading] = useState(false);
  const [generatedCookies, setGeneratedCookies] = useState<any[]>([]);
  const [domain, setDomain] = useState('example.com');
  const [cookieCount, setCookieCount] = useState(5);
  const [profileId, setProfileId] = useState('default');
  const [months, setMonths] = useState(3);
  const [sitesPerMonth, setSitesPerMonth] = useState(50);
  const [showRealistic, setShowRealistic] = useState(false);

  const handleGenerateSimple = async () => {
    setLoading(true);
    try {
      const response = await generateCookies(domain, cookieCount);
      
      if (response.success) {
        setGeneratedCookies(response.cookies || []);
        alert(`✅ Generated ${response.count} cookies for ${domain}`);
      } else {
        alert(`Failed to generate cookies: ${response.error}`);
      }
    } catch (error) {
      console.error('Error generating cookies:', error);
      alert('Failed to generate cookies');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateRealistic = async () => {
    setLoading(true);
    try {
      const response = await generateRealisticCookies(profileId, months, sitesPerMonth);
      
      if (response.success) {
        setGeneratedCookies(response.cookies || []);
        alert(`✅ Generated ${response.count} realistic cookies!\n\nProfile: ${profileId}\nMonths: ${months}\nTotal cookies: ${response.count}`);
      } else {
        alert(`Failed to generate realistic cookies: ${response.error}`);
      }
    } catch (error) {
      console.error('Error generating realistic cookies:', error);
      alert('Failed to generate realistic cookies');
    } finally {
      setLoading(false);
    }
  };

  const handleClearCookies = async (specificDomain?: string) => {
    try {
      const response = await clearCookies(specificDomain);
      
      if (response.success) {
        setGeneratedCookies([]);
        alert(`✅ ${response.message}`);
      } else {
        alert(`Failed to clear cookies: ${response.error}`);
      }
    } catch (error) {
      console.error('Error clearing cookies:', error);
      alert('Failed to clear cookies');
    }
  };

  const handleExportCookies = async () => {
    try {
      const filename = `cookies_${Date.now()}.json`;
      const response = await exportCookies(filename);
      
      if (response.success) {
        alert(`✅ Cookies exported to ${filename}`);
      } else {
        alert(`Failed to export cookies: ${response.error}`);
      }
    } catch (error) {
      console.error('Error exporting cookies:', error);
      alert('Failed to export cookies');
    }
  };

  const handleImportCookies = async () => {
    try {
      const filename = prompt('Enter filename to import:');
      if (!filename) return;

      const response = await importCookies(filename);
      
      if (response.success) {
        alert(`✅ Imported ${response.count} cookie domains from ${filename}`);
      } else {
        alert(`Failed to import cookies: ${response.error}`);
      }
    } catch (error) {
      console.error('Error importing cookies:', error);
      alert('Failed to import cookies');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <Cookie className="w-6 h-6 text-cyan-400" />
            Cookie Manager
          </h2>
          <p className="text-gray-400 mt-1">Generate and manage browser cookies</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleExportCookies}
            className="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg flex items-center gap-2 transition-colors"
          >
            <Download className="w-4 h-4" />
            Export
          </button>
          <button
            onClick={handleImportCookies}
            className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg flex items-center gap-2 transition-colors"
          >
            <Upload className="w-4 h-4" />
            Import
          </button>
          <button
            onClick={() => handleClearCookies()}
            className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg flex items-center gap-2 transition-colors"
          >
            <Trash2 className="w-4 h-4" />
            Clear All
          </button>
        </div>
      </div>

      {/* Generation Mode Tabs */}
      <div className="flex gap-2 border-b border-gray-700">
        <button
          onClick={() => setShowRealistic(false)}
          className={`px-4 py-2 font-medium transition-colors ${
            !showRealistic
              ? 'text-cyan-400 border-b-2 border-cyan-400'
              : 'text-gray-400 hover:text-gray-300'
          }`}
        >
          <Cookie className="w-4 h-4 inline mr-2" />
          Simple Cookies
        </button>
        <button
          onClick={() => setShowRealistic(true)}
          className={`px-4 py-2 font-medium transition-colors ${
            showRealistic
              ? 'text-purple-400 border-b-2 border-purple-400'
              : 'text-gray-400 hover:text-gray-300'
          }`}
        >
          <Sparkles className="w-4 h-4 inline mr-2" />
          Realistic Cookies
        </button>
      </div>

      {/* Simple Cookie Generation */}
      {!showRealistic && (
        <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Generate Simple Cookies</h3>
          <p className="text-gray-400 text-sm mb-4">
            Create basic session cookies for testing and development
          </p>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Domain
              </label>
              <input
                type="text"
                value={domain}
                onChange={(e) => setDomain(e.target.value)}
                placeholder="example.com"
                className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Cookie Count
              </label>
              <input
                type="number"
                value={cookieCount}
                onChange={(e) => setCookieCount(parseInt(e.target.value) || 1)}
                min="1"
                max="20"
                className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-cyan-500"
              />
            </div>
          </div>

          <button
            onClick={handleGenerateSimple}
            disabled={loading}
            className="w-full px-4 py-3 bg-cyan-500 hover:bg-cyan-600 disabled:bg-cyan-500/50 disabled:cursor-not-allowed text-white rounded-lg flex items-center justify-center gap-2 transition-colors font-medium"
          >
            {loading ? (
              <>
                <RefreshCw className="w-5 h-5 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Cookie className="w-5 h-5" />
                Generate Simple Cookies
              </>
            )}
          </button>
        </div>
      )}

      {/* Realistic Cookie Generation */}
      {showRealistic && (
        <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-purple-400" />
            Generate Realistic Cookies
          </h3>
          <p className="text-gray-400 text-sm mb-4">
            Create comprehensive cookie profiles with behavioral patterns, temporal distribution, and cross-site relationships
          </p>

          <div className="grid grid-cols-3 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Profile ID
              </label>
              <input
                type="text"
                value={profileId}
                onChange={(e) => setProfileId(e.target.value)}
                placeholder="default"
                className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-purple-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Months of History
              </label>
              <input
                type="number"
                value={months}
                onChange={(e) => setMonths(parseInt(e.target.value) || 1)}
                min="1"
                max="12"
                className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-purple-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Sites per Month
              </label>
              <input
                type="number"
                value={sitesPerMonth}
                onChange={(e) => setSitesPerMonth(parseInt(e.target.value) || 10)}
                min="10"
                max="200"
                className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-purple-500"
              />
            </div>
          </div>

          <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4 mb-4">
            <h4 className="text-sm font-medium text-purple-300 mb-2">Features:</h4>
            <ul className="text-sm text-gray-300 space-y-1">
              <li>• Temporal patterns (realistic visit times)</li>
              <li>• Cross-site relationships (referrer tracking)</li>
              <li>• Session, preference, analytics, and auth cookies</li>
              <li>• Age decay and renewal patterns</li>
              <li>• Behavioral consistency across sites</li>
            </ul>
          </div>

          <button
            onClick={handleGenerateRealistic}
            disabled={loading}
            className="w-full px-4 py-3 bg-purple-500 hover:bg-purple-600 disabled:bg-purple-500/50 disabled:cursor-not-allowed text-white rounded-lg flex items-center justify-center gap-2 transition-colors font-medium"
          >
            {loading ? (
              <>
                <RefreshCw className="w-5 h-5 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                Generate Realistic Cookies
              </>
            )}
          </button>
        </div>
      )}

      {/* Generated Cookies Display */}
      {generatedCookies.length > 0 && (
        <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <FileJson className="w-5 h-5 text-cyan-400" />
              Generated Cookies ({generatedCookies.length})
            </h3>
            <button
              onClick={() => setGeneratedCookies([])}
              className="text-sm text-gray-400 hover:text-gray-300"
            >
              Clear Display
            </button>
          </div>
          
          <div className="bg-gray-900 rounded-lg p-4 max-h-96 overflow-y-auto">
            <pre className="text-sm text-gray-300 whitespace-pre-wrap">
              {JSON.stringify(generatedCookies, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}

