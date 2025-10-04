/**
 * Tauri API wrapper for Python sidecar commands
 */

import { invoke } from "@tauri-apps/api/core";

export interface SidecarResponse {
  success: boolean;
  error?: string;
  [key: string]: any;
}

export interface Profile {
  profile_id: string;
  profile_name: string;
  location?: {
    city: string;
    country: string;
    timezone: string;
  };
  browser?: {
    user_agent: string;
  };
}

/**
 * Start the Python sidecar process
 */
export async function startSidecar(): Promise<string> {
  return await invoke<string>("start_sidecar");
}

/**
 * Ping the Python sidecar to check if it's alive
 */
export async function pingSidecar(): Promise<SidecarResponse> {
  return await invoke<SidecarResponse>("ping_sidecar");
}

/**
 * Create a new profile
 */
export async function createProfile(
  profileName: string,
  location?: string
): Promise<SidecarResponse> {
  return await invoke<SidecarResponse>("create_profile", {
    profileName,
    location,
  });
}

/**
 * Load an existing profile
 */
export async function loadProfile(profileId: string): Promise<SidecarResponse> {
  return await invoke<SidecarResponse>("load_profile", {
    profileId,
  });
}

/**
 * List all profiles
 */
export async function listProfiles(): Promise<SidecarResponse> {
  return await invoke<SidecarResponse>("list_profiles");
}

/**
 * Delete a profile
 */
export async function deleteProfile(profileId: string): Promise<SidecarResponse> {
  return await invoke<SidecarResponse>("delete_profile", {
    profileId,
  });
}

/**
 * Get sidecar status
 */
export async function getSidecarStatus(): Promise<SidecarResponse> {
  return await invoke<SidecarResponse>("get_sidecar_status");
}

/**
 * Launch browser with profile
 */
export async function launchBrowser(
  profileId: string,
  url?: string
): Promise<SidecarResponse> {
  return await invoke<SidecarResponse>("launch_browser", {
    profileId,
    url,
  });
}

/**
 * Run leak detection test
 */
export async function runLeakTest(testType?: string): Promise<SidecarResponse> {
  return await invoke<SidecarResponse>("run_leak_test", {
    testType,
  });
}

