import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  User,
  Plus,
  Trash2,
  Edit,
  Globe,
  Clock,
  CheckCircle,
  XCircle,
  Search,
  Filter,
  RefreshCw,
  Shield,
  Cookie,
  Activity,
  TrendingUp,
  AlertTriangle,
  Info,
} from "lucide-react";
import { listProfiles, createProfile, deleteProfile, loadProfile } from "../api";
import type { Profile } from "../api";

interface ProfileStats {
  anonymity_score: number;
  risk_level: 'low' | 'medium' | 'high';
  total_cookies: number;
  unique_domains: number;
  user_agent_strength: number;
  fingerprint_consistency: number;
  last_leak_test?: string;
  leak_test_passed?: boolean;
}

interface ProfileWithMetadata extends Profile {
  creation_date?: string;
  last_used?: string;
  is_active?: boolean;
  stats?: ProfileStats;
}

export default function ProfileManager() {
  const [profiles, setProfiles] = useState<ProfileWithMetadata[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [selectedProfile, setSelectedProfile] = useState<ProfileWithMetadata | null>(null);

  useEffect(() => {
    loadProfiles();
  }, []);

  // Calculate anonymity score for a profile
  function calculateAnonymityScore(profile: Profile): ProfileStats {
    let score = 0;
    let userAgentStrength = 0;
    let fingerprintConsistency = 0;

    // User Agent (25 points)
    if (profile.browser?.user_agent) {
      // Calculate strength based on user agent length and complexity
      const ua = profile.browser.user_agent;
      userAgentStrength = Math.min(100, 60 + (ua.length / 2));
      score += 25;
    }

    // Location data (20 points)
    if (profile.location?.city && profile.location?.country) {
      score += 15;
      if (profile.location?.timezone) {
        score += 5;
      }
    }

    // Fingerprint consistency (25 points)
    // Base score on whether profile has fingerprint data
    if (profile.browser?.user_agent) {
      fingerprintConsistency = 85; // Consistent if profile exists
      score += Math.floor(fingerprintConsistency / 4);
    } else {
      fingerprintConsistency = 50; // Low if no data
      score += Math.floor(fingerprintConsistency / 4);
    }

    // Cookies - REAL DATA (20 points)
    // Get actual cookie count from profile data (will be 0 until cookies are generated)
    const totalCookies = 0;
    const uniqueDomains = 0;
    // No points for cookies until they're actually generated
    // Future: score += Math.min(20, Math.floor(totalCookies / 25));

    // Profile completeness bonus (10 points)
    let completenessBonus = 0;
    if (profile.profile_name) completenessBonus += 2;
    if (profile.location?.city) completenessBonus += 2;
    if (profile.location?.country) completenessBonus += 2;
    if (profile.location?.timezone) completenessBonus += 2;
    if (profile.browser?.user_agent) completenessBonus += 2;
    score += completenessBonus;

    // Determine risk level based on actual score
    let riskLevel: 'low' | 'medium' | 'high';
    if (score >= 70) riskLevel = 'low';
    else if (score >= 50) riskLevel = 'medium';
    else riskLevel = 'high';

    return {
      anonymity_score: Math.min(100, score),
      risk_level: riskLevel,
      total_cookies: totalCookies,
      unique_domains: uniqueDomains,
      user_agent_strength: Math.floor(userAgentStrength),
      fingerprint_consistency: Math.floor(fingerprintConsistency),
      leak_test_passed: undefined, // Only set after running leak test
    };
  }

  async function loadProfiles() {
    try {
      setLoading(true);
      setError(null);
      const response = await listProfiles();

      if (response.success) {
        // Add stats to each profile
        const profilesWithStats = (response.profiles || []).map(profile => ({
          ...profile,
          stats: calculateAnonymityScore(profile),
        }));
        setProfiles(profilesWithStats);
      } else {
        setError(response.error || "Failed to load profiles");
      }
    } catch (err) {
      setError(`Error: ${err}`);
    } finally {
      setLoading(false);
    }
  }

  async function handleCreateProfile(name: string, location?: string) {
    try {
      const response = await createProfile(name, location);
      
      if (response.success) {
        await loadProfiles();
        setShowCreateDialog(false);
      } else {
        setError(response.error || "Failed to create profile");
      }
    } catch (err) {
      setError(`Error: ${err}`);
    }
  }

  async function handleDeleteProfile(profileId: string) {
    if (!confirm("Are you sure you want to delete this profile?")) {
      return;
    }

    try {
      const response = await deleteProfile(profileId);
      
      if (response.success) {
        await loadProfiles();
      } else {
        setError(response.error || "Failed to delete profile");
      }
    } catch (err) {
      setError(`Error: ${err}`);
    }
  }

  async function handleLoadProfile(profileId: string) {
    try {
      const response = await loadProfile(profileId);
      
      if (response.success) {
        setSelectedProfile(response.profile);
      } else {
        setError(response.error || "Failed to load profile");
      }
    } catch (err) {
      setError(`Error: ${err}`);
    }
  }

  const filteredProfiles = profiles.filter((profile) =>
    profile.profile_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-heading font-bold text-neon-cyan">
            Profile Manager
          </h2>
          <p className="text-text-secondary mt-1">
            Manage your anonymous browsing profiles
          </p>
        </div>
        <button
          onClick={() => setShowCreateDialog(true)}
          className="btn-neon-cyan flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Create Profile
        </button>
      </div>

      {/* Search & Filter Bar */}
      <div className="glass-card p-4">
        <div className="flex items-center gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-text-secondary" />
            <input
              type="text"
              placeholder="Search profiles..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-dark-darker border border-neon-cyan/20 rounded-lg
                       text-text-primary placeholder-text-secondary
                       focus:outline-none focus:border-neon-cyan/50 transition-colors"
            />
          </div>
          <button
            onClick={loadProfiles}
            className="btn-neon-purple flex items-center gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
        </div>
      </div>

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

      {/* Loading State */}
      {loading && (
        <div className="flex items-center justify-center py-12">
          <RefreshCw className="w-8 h-8 text-neon-cyan animate-spin" />
        </div>
      )}

      {/* Profile Grid */}
      {!loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <AnimatePresence>
            {filteredProfiles.map((profile) => (
              <ProfileCard
                key={profile.profile_id}
                profile={profile}
                onDelete={handleDeleteProfile}
                onLoad={handleLoadProfile}
                isSelected={selectedProfile?.profile_id === profile.profile_id}
              />
            ))}
          </AnimatePresence>
        </div>
      )}

      {/* Empty State */}
      {!loading && filteredProfiles.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="glass-card p-12 text-center"
        >
          <User className="w-16 h-16 text-text-secondary mx-auto mb-4" />
          <h3 className="text-xl font-heading text-text-primary mb-2">
            No profiles found
          </h3>
          <p className="text-text-secondary mb-6">
            {searchQuery
              ? "Try a different search term"
              : "Create your first profile to get started"}
          </p>
          {!searchQuery && (
            <button
              onClick={() => setShowCreateDialog(true)}
              className="btn-neon-cyan"
            >
              Create Profile
            </button>
          )}
        </motion.div>
      )}

      {/* Create Profile Dialog */}
      <CreateProfileDialog
        isOpen={showCreateDialog}
        onClose={() => setShowCreateDialog(false)}
        onCreate={handleCreateProfile}
      />

      {/* Profile Details Panel */}
      {selectedProfile && (
        <ProfileDetailsPanel
          profile={selectedProfile}
          onClose={() => setSelectedProfile(null)}
        />
      )}
    </div>
  );
}

// Profile Card Component
interface ProfileCardProps {
  profile: ProfileWithMetadata;
  onDelete: (id: string) => void;
  onLoad: (id: string) => void;
  isSelected: boolean;
}

function ProfileCard({ profile, onDelete, onLoad, isSelected }: ProfileCardProps) {
  const stats = profile.stats;

  // Get color based on anonymity score
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getRiskColor = (risk: string) => {
    if (risk === 'low') return 'text-green-400 bg-green-400/10';
    if (risk === 'medium') return 'text-yellow-400 bg-yellow-400/10';
    return 'text-red-400 bg-red-400/10';
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      className={`glass-card p-4 cursor-pointer transition-all hover:shadow-glow-cyan
                  ${isSelected ? "border-neon-cyan shadow-glow-cyan" : ""}`}
      onClick={() => onLoad(profile.profile_id)}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-neon-cyan to-neon-purple
                          flex items-center justify-center">
            <User className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-heading font-bold text-text-primary">
              {profile.profile_name}
            </h3>
            {profile.is_active && (
              <span className="text-xs text-neon-green flex items-center gap-1">
                <CheckCircle className="w-3 h-3" />
                Active
              </span>
            )}
          </div>
        </div>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onDelete(profile.profile_id);
          }}
          className="text-text-secondary hover:text-red-400 transition-colors"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>

      {profile.location && (
        <div className="flex items-center gap-2 text-sm text-text-secondary mb-2">
          <Globe className="w-4 h-4" />
          <span>
            {profile.location.city}, {profile.location.country}
          </span>
        </div>
      )}

      {/* Anonymity Score */}
      {stats && (
        <div className="mt-3 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs text-text-secondary flex items-center gap-1">
              <Shield className="w-3 h-3" />
              Anonymity Score
            </span>
            <span className={`text-sm font-bold ${getScoreColor(stats.anonymity_score)}`}>
              {stats.anonymity_score}/100
            </span>
          </div>

          {/* Risk Level Badge */}
          <div className="flex items-center justify-between">
            <span className="text-xs text-text-secondary">Risk Level</span>
            <span className={`text-xs px-2 py-0.5 rounded-full ${getRiskColor(stats.risk_level)}`}>
              {stats.risk_level.toUpperCase()}
            </span>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 gap-2 mt-2 pt-2 border-t border-gray-700">
            <div className="text-xs">
              <div className="text-text-secondary">Cookies</div>
              <div className="text-cyan-400 font-semibold">{stats.total_cookies}</div>
            </div>
            <div className="text-xs">
              <div className="text-text-secondary">Domains</div>
              <div className="text-purple-400 font-semibold">{stats.unique_domains}</div>
            </div>
          </div>
        </div>
      )}

      {profile.last_used && (
        <div className="flex items-center gap-2 text-xs text-text-secondary">
          <Clock className="w-3 h-3" />
          <span>Last used: {new Date(profile.last_used).toLocaleDateString()}</span>
        </div>
      )}
    </motion.div>
  );
}

// Create Profile Dialog Component
interface CreateProfileDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (name: string, location?: string) => void;
}

function CreateProfileDialog({ isOpen, onClose, onCreate }: CreateProfileDialogProps) {
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (name.trim()) {
      onCreate(name.trim(), location.trim() || undefined);
      setName("");
      setLocation("");
    }
  };

  if (!isOpen) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        className="glass-card p-6 max-w-md w-full m-4"
        onClick={(e) => e.stopPropagation()}
      >
        <h3 className="text-2xl font-heading font-bold text-neon-cyan mb-4">
          Create New Profile
        </h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-text-primary mb-2">
              Profile Name *
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g., Work Profile"
              className="w-full px-4 py-2 bg-dark-darker border border-neon-cyan/20 rounded-lg
                       text-text-primary placeholder-text-secondary
                       focus:outline-none focus:border-neon-cyan/50 transition-colors"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-text-primary mb-2">
              Location (Optional)
            </label>
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g., New York, London"
              className="w-full px-4 py-2 bg-dark-darker border border-neon-cyan/20 rounded-lg
                       text-text-primary placeholder-text-secondary
                       focus:outline-none focus:border-neon-cyan/50 transition-colors"
            />
          </div>
          <div className="flex gap-3 pt-2">
            <button type="submit" className="btn-neon-cyan flex-1">
              Create Profile
            </button>
            <button
              type="button"
              onClick={onClose}
              className="btn-neon-purple flex-1"
            >
              Cancel
            </button>
          </div>
        </form>
      </motion.div>
    </motion.div>
  );
}

// Profile Details Panel Component
interface ProfileDetailsPanelProps {
  profile: ProfileWithMetadata;
  onClose: () => void;
}

function ProfileDetailsPanel({ profile, onClose }: ProfileDetailsPanelProps) {
  const stats = profile.stats;

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getRiskBadgeColor = (risk: string) => {
    if (risk === 'low') return 'bg-green-400/20 text-green-400 border-green-400/30';
    if (risk === 'medium') return 'bg-yellow-400/20 text-yellow-400 border-yellow-400/30';
    return 'bg-red-400/20 text-red-400 border-red-400/30';
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, y: 20 }}
        animate={{ scale: 1, y: 0 }}
        exit={{ scale: 0.9, y: 20 }}
        className="glass-card p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-start justify-between mb-6">
          <div>
            <h2 className="text-2xl font-heading font-bold text-neon-cyan mb-1">
              {profile.profile_name}
            </h2>
            <p className="text-text-secondary text-sm">Profile ID: {profile.profile_id}</p>
          </div>
          <button
            onClick={onClose}
            className="text-text-secondary hover:text-text-primary transition-colors"
          >
            <XCircle className="w-6 h-6" />
          </button>
        </div>

        {/* Anonymity Score Section */}
        {stats && (
          <div className="space-y-6">
            {/* Score Overview */}
            <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                  <Shield className="w-5 h-5 text-cyan-400" />
                  Anonymity Overview
                </h3>
                <span className={`text-3xl font-bold ${getScoreColor(stats.anonymity_score)}`}>
                  {stats.anonymity_score}/100
                </span>
              </div>

              {/* Progress Bar */}
              <div className="w-full bg-gray-700 rounded-full h-3 mb-4">
                <div
                  className={`h-3 rounded-full transition-all ${
                    stats.anonymity_score >= 80
                      ? 'bg-gradient-to-r from-green-500 to-green-400'
                      : stats.anonymity_score >= 60
                      ? 'bg-gradient-to-r from-yellow-500 to-yellow-400'
                      : 'bg-gradient-to-r from-red-500 to-red-400'
                  }`}
                  style={{ width: `${stats.anonymity_score}%` }}
                />
              </div>

              {/* Risk Level */}
              <div className="flex items-center justify-between">
                <span className="text-sm text-text-secondary">Risk Level</span>
                <span className={`px-3 py-1 rounded-full text-sm font-semibold border ${getRiskBadgeColor(stats.risk_level)}`}>
                  {stats.risk_level.toUpperCase()}
                </span>
              </div>
            </div>

            {/* Statistics Grid */}
            <div className="grid grid-cols-2 gap-4">
              {/* Cookies */}
              <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                <div className="flex items-center gap-2 mb-2">
                  <Cookie className="w-4 h-4 text-cyan-400" />
                  <span className="text-sm text-text-secondary">Total Cookies</span>
                </div>
                <div className="text-2xl font-bold text-cyan-400">{stats.total_cookies}</div>
                <div className="text-xs text-text-secondary mt-1">
                  {stats.unique_domains} unique domains
                </div>
              </div>

              {/* User Agent */}
              <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                <div className="flex items-center gap-2 mb-2">
                  <Activity className="w-4 h-4 text-purple-400" />
                  <span className="text-sm text-text-secondary">User Agent</span>
                </div>
                <div className="text-2xl font-bold text-purple-400">{stats.user_agent_strength}%</div>
                <div className="text-xs text-text-secondary mt-1">Strength rating</div>
              </div>

              {/* Fingerprint */}
              <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                <div className="flex items-center gap-2 mb-2">
                  <TrendingUp className="w-4 h-4 text-green-400" />
                  <span className="text-sm text-text-secondary">Fingerprint</span>
                </div>
                <div className="text-2xl font-bold text-green-400">{stats.fingerprint_consistency}%</div>
                <div className="text-xs text-text-secondary mt-1">Consistency score</div>
              </div>

              {/* Leak Test */}
              <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                <div className="flex items-center gap-2 mb-2">
                  <AlertTriangle className="w-4 h-4 text-yellow-400" />
                  <span className="text-sm text-text-secondary">Leak Test</span>
                </div>
                <div className={`text-2xl font-bold ${stats.leak_test_passed ? 'text-green-400' : 'text-red-400'}`}>
                  {stats.leak_test_passed ? 'PASSED' : 'FAILED'}
                </div>
                <div className="text-xs text-text-secondary mt-1">Last test result</div>
              </div>
            </div>

            {/* Profile Details */}
            <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
              <h3 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
                <Info className="w-5 h-5 text-cyan-400" />
                Profile Details
              </h3>

              <div className="space-y-3">
                {/* Location */}
                {profile.location && (
                  <div className="flex items-start gap-3">
                    <Globe className="w-4 h-4 text-cyan-400 mt-0.5" />
                    <div className="flex-1">
                      <div className="text-sm text-text-secondary">Location</div>
                      <div className="text-white">
                        {profile.location.city}, {profile.location.country}
                      </div>
                      {profile.location.timezone && (
                        <div className="text-xs text-text-secondary">
                          Timezone: {profile.location.timezone}
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* User Agent */}
                {profile.browser?.user_agent && (
                  <div className="flex items-start gap-3">
                    <Activity className="w-4 h-4 text-purple-400 mt-0.5" />
                    <div className="flex-1">
                      <div className="text-sm text-text-secondary">User Agent</div>
                      <div className="text-white text-xs font-mono break-all">
                        {profile.browser.user_agent}
                      </div>
                    </div>
                  </div>
                )}

                {/* Timestamps */}
                {profile.creation_date && (
                  <div className="flex items-start gap-3">
                    <Clock className="w-4 h-4 text-green-400 mt-0.5" />
                    <div className="flex-1">
                      <div className="text-sm text-text-secondary">Created</div>
                      <div className="text-white text-sm">
                        {new Date(profile.creation_date).toLocaleString()}
                      </div>
                    </div>
                  </div>
                )}

                {profile.last_used && (
                  <div className="flex items-start gap-3">
                    <Clock className="w-4 h-4 text-yellow-400 mt-0.5" />
                    <div className="flex-1">
                      <div className="text-sm text-text-secondary">Last Used</div>
                      <div className="text-white text-sm">
                        {new Date(profile.last_used).toLocaleString()}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Recommendations */}
            <div className="bg-gradient-to-r from-cyan-500/10 to-purple-500/10 rounded-lg p-4 border border-cyan-500/30">
              <h3 className="text-sm font-semibold text-cyan-400 mb-2">💡 Recommendations</h3>
              <ul className="text-xs text-text-secondary space-y-1">
                {stats.anonymity_score < 80 && (
                  <li>• Consider adding more cookies to improve authenticity</li>
                )}
                {stats.anonymity_score < 60 && (
                  <li>• Update user agent to a more recent version</li>
                )}
                {!stats.leak_test_passed && (
                  <li>• Run leak detection test and fix identified issues</li>
                )}
                <li>• Regularly rotate proxies for better anonymity</li>
                <li>• Use this profile with Tor or VPN for maximum protection</li>
              </ul>
            </div>
          </div>
        )}

        {/* Close Button */}
        <div className="mt-6 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg transition-colors"
          >
            Close
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}

