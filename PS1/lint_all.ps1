#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$backend = Join-Path $PSScriptRoot "..\backend"
$py = Join-Path $backend ".venv\Scripts\python.exe"

Push-Location $backend
try {
  & $py -m ruff check .
  & $py -m mypy .
} finally { Pop-Location }

$frontend = Join-Path $PSScriptRoot "..\frontend"
Push-Location $frontend
try {
  npm run lint
} finally { Pop-Location }

Write-Host "[lint_all] OK." -ForegroundColor Green
exit 0
