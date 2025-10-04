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

export interface Proxy {
  id: string;
  name: string;
  type: 'socks5' | 'http' | 'https';
  host: string;
  port: number;
  username?: string;
  password?: string;
  status: 'active' | 'inactive' | 'testing';
  last_tested?: string;
  response_time?: number;
  created_at?: string;
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

// Proxy Management API

/**
 * Add a new proxy
 */
export async function addProxy(
  id: string,
  name: string,
  proxyType: 'socks5' | 'http' | 'https',
  host: string,
  port: number,
  username?: string,
  password?: string
): Promise<SidecarResponse> {
  return await invoke<SidecarResponse>("add_proxy", {
    id,
    name,
    proxyType,
    host,
    port,
    username,
    password,
  });
}

/**
 * List all proxies
 */
export async function listProxies(): Promise<SidecarResponse & { proxies?: Proxy[] }> {
  return await invoke<SidecarResponse>("list_proxies");
}

/**
 * Test a proxy connection
 */
export async function testProxy(proxyId: string): Promise<SidecarResponse> {
  return await invoke<SidecarResponse>("test_proxy", {
    proxyId,
  });
}

/**
 * Delete a proxy
 */
export async function deleteProxy(proxyId: string): Promise<SidecarResponse> {
  return await invoke<SidecarResponse>("delete_proxy", {
    proxyId,
  });
}

/**
 * Get the currently active proxy
 */
export async function getActiveProxy(): Promise<SidecarResponse & { proxy?: Proxy }> {
  return await invoke<SidecarResponse>("get_active_proxy");
}

/**
 * Set the active proxy (pass null to clear)
 */
export async function setActiveProxy(proxyId: string | null): Promise<SidecarResponse> {
  return await invoke<SidecarResponse>("set_active_proxy", {
    proxyId,
  });
}

/**
 * Scrape proxies from public sources
 */
export async function scrapeProxies(
  maxProxies?: number,
  proxyType?: 'socks5' | 'http' | 'https',
  autoSave?: boolean
): Promise<SidecarResponse> {
  return await invoke<SidecarResponse>("scrape_proxies", {
    maxProxies,
    proxyType,
    autoSave,
  });
}

/**
 * Scrape proxies from a specific geographic region
 */
export async function scrapeProxiesByRegion(
  region: string,
  maxProxies?: number,
  autoSave?: boolean
): Promise<SidecarResponse> {
  return await invoke<SidecarResponse>("scrape_proxies_by_region", {
    region,
    maxProxies,
    autoSave,
  });
}

