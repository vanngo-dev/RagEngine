# Branching Strategy

## Source of Truth

`main` is the shared source of truth for backend, web UI, desktop wrapper, production adapter skeletons, and release scripts.

## Feature Branches

Slice 13 feature work is split by concern:

- `feature/13a-shared-web-ui`
- `feature/13b-tauri-desktop`
- `feature/13c-production-adapters`
- `feature/13d-release-packaging`

Each feature branch is merged back into `main` after validation.

## Release Branches

Release branches are targets, not separate products:

- `release/desktop-local`: LocalLite plus shared React UI and Tauri desktop packaging
- `release/online-prod`: production Docker/server profile and release documentation

Do not develop unique app logic directly on release branches. Branch from `main`, adjust target packaging/configuration only when needed, and merge source changes through `main`.

## Release Flow

```powershell
git checkout main
git checkout -B release/desktop-local
git checkout main
git checkout -B release/online-prod
git checkout main
```

Do not push release branches unless explicitly requested.
