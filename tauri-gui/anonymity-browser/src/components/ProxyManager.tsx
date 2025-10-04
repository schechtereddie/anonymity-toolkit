import { useState, useEffect } from 'react';
import { Plus, Trash2, RefreshCw, CheckCircle, XCircle, Globe, Shield, Download } from 'lucide-react';
import { addProxy, listProxies, testProxy, deleteProxy, getActiveProxy, setActiveProxy, scrapeProxies } from '../api';

interface Proxy {
  id: string;
  name: string;
  type: 'socks5' | 'http' | 'https';
  host: string;
  port: number;
  username?: string;
  password?: string;
  status: 'active' | 'inactive' | 'testing';
  lastTested?: string;
  responseTime?: number;
}

export default function ProxyManager() {
  const [proxies, setProxies] = useState<Proxy[]>([]);
  const [loading, setLoading] = useState(false);
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [testingProxy, setTestingProxy] = useState<string | null>(null);
  const [scraping, setScraping] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    name: '',
    type: 'socks5' as 'socks5' | 'http' | 'https',
    host: '',
    port: '',
    username: '',
    password: '',
  });

  useEffect(() => {
    loadProxies();
  }, []);

  const loadProxies = async () => {
    setLoading(true);
    try {
      const response = await listProxies();
      if (response.success && response.proxies) {
        setProxies(response.proxies);
      }
    } catch (error) {
      console.error('Failed to load proxies:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddProxy = async () => {
    if (!formData.name || !formData.host || !formData.port) {
      alert('Please fill in all required fields');
      return;
    }

    try {
      const proxyId = Date.now().toString();
      const response = await addProxy(
        proxyId,
        formData.name,
        formData.type,
        formData.host,
        parseInt(formData.port),
        formData.username || undefined,
        formData.password || undefined
      );

      if (response.success) {
        await loadProxies();
        setShowAddDialog(false);
        resetForm();
      } else {
        alert(`Failed to add proxy: ${response.error}`);
      }
    } catch (error) {
      console.error('Error adding proxy:', error);
      alert('Failed to add proxy');
    }
  };

  const handleDeleteProxy = async (id: string) => {
    if (confirm('Are you sure you want to delete this proxy?')) {
      try {
        const response = await deleteProxy(id);
        if (response.success) {
          await loadProxies();
        } else {
          alert(`Failed to delete proxy: ${response.error}`);
        }
      } catch (error) {
        console.error('Error deleting proxy:', error);
        alert('Failed to delete proxy');
      }
    }
  };

  const handleTestProxy = async (id: string) => {
    setTestingProxy(id);

    try {
      const response = await testProxy(id);

      if (response.success) {
        // Reload proxies to get updated status
        await loadProxies();
      } else {
        alert(`Proxy test failed: ${response.error}`);
        await loadProxies();
      }
    } catch (error) {
      console.error('Error testing proxy:', error);
      alert('Failed to test proxy');
    } finally {
      setTestingProxy(null);
    }
  };

  const handleScrapeProxies = async () => {
    setScraping(true);
    try {
      const response = await scrapeProxies(100, 'socks5', true);

      if (response.success) {
        const count = response.count || 0;
        const savedCount = response.saved_count || 0;
        alert(`✅ Scraping complete!\n\nFound: ${count} proxies\nSaved: ${savedCount} proxies\n\nProxies have been added to your list.`);
        await loadProxies();
      } else {
        alert(`Failed to scrape proxies: ${response.error}`);
      }
    } catch (error) {
      console.error('Error scraping proxies:', error);
      alert('Failed to scrape proxies. Make sure the backend is running.');
    } finally {
      setScraping(false);
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      type: 'socks5',
      host: '',
      port: '',
      username: '',
      password: '',
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <Globe className="w-6 h-6 text-cyan-400" />
            Proxy Manager
          </h2>
          <p className="text-gray-400 mt-1">Configure and test proxy servers</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleScrapeProxies}
            disabled={scraping}
            className="px-4 py-2 bg-purple-500 hover:bg-purple-600 disabled:bg-purple-500/50 disabled:cursor-not-allowed text-white rounded-lg flex items-center gap-2 transition-colors"
          >
            {scraping ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                Scraping...
              </>
            ) : (
              <>
                <Download className="w-4 h-4" />
                Scrape Proxies
              </>
            )}
          </button>
          <button
            onClick={() => setShowAddDialog(true)}
            className="px-4 py-2 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg flex items-center gap-2 transition-colors"
          >
            <Plus className="w-4 h-4" />
            Add Proxy
          </button>
        </div>
      </div>

      {/* Proxy List */}
      {loading ? (
        <div className="text-center py-12">
          <RefreshCw className="w-8 h-8 text-cyan-400 animate-spin mx-auto" />
          <p className="text-gray-400 mt-2">Loading proxies...</p>
        </div>
      ) : proxies.length === 0 ? (
        <div className="text-center py-12 bg-gray-800/50 rounded-lg border border-gray-700">
          <Shield className="w-12 h-12 text-gray-600 mx-auto" />
          <p className="text-gray-400 mt-4">No proxies configured</p>
          <p className="text-gray-500 text-sm mt-2">Add a proxy to get started</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {proxies.map((proxy) => (
            <div
              key={proxy.id}
              className="bg-gray-800/50 rounded-lg border border-gray-700 p-4 hover:border-cyan-500/50 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <h3 className="text-lg font-semibold text-white">{proxy.name}</h3>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      proxy.status === 'active' ? 'bg-green-500/20 text-green-400' :
                      proxy.status === 'testing' ? 'bg-yellow-500/20 text-yellow-400' :
                      'bg-gray-500/20 text-gray-400'
                    }`}>
                      {proxy.status}
                    </span>
                    <span className="px-2 py-1 rounded text-xs font-medium bg-purple-500/20 text-purple-400 uppercase">
                      {proxy.type}
                    </span>
                  </div>
                  
                  <div className="mt-2 space-y-1">
                    <p className="text-gray-400 text-sm">
                      <span className="text-gray-500">Host:</span> {proxy.host}:{proxy.port}
                    </p>
                    {proxy.username && (
                      <p className="text-gray-400 text-sm">
                        <span className="text-gray-500">Username:</span> {proxy.username}
                      </p>
                    )}
                    {proxy.lastTested && (
                      <p className="text-gray-400 text-sm">
                        <span className="text-gray-500">Last Tested:</span> {new Date(proxy.lastTested).toLocaleString()}
                        {proxy.responseTime && (
                          <span className="ml-2 text-cyan-400">({proxy.responseTime.toFixed(0)}ms)</span>
                        )}
                      </p>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleTestProxy(proxy.id)}
                    disabled={testingProxy === proxy.id}
                    className="p-2 text-cyan-400 hover:bg-cyan-500/10 rounded-lg transition-colors disabled:opacity-50"
                    title="Test Proxy"
                  >
                    <RefreshCw className={`w-4 h-4 ${testingProxy === proxy.id ? 'animate-spin' : ''}`} />
                  </button>
                  <button
                    onClick={() => handleDeleteProxy(proxy.id)}
                    className="p-2 text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                    title="Delete Proxy"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Add Proxy Dialog */}
      {showAddDialog && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-gray-900 rounded-lg border border-gray-700 p-6 w-full max-w-md">
            <h3 className="text-xl font-bold text-white mb-4">Add New Proxy</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Proxy Name *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
                  placeholder="My Proxy"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Type *</label>
                <select
                  value={formData.type}
                  onChange={(e) => setFormData({ ...formData, type: e.target.value as any })}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
                >
                  <option value="socks5">SOCKS5</option>
                  <option value="http">HTTP</option>
                  <option value="https">HTTPS</option>
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-1">Host *</label>
                  <input
                    type="text"
                    value={formData.host}
                    onChange={(e) => setFormData({ ...formData, host: e.target.value })}
                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
                    placeholder="127.0.0.1"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-1">Port *</label>
                  <input
                    type="number"
                    value={formData.port}
                    onChange={(e) => setFormData({ ...formData, port: e.target.value })}
                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
                    placeholder="1080"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Username (Optional)</label>
                <input
                  type="text"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
                  placeholder="username"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Password (Optional)</label>
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={() => {
                  setShowAddDialog(false);
                  resetForm();
                }}
                className="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleAddProxy}
                className="flex-1 px-4 py-2 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg transition-colors"
              >
                Add Proxy
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

