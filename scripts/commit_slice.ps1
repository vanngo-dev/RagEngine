param(
    [Parameter(Mandatory=$true)]
    [string]$Slice,

    [Parameter(Mandatory=$true)]
    [string]$Message
)

$ErrorActionPreference = "Stop"

Write-Host "Git status:"
git status --short

$changes = git status --short

if ([string]::IsNullOrWhiteSpace($changes)) {
    throw "No changes to commit."
}

git add .

git commit -m "$Message"

Write-Host "Committed $Slice"
