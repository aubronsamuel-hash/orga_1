#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$backend = Join-Path $PSScriptRoot "..\backend"
$py = Join-Path $backend ".venv\Scripts\python.exe"

Push-Location $backend
try {
  & $py -m pytest -q --cov=backend --cov-report=term-missing
} finally { Pop-Location }

$frontend = Join-Path $PSScriptRoot "..\frontend"
Push-Location $frontend
try {
  npm run build
} finally { Pop-Location }

Write-Host "[test_all] OK." -ForegroundColor Green
exit 0
