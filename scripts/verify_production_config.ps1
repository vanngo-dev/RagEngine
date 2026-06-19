param(
    [switch]$SkipDocker
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

$requiredFiles = @(
    "docker-compose.production.yml",
    ".env.production.example",
    "docs/production.md",
    "docs/online-release.md"
)

foreach ($file in $requiredFiles) {
    if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot $file))) {
        throw "Missing required production release file: $file"
    }
}

$requiredEnvKeys = @(
    "STORAGE_PROFILE=production",
    "POSTGRES_DSN=",
    "QDRANT_URL=",
    "OPENSEARCH_URL=",
    "REDIS_URL="
)

$envExample = Get-Content -Raw -LiteralPath (Join-Path $RepoRoot ".env.production.example")
foreach ($key in $requiredEnvKeys) {
    if (-not $envExample.Contains($key)) {
        throw "Missing required production env key: $key"
    }
}

if (-not $SkipDocker) {
    $docker = Get-Command "docker" -ErrorAction SilentlyContinue
    if ($null -eq $docker) {
        Write-Host "Docker is not available; skipping docker compose config validation."
    }
    else {
        Write-Host "Validating production Docker Compose configuration..."
        docker compose -f docker-compose.production.yml config | Out-Null
    }
}
else {
    Write-Host "Skipping Docker validation."
}

Write-Host "Production configuration verification completed."
