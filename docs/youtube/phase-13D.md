# Phase 13D — Packaging and Release Workflow

## Video Goal

Add release scripts and documentation for local desktop/web and online production targets without changing core app logic.

## What Changed

- Added backend, web UI, and desktop UI start scripts.
- Added local release verification script.
- Added production configuration verification script.
- Added release documentation:
  - `docs/release.md`
  - `docs/desktop-release.md`
  - `docs/online-release.md`
  - `docs/BRANCHING_STRATEGY.md`
- Documented release branches as targets derived from `main`.

## Local Release Commands

```powershell
.\scripts\start_backend.ps1
.\scripts\start_web_ui.ps1
.\scripts\start_desktop_ui.ps1
.\scripts\verify_local_release.ps1
```

## Production Release Commands

```powershell
.\scripts\verify_production_config.ps1
docker compose -f docker-compose.production.yml config
```

## Known Limitations

- Tauri build validation can be blocked by local application control policy.
- Production adapters are skeletons.
- Release branches should not contain unique app logic.
