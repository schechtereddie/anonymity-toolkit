# 📚 API Documentation

**Anonymity Browser - Tauri Edition**  
**Version:** 1.0.0  
**Last Updated:** 2025-10-04

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [TypeScript API](#typescript-api)
4. [Rust Commands](#rust-commands)
5. [Python Sidecar](#python-sidecar)
6. [Data Types](#data-types)
7. [Error Handling](#error-handling)
8. [Examples](#examples)

---

## Overview

The Anonymity Browser uses a three-tier architecture:

```
React Frontend (TypeScript)
    ↓ invoke()
Tauri Backend (Rust)
    ↓ stdin/stdout JSON
Python Sidecar (Python)
```

All communication uses JSON messages with a standardized format.

---

## Architecture

### Communication Flow

1. **Frontend → Rust**: Uses Tauri's `invoke()` function
2. **Rust → Python**: JSON messages via stdin/stdout
3. **Python → Rust**: JSON responses via stdout
4. **Rust → Frontend**: Returns Promise with response data

### Message Protocol

**Request Format:**
```json
{
  "command": "command_name",
  "data": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

**Response Format:**
```json
{
  "success": true,
  "data_field": "value",
  "error": "error message (if success=false)"
}
```

---

## TypeScript API

Located in: `src/api.ts`

### Core Functions

#### `startSidecar()`
Start the Python sidecar process.

```typescript
const result = await startSidecar();
// Returns: "Python sidecar started successfully"
```

#### `pingSidecar()`
Health check for the Python backend.

```typescript
const response = await pingSidecar();
// Returns: { success: true, message: "pong", version: "1.0.0" }
```

#### `getSidecarStatus()`
Get detailed status of the Python backend.

```typescript
const response = await getSidecarStatus();
// Returns: {
//   success: true,
//   status: "running",
//   modules: {
//     profile_db: true,
//     profile_generator: true,
//     browser_launcher: false,
//     leak_detector: false
//   }
// }
```

### Profile Management

#### `createProfile(profileName, location?)`
Create a new anonymous profile.

```typescript
const response = await createProfile("WorkProfile", "New York");
// Returns: {
//   success: true,
//   profile_id: "uuid-here",
//   profile_name: "WorkProfile",
//   message: "Profile WorkProfile created successfully"
// }
```

**Parameters:**
- `profileName` (string, required): Name for the profile
- `location` (string, optional): Location hint (e.g., "New York", "London")

#### `loadProfile(profileId)`
Load an existing profile.

```typescript
const response = await loadProfile("uuid-here");
// Returns: {
//   success: true,
//   profile: {
//     profile_id: "uuid-here",
//     profile_name: "WorkProfile",
//     location: {
//       city: "New York",
//       country: "United States",
//       timezone: "America/New_York"
//     },
//     browser: {
//       user_agent: "Mozilla/5.0 ..."
//     }
//   }
// }
```

#### `listProfiles()`
Get all profiles.

```typescript
const response = await listProfiles();
// Returns: {
//   success: true,
//   profiles: [
//     {
//       profile_id: "uuid-1",
//       profile_name: "WorkProfile",
//       creation_date: "2025-10-04T12:00:00",
//       last_used: "2025-10-04T12:00:00",
//       is_active: true
//     }
//   ],
//   count: 1
// }
```

#### `deleteProfile(profileId)`
Delete a profile.

```typescript
const response = await deleteProfile("uuid-here");
// Returns: {
//   success: true,
//   message: "Profile uuid-here deleted successfully"
// }
```

### Browser Launcher

#### `launchBrowser(profileId, url?)`
Launch an anonymous browser with a profile.

```typescript
const response = await launchBrowser("uuid-here", "https://google.com");
// Returns: {
//   success: true,
//   message: "Browser launching with profile WorkProfile",
//   profile_id: "uuid-here",
//   url: "https://google.com",
//   browser_type: "chromium"
// }
```

**Parameters:**
- `profileId` (string, required): Profile to use
- `url` (string, optional): Starting URL (default: "https://www.google.com")

### Leak Detection

#### `runLeakTest(testType?)`
Run privacy leak detection tests.

```typescript
const response = await runLeakTest("all");
// Returns: {
//   success: true,
//   results: {
//     webrtc: {
//       test_name: "WebRTC Leak",
//       status: "pass",
//       message: "No WebRTC leak detected",
//       details: { public_ip: "1.2.3.4" }
//     },
//     dns: { ... },
//     canvas: { ... },
//     webgl: { ... }
//   },
//   test_count: 7
// }
```

**Parameters:**
- `testType` (string, optional): Test to run ("all", "webrtc", "dns", "canvas", "webgl", "audio", "timezone", "automation")

**Test Statuses:**
- `pass`: Test passed, no leak detected
- `warning`: Potential issue detected
- `fail`: Critical leak detected

---

## Rust Commands

Located in: `src-tauri/src/sidecar.rs`

All Rust commands are async and return `Result<SidecarResponse, String>`.

### Command List

1. `start_sidecar` - Start Python process
2. `ping_sidecar` - Health check
3. `create_profile` - Create new profile
4. `load_profile` - Load profile by ID
5. `list_profiles` - Get all profiles
6. `delete_profile` - Delete profile
7. `get_sidecar_status` - Get backend status
8. `launch_browser` - Launch browser with profile
9. `run_leak_test` - Run leak detection

### Example Rust Command

```rust
#[tauri::command]
pub async fn create_profile(
    sidecar: State<'_, PythonSidecar>,
    profile_name: String,
    location: Option<String>,
) -> Result<SidecarResponse, String> {
    let data = serde_json::json!({
        "profile_name": profile_name,
        "location": location,
    });
    
    sidecar.send_command("create_profile", data)
}
```

---

## Python Sidecar

Located in: `python-backend/main.py`

### Command Handlers

Each command has a corresponding handler method:

```python
def handle_create_profile(self, data: Dict[str, Any]) -> Dict[str, Any]:
    profile_name = data.get('profile_name')
    location = data.get('location')
    
    # Generate profile
    profile = self.profile_generator.generate_profile(
        profile_name=profile_name,
        location_hint=location
    )
    
    # Save to database
    self.profile_db.save_profile(profile)
    
    return {
        'success': True,
        'profile_id': profile.profile_id,
        'profile_name': profile.profile_name,
        'message': f'Profile {profile_name} created successfully'
    }
```

### Available Handlers

- `handle_ping` - Health check
- `handle_create_profile` - Create profile
- `handle_load_profile` - Load profile
- `handle_list_profiles` - List profiles
- `handle_delete_profile` - Delete profile
- `handle_launch_browser` - Launch browser (Playwright)
- `handle_run_leak_test` - Run leak tests
- `handle_get_status` - Get status

---

## Data Types

### TypeScript Interfaces

```typescript
interface SidecarResponse {
  success: boolean;
  error?: string;
  [key: string]: any;
}

interface Profile {
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

interface LeakTestResult {
  test_name: string;
  status: "pass" | "fail" | "warning" | "running";
  message: string;
  details?: any;
}
```

---

## Error Handling

### Error Response Format

```json
{
  "success": false,
  "error": "Detailed error message"
}
```

### Common Errors

1. **Profile Not Found**
   ```json
   {
     "success": false,
     "error": "Profile uuid-here not found"
   }
   ```

2. **Missing Parameters**
   ```json
   {
     "success": false,
     "error": "profile_id is required"
   }
   ```

3. **Sidecar Not Running**
   ```json
   {
     "success": false,
     "error": "Python sidecar not running"
   }
   ```

### Error Handling in TypeScript

```typescript
try {
  const response = await createProfile("MyProfile");
  
  if (response.success) {
    console.log("Profile created:", response.profile_id);
  } else {
    console.error("Error:", response.error);
  }
} catch (err) {
  console.error("Exception:", err);
}
```

---

## Examples

### Complete Workflow Example

```typescript
import {
  startSidecar,
  pingSidecar,
  createProfile,
  loadProfile,
  launchBrowser,
  runLeakTest
} from "./api";

async function completeWorkflow() {
  // 1. Start backend
  await startSidecar();
  
  // 2. Check connection
  const ping = await pingSidecar();
  console.log("Backend version:", ping.version);
  
  // 3. Create profile
  const created = await createProfile("TestProfile", "London");
  const profileId = created.profile_id;
  
  // 4. Load profile details
  const loaded = await loadProfile(profileId);
  console.log("Profile location:", loaded.profile.location);
  
  // 5. Run leak tests
  const leaks = await runLeakTest("all");
  console.log("Tests passed:", leaks.test_count);
  
  // 6. Launch browser
  const browser = await launchBrowser(profileId, "https://example.com");
  console.log("Browser launched:", browser.message);
}
```

---

## Testing

### Integration Tests

Run the test script:

```bash
cd /home/eddie/anon_best/tauri-gui/anonymity-browser
./test_integration.sh
```

### Manual Testing

Test individual commands:

```bash
cd python-backend

# Ping
echo '{"command":"ping","data":{}}' | python3 main.py

# Create profile
echo '{"command":"create_profile","data":{"profile_name":"Test"}}' | python3 main.py

# Run leak test
echo '{"command":"run_leak_test","data":{"test_type":"all"}}' | python3 main.py
```

---

## Performance

### Response Times

- **Ping**: < 10ms
- **Create Profile**: 50-100ms
- **Load Profile**: 10-20ms
- **List Profiles**: 20-50ms
- **Launch Browser**: 2-5 seconds
- **Leak Tests**: 1-3 seconds

### Resource Usage

- **Memory**: ~50MB (Python sidecar)
- **CPU**: < 5% idle, 10-20% during operations
- **Disk**: Minimal (SQLite database)

---

## Security Considerations

1. **IPC Security**: stdin/stdout communication is process-local
2. **Profile Storage**: SQLite database with file permissions
3. **Browser Isolation**: Each profile uses separate browser context
4. **Fingerprint Randomization**: Canvas, WebGL, audio randomized per profile

---

**For more information, see:**
- [User Guide](USER_GUIDE.md)
- [Development Guide](DEVELOPMENT.md)
- [Troubleshooting](TROUBLESHOOTING.md)

