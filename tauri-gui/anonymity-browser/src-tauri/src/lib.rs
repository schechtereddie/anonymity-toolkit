// Modules
mod sidecar;

use sidecar::PythonSidecar;
use tauri::Manager;

// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    // Initialize Python sidecar
    let python_sidecar = PythonSidecar::new();

    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .manage(python_sidecar)
        .invoke_handler(tauri::generate_handler![
            greet,
            sidecar::start_sidecar,
            sidecar::ping_sidecar,
            sidecar::create_profile,
            sidecar::load_profile,
            sidecar::list_profiles,
            sidecar::delete_profile,
            sidecar::get_sidecar_status,
            sidecar::launch_browser,
            sidecar::run_leak_test,
        ])
        .setup(|app| {
            // Auto-start the Python sidecar
            let sidecar = app.state::<PythonSidecar>();
            if let Err(e) = sidecar.start() {
                eprintln!("Failed to start Python sidecar: {}", e);
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
