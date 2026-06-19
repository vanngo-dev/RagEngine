param(
    [ValidateRange(0, 12)]
    [int]$Start = 0,

    [ValidateRange(0, 12)]
    [int]$End = 12,

    [switch]$AutoCodex,

    [switch]$NoCommit
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

$Slices = @(
  @{
    Id = "slice-00"
    File = "docs/codex/slices/slice-00-project-foundation.md"
    Commit = "Slice 00: project foundation"
  },
  @{
    Id = "slice-01"
    File = "docs/codex/slices/slice-01-document-pipeline.md"
    Commit = "Slice 01: minimal document pipeline"
  },
  @{
    Id = "slice-02"
    File = "docs/codex/slices/slice-02-searchable-rag.md"
    Commit = "Slice 02: searchable RAG retrieval"
  },
  @{
    Id = "slice-03"
    File = "docs/codex/slices/slice-03-answer-citations.md"
    Commit = "Slice 03: grounded answers with citations"
  },
  @{
    Id = "slice-04"
    File = "docs/codex/slices/slice-04-eval-debug.md"
    Commit = "Slice 04: lightweight eval and debug trace"
  },
  @{
    Id = "slice-05"
    File = "docs/codex/slices/slice-05-hybrid-rrf.md"
    Commit = "Slice 05: hybrid retrieval with RRF"
  },
  @{
    Id = "slice-06"
    File = "docs/codex/slices/slice-06-metadata-supersession.md"
    Commit = "Slice 06: metadata filters and supersession"
  },
  @{
    Id = "slice-07"
    File = "docs/codex/slices/slice-07-reranker-evidence.md"
    Commit = "Slice 07: reranker and evidence selector"
  },
  @{
    Id = "slice-08"
    File = "docs/codex/slices/slice-08-prompt-injection-defense.md"
    Commit = "Slice 08: prompt injection defense"
  },
  @{
    Id = "slice-09"
    File = "docs/codex/slices/slice-09-claim-verification.md"
    Commit = "Slice 09: structured claims and citation verification"
  },
  @{
    Id = "slice-10"
    File = "docs/codex/slices/slice-10-confidence-refusal.md"
    Commit = "Slice 10: confidence and refusal"
  },
  @{
    Id = "slice-11"
    File = "docs/codex/slices/slice-11-full-eval-harness.md"
    Commit = "Slice 11: full evaluation harness"
  },
  @{
    Id = "slice-12"
    File = "docs/codex/slices/slice-12-production-adapter-interfaces.md"
    Commit = "Slice 12: production adapter interfaces"
  }
)

if ($Start -gt $End) {
    throw "-Start must be less than or equal to -End."
}

if ($AutoCodex -and [string]::IsNullOrWhiteSpace($env:CODEX_CMD)) {
    throw "-AutoCodex requires the CODEX_CMD environment variable. Example: `$env:CODEX_CMD = 'REPLACE_WITH_CODEX_CLI_COMMAND'"
}

function Resolve-RepoPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    return Join-Path $RepoRoot $Path
}

function Assert-RequiredFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath (Resolve-RepoPath $Path))) {
        throw "Missing required file: $Path"
    }
}

function Get-CurrentPowerShellExecutable {
    $currentProcess = Get-Process -Id $PID

    if (-not [string]::IsNullOrWhiteSpace($currentProcess.Path)) {
        return $currentProcess.Path
    }

    $pwsh = Get-Command "pwsh" -ErrorAction SilentlyContinue
    if ($null -ne $pwsh) {
        return $pwsh.Source
    }

    $powershell = Get-Command "powershell" -ErrorAction Stop
    return $powershell.Source
}

function Invoke-SlicePromptGeneration {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Slice
    )

    & (Resolve-RepoPath "scripts/run_slice.ps1") `
        -SliceId $Slice["Id"] `
        -SliceFile $Slice["File"]

    Assert-RequiredFile "docs/codex/ACTIVE_PROMPT.md"
}

function Invoke-AutoCodexCommand {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Slice
    )

    $activePromptPath = (Resolve-Path -LiteralPath (Resolve-RepoPath "docs/codex/ACTIVE_PROMPT.md")).Path

    $env:CODEX_ACTIVE_PROMPT = $activePromptPath
    $env:CODEX_SLICE_ID = $Slice["Id"]
    $env:CODEX_SLICE_FILE = $Slice["File"]

    $command = $env:CODEX_CMD
    $command = $command.Replace("{PromptFile}", $activePromptPath)
    $command = $command.Replace("{ActivePrompt}", $activePromptPath)
    $command = $command.Replace("{SliceId}", $Slice["Id"])
    $command = $command.Replace("{SliceFile}", $Slice["File"])

    Write-Host ""
    Write-Host "Running CODEX_CMD for $($Slice["Id"])..."
    Write-Host "CODEX_ACTIVE_PROMPT=$activePromptPath"
    Write-Host ""

    $global:LASTEXITCODE = 0
    Invoke-Expression $command

    if ($global:LASTEXITCODE -ne 0) {
        throw "CODEX_CMD failed for $($Slice["Id"]) with exit code $global:LASTEXITCODE."
    }
}

function Invoke-GateWithCapture {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SliceId
    )

    $powerShellExe = Get-CurrentPowerShellExecutable
    $gateScript = Resolve-RepoPath "scripts/run_gate.ps1"
    $arguments = @("-NoProfile")

    if ($env:OS -eq "Windows_NT") {
        $arguments += @("-ExecutionPolicy", "Bypass")
    }

    $arguments += @("-File", $gateScript, "-Slice", $SliceId)

    Write-Host ""
    Write-Host "Running gate for $SliceId..."
    Write-Host ""

    $output = & $powerShellExe @arguments 2>&1
    $exitCode = $global:LASTEXITCODE
    $outputText = ($output | Out-String).TrimEnd()

    return [pscustomobject]@{
        Passed = ($exitCode -eq 0)
        ExitCode = $exitCode
        Output = $outputText
    }
}

function Write-FixPrompt {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SliceId,

        [Parameter(Mandatory = $true)]
        [string]$GateOutput
    )

    $fixPromptPath = Resolve-RepoPath "docs/codex/ACTIVE_FIX_PROMPT.md"
    $capturedOutput = $GateOutput

    if ([string]::IsNullOrWhiteSpace($capturedOutput)) {
        $capturedOutput = "(No gate output was captured.)"
    }

    $fixPrompt = @(
        "# ACTIVE FIX PROMPT",
        "",
        "The gate failed for $SliceId.",
        "",
        "Fix only the failing tests and code needed for this slice.",
        "Do not add new features.",
        "Do not implement future slices.",
        "Do not weaken or delete tests unless replacing them with better tests.",
        "",
        "## Failed Gate Output",
        "",
        "````text",
        $capturedOutput,
        "````"
    ) -join "`r`n"

    Set-Content -LiteralPath $fixPromptPath -Value $fixPrompt -Encoding UTF8
    Write-Host "Fix prompt created: docs/codex/ACTIVE_FIX_PROMPT.md"
}

function Invoke-SliceCommit {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Slice
    )

    & (Resolve-RepoPath "scripts/commit_slice.ps1") `
        -Slice $Slice["Id"] `
        -Message $Slice["Commit"]
}

Assert-RequiredFile "scripts/run_slice.ps1"
Assert-RequiredFile "scripts/run_gate.ps1"
Assert-RequiredFile "scripts/commit_slice.ps1"

for ($index = $Start; $index -le $End; $index++) {
    Assert-RequiredFile $Slices[$index]["File"]
}

$mode = "manual"
if ($AutoCodex) {
    $mode = "auto"
}

Write-Host "========================================"
Write-Host "Running vertical slices $Start through $End in $mode mode"
Write-Host "NoCommit: $($NoCommit.IsPresent)"
Write-Host "========================================"

for ($index = $Start; $index -le $End; $index++) {
    $slice = $Slices[$index]

    Write-Host ""
    Write-Host "========================================"
    Write-Host "Preparing $($slice["Id"])"
    Write-Host "Prompt: $($slice["File"])"
    Write-Host "========================================"

    Invoke-SlicePromptGeneration -Slice $slice

    if ($AutoCodex) {
        Invoke-AutoCodexCommand -Slice $slice
    }
    else {
        Write-Host ""
        Write-Host "Manual Codex step required for $($slice["Id"])."
        Write-Host "1. Open docs/codex/ACTIVE_PROMPT.md."
        Write-Host "2. Paste the full file into Codex."
        Write-Host "3. Let Codex implement only this slice."
        Write-Host "4. Return here after Codex is finished."
        Write-Host ""
        Read-Host "Press Enter to run the gate for $($slice["Id"])"
    }

    $gate = Invoke-GateWithCapture -SliceId $slice["Id"]

    if (-not $gate.Passed) {
        Write-Host $gate.Output
        Write-FixPrompt -SliceId $slice["Id"] -GateOutput $gate.Output
        Write-Host ""
        Write-Host "Gate failed for $($slice["Id"]). Stopping."

        if ($gate.ExitCode -ne 0) {
            exit $gate.ExitCode
        }

        exit 1
    }

    Write-Host $gate.Output
    Write-Host ""
    Write-Host "Gate passed for $($slice["Id"])."

    if ($NoCommit) {
        Write-Host "Skipping commit for $($slice["Id"]) because -NoCommit was set."
    }
    else {
        Invoke-SliceCommit -Slice $slice
    }
}

Write-Host ""
Write-Host "All requested slices completed."
