# Release Workflow

## Targets

This repository has two release targets:

- Local desktop/web release for LocalLite
- Online production profile release for server infrastructure

Both targets come from `main`.

## Local Verification

```powershell
.\scripts\verify_local_release.ps1 -SkipTauriBuild -SkipHealthCheck
```

Run without skips when the backend is running and Tauri builds are permitted by the machine policy:

```powershell
.\scripts\verify_local_release.ps1
```

## Production Configuration Verification

```powershell
.\scripts\verify_production_config.ps1
```

This validates required files, required environment keys, and Docker Compose configuration when Docker is available.

## Branches

- `main`: shared source of truth
- `release/desktop-local`: local desktop/web release target
- `release/online-prod`: production server release target

Release branches should not contain separate product logic.
