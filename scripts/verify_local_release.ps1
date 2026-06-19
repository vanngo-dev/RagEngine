param(
    [string]$HealthUrl = "http://127.0.0.1:8000/health",
    [switch]$SkipFrontendBuild,
    [switch]$SkipTauriBuild,
    [switch]$SkipHealthCheck
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
$FrontendRoot = Join-Path $RepoRoot "frontend"
Set-Location $RepoRoot

Write-Host "Running backend tests..."
python -m pytest -q

Write-Host "Running lightweight eval..."
python -m rag_engine.evals.lightweight_eval

if (-not $SkipFrontendBuild) {
    Write-Host "Building shared web UI..."
    Push-Location $FrontendRoot
    npm run build
    Pop-Location
}
else {
    Write-Host "Skipping frontend build."
}

if (-not $SkipTauriBuild) {
    Write-Host "Building Tauri desktop shell..."
    Push-Location $FrontendRoot
    npm run tauri:build
    Pop-Location
}
else {
    Write-Host "Skipping Tauri build."
}

if (-not $SkipHealthCheck) {
    Write-Host "Checking backend health at $HealthUrl..."
    $health = Invoke-RestMethod -Uri $HealthUrl -Method Get
    if ($health.status -ne "ok") {
        throw "Health check did not return status=ok."
    }
    Write-Host "Health check passed."
}
else {
    Write-Host "Skipping health check."
}

Write-Host "Local release verification completed."
