use serde::{Deserialize, Serialize};
use std::io::{BufRead, BufReader, Write};
use std::process::{Child, Command, Stdio};
use std::sync::{Arc, Mutex};
use tauri::State;

#[derive(Debug, Serialize, Deserialize)]
pub struct SidecarMessage {
    pub command: String,
    pub data: serde_json::Value,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct SidecarResponse {
    pub success: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<String>,
    #[serde(flatten)]
    pub data: serde_json::Value,
}

pub struct PythonSidecar {
    process: Arc<Mutex<Option<Child>>>,
}

impl PythonSidecar {
    pub fn new() -> Self {
        Self {
            process: Arc::new(Mutex::new(None)),
        }
    }

    pub fn start(&self) -> Result<(), String> {
        let mut process_guard = self.process.lock().unwrap();
        
        if process_guard.is_some() {
            return Ok(()); // Already running
        }

        // Get the path to the Python sidecar
        let python_path = std::env::current_dir()
            .map_err(|e| format!("Failed to get current directory: {}", e))?
            .join("../python-backend/main.py");

        println!("Starting Python sidecar at: {:?}", python_path);

        // Start the Python process
        let child = Command::new("python3")
            .arg(python_path)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .map_err(|e| format!("Failed to start Python sidecar: {}", e))?;

        println!("Python sidecar started with PID: {:?}", child.id());

        *process_guard = Some(child);
        Ok(())
    }

    pub fn send_command(&self, command: &str, data: serde_json::Value) -> Result<SidecarResponse, String> {
        let mut process_guard = self.process.lock().unwrap();
        
        let process = process_guard
            .as_mut()
            .ok_or_else(|| "Python sidecar not running".to_string())?;

        // Create message
        let message = SidecarMessage {
            command: command.to_string(),
            data,
        };

        // Serialize to JSON
        let json_message = serde_json::to_string(&message)
            .map_err(|e| format!("Failed to serialize message: {}", e))?;

        // Send to Python process
        let stdin = process
            .stdin
            .as_mut()
            .ok_or_else(|| "Failed to get stdin".to_string())?;

        writeln!(stdin, "{}", json_message)
            .map_err(|e| format!("Failed to write to stdin: {}", e))?;

        stdin.flush()
            .map_err(|e| format!("Failed to flush stdin: {}", e))?;

        // Read response from Python process
        let stdout = process
            .stdout
            .as_mut()
            .ok_or_else(|| "Failed to get stdout".to_string())?;

        let mut reader = BufReader::new(stdout);
        let mut response_line = String::new();
        
        reader.read_line(&mut response_line)
            .map_err(|e| format!("Failed to read response: {}", e))?;

        // Parse response
        let response: SidecarResponse = serde_json::from_str(&response_line)
            .map_err(|e| format!("Failed to parse response: {}", e))?;

        Ok(response)
    }

    pub fn stop(&self) -> Result<(), String> {
        let mut process_guard = self.process.lock().unwrap();
        
        if let Some(mut child) = process_guard.take() {
            child.kill()
                .map_err(|e| format!("Failed to kill Python sidecar: {}", e))?;
            println!("Python sidecar stopped");
        }
        
        Ok(())
    }
}

impl Drop for PythonSidecar {
    fn drop(&mut self) {
        let _ = self.stop();
    }
}

// Tauri commands

#[tauri::command]
pub async fn start_sidecar(sidecar: State<'_, PythonSidecar>) -> Result<String, String> {
    sidecar.start()?;
    Ok("Python sidecar started successfully".to_string())
}

#[tauri::command]
pub async fn ping_sidecar(sidecar: State<'_, PythonSidecar>) -> Result<SidecarResponse, String> {
    sidecar.send_command("ping", serde_json::json!({}))
}

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

#[tauri::command]
pub async fn load_profile(
    sidecar: State<'_, PythonSidecar>,
    profile_id: String,
) -> Result<SidecarResponse, String> {
    let data = serde_json::json!({
        "profile_id": profile_id,
    });
    
    sidecar.send_command("load_profile", data)
}

#[tauri::command]
pub async fn list_profiles(
    sidecar: State<'_, PythonSidecar>,
) -> Result<SidecarResponse, String> {
    sidecar.send_command("list_profiles", serde_json::json!({}))
}

#[tauri::command]
pub async fn delete_profile(
    sidecar: State<'_, PythonSidecar>,
    profile_id: String,
) -> Result<SidecarResponse, String> {
    let data = serde_json::json!({
        "profile_id": profile_id,
    });
    
    sidecar.send_command("delete_profile", data)
}

#[tauri::command]
pub async fn get_sidecar_status(
    sidecar: State<'_, PythonSidecar>,
) -> Result<SidecarResponse, String> {
    sidecar.send_command("get_status", serde_json::json!({}))
}

#[tauri::command]
pub async fn launch_browser(
    sidecar: State<'_, PythonSidecar>,
    profile_id: String,
    url: Option<String>,
) -> Result<SidecarResponse, String> {
    let data = serde_json::json!({
        "profile_id": profile_id,
        "url": url,
    });
    
    sidecar.send_command("launch_browser", data)
}

#[tauri::command]
pub async fn run_leak_test(
    sidecar: State<'_, PythonSidecar>,
    test_type: Option<String>,
) -> Result<SidecarResponse, String> {
    let data = serde_json::json!({
        "test_type": test_type,
    });
    
    sidecar.send_command("run_leak_test", data)
}

