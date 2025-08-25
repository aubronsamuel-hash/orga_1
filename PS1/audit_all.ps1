#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$EXIT_PREREQ = 2

# Backend audits
$backend = Join-Path $PSScriptRoot "..\backend"
$py = Join-Path $backend ".venv\Scripts\python.exe"
Push-Location $backend
try {
  try { & $py -m pip_audit --progress-spinner=off } catch { Write-Warning "pip-audit indisponible"; exit $EXIT_PREREQ }
  try { & $py -m bandit -q -r backend } catch { Write-Warning "bandit indisponible" }
} finally { Pop-Location }

# Frontend audits
$frontend = Join-Path $PSScriptRoot "..\frontend"
Push-Location $frontend
try {
  try { npm audit --audit-level=high } catch { Write-Warning "npm audit indisponible"; exit $EXIT_PREREQ }
} finally { Pop-Location }

Write-Host "[audit_all] Termine." -ForegroundColor Green
exit 0
