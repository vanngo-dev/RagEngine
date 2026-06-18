# Robust Local RAG Engine

## Codex Vertical Slice Workflow

This repository is set up for phase-gated Codex implementation of the robust local RAG engine v3. The engine itself has not been implemented yet; each future Codex run should implement exactly one vertical slice.

### Generate an Active Prompt

```powershell
.\scripts\run_slice.ps1 `
  -SliceId "slice-00" `
  -SliceFile "docs/codex/slices/slice-00-project-foundation.md"
```

Then paste `docs/codex/ACTIVE_PROMPT.md` into Codex.

### Run Gate

```powershell
.\scripts\run_gate.ps1 -Slice "slice-00"
```

### Commit Slice

```powershell
.\scripts\commit_slice.ps1 `
  -Slice "slice-00" `
  -Message "Slice 00: project foundation"
```
