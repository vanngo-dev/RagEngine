param(
    [Parameter(Mandatory=$true)]
    [string]$SliceId,

    [Parameter(Mandatory=$true)]
    [string]$SliceFile
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path "docs/codex/MASTER_RULES.md")) {
    throw "Missing docs/codex/MASTER_RULES.md"
}

if (-not (Test-Path $SliceFile)) {
    throw "Missing slice file: $SliceFile"
}

if (-not (Test-Path "docs/spec/RAG_ENGINE_V3.md")) {
    throw "Missing docs/spec/RAG_ENGINE_V3.md"
}

$masterRules = Get-Content "docs/codex/MASTER_RULES.md" -Raw
$slicePrompt = Get-Content $SliceFile -Raw
$v3Spec = Get-Content "docs/spec/RAG_ENGINE_V3.md" -Raw

$activePrompt = @"
# ACTIVE CODEX PROMPT

You are implementing one vertical slice of the robust local RAG engine v3.

Do not implement the whole engine.
Do not go beyond the requested slice.

---

# Master Rules

$masterRules

---

# v3 Spec Reference

Use this as the project specification.
Do not implement the whole spec now.
Only implement the requested slice.

$v3Spec

---

# Current Slice

$slicePrompt
"@

Set-Content "docs/codex/ACTIVE_PROMPT.md" $activePrompt

Write-Host "========================================"
Write-Host "Active Codex prompt created:"
Write-Host "docs/codex/ACTIVE_PROMPT.md"
Write-Host "========================================"
Write-Host ""
Write-Host "Next:"
Write-Host "1. Open docs/codex/ACTIVE_PROMPT.md"
Write-Host "2. Paste it into Codex"
Write-Host "3. Let Codex implement the slice"
Write-Host "4. Run:"
Write-Host "   .\scripts\run_gate.ps1 -Slice $SliceId"
Write-Host ""
