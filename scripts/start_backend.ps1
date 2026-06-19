param(
    [string]$HostAddress = "127.0.0.1",
    [int]$Port = 8000,
    [switch]$NoReload
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

$uvicornArgs = @("app.main:app", "--host", $HostAddress, "--port", $Port.ToString())
if (-not $NoReload) {
    $uvicornArgs += "--reload"
}

Write-Host "Starting FastAPI backend at http://$HostAddress`:$Port"
python -m uvicorn @uvicornArgs
