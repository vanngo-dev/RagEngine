# Desktop Release

## Target

`release/desktop-local` is for LocalLite plus the shared React UI and Tauri desktop wrapper.

## Run Locally

Start the backend:

```powershell
.\scripts\start_backend.ps1
```

Start the web UI:

```powershell
.\scripts\start_web_ui.ps1
```

Start the desktop shell:

```powershell
.\scripts\start_desktop_ui.ps1
```

## Verify

```powershell
.\scripts\verify_local_release.ps1
```

Use these skips when validating on a machine that cannot run Tauri build scripts or does not have the backend already running:

```powershell
.\scripts\verify_local_release.ps1 -SkipTauriBuild -SkipHealthCheck
```

## Known Limitations

- The desktop shell does not bundle the FastAPI backend as a sidecar yet.
- Tauri builds require Rust, Tauri prerequisites, and a local policy that permits Cargo build scripts.
- LocalLite remains single-user local storage.
