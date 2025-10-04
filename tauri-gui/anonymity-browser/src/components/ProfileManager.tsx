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
} from "lucide-react";
import { listProfiles, createProfile, deleteProfile, loadProfile } from "../api";
import type { Profile } from "../api";

interface ProfileWithMetadata extends Profile {
  creation_date?: string;
  last_used?: string;
  is_active?: boolean;
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

  async function loadProfiles() {
    try {
      setLoading(true);
      setError(null);
      const response = await listProfiles();
      
      if (response.success) {
        setProfiles(response.profiles || []);
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

// Profile Details Panel Component (placeholder)
interface ProfileDetailsPanelProps {
  profile: ProfileWithMetadata;
  onClose: () => void;
}

function ProfileDetailsPanel({ profile, onClose }: ProfileDetailsPanelProps) {
  return null; // Will implement in next iteration
}

