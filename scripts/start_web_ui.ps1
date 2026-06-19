param(
    [string]$HostAddress = "127.0.0.1",
    [int]$Port = 5173
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
$FrontendRoot = Join-Path $RepoRoot "frontend"

if (-not (Test-Path -LiteralPath $FrontendRoot)) {
    throw "Missing frontend directory. Run Slice 13A first."
}

Set-Location $FrontendRoot
Write-Host "Starting shared web UI at http://$HostAddress`:$Port"
npm run dev -- --host $HostAddress --port $Port
