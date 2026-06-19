param()

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
$FrontendRoot = Join-Path $RepoRoot "frontend"

if (-not (Test-Path -LiteralPath (Join-Path $FrontendRoot "src-tauri"))) {
    throw "Missing Tauri directory. Run Slice 13B first."
}

Set-Location $FrontendRoot
Write-Host "Starting Tauri desktop shell with the shared React UI..."
npm run tauri:dev
