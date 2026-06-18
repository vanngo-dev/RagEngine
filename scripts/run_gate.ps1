param(
    [Parameter(Mandatory=$true)]
    [string]$Slice
)

$ErrorActionPreference = "Stop"

Write-Host "========================================"
Write-Host "Running gate for $Slice"
Write-Host "========================================"

if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating existing virtual environment..."
    & .\.venv\Scripts\Activate.ps1
}
elseif ((Test-Path "pyproject.toml") -or (Test-Path "requirements.txt")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
    & .\.venv\Scripts\Activate.ps1
}
else {
    Write-Host "No Python project files found yet. Skipping virtual environment setup."
}

if (Test-Path "requirements.txt") {
    Write-Host "Installing requirements..."
    python -m pip install -r requirements.txt
}

if (Test-Path "pyproject.toml") {
    Write-Host "Installing project in editable mode..."
    python -m pip install -e .
}

if (Test-Path "tests") {
    Write-Host "Running pytest..."
    python -m pytest -q

    if ($LASTEXITCODE -ne 0) {
        throw "Tests failed. Gate blocked."
    }
}
else {
    Write-Host "No tests folder found yet. This is only acceptable before Slice 00 is implemented."
}

Write-Host "Checking docs/youtube folder..."
if (Test-Path "docs/youtube") {
    $phaseDocs = Get-ChildItem "docs/youtube" -Filter "*.md" -ErrorAction SilentlyContinue

    if ($phaseDocs.Count -eq 0) {
        Write-Host "Warning: docs/youtube exists but contains no Markdown files."
    }
}
else {
    Write-Host "Warning: docs/youtube folder does not exist yet."
}

Write-Host "Gate passed for $Slice"

