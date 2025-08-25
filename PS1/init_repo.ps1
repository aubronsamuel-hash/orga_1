#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$EXIT_OK = 0
$EXIT_USAGE = 1
$EXIT_PREREQ = 2
$EXIT_TIMEOUT = 3
$EXIT_NET = 4
$EXIT_AUTH = 5
$EXIT_INTERNAL = 10

function Test-Cmd { param([Parameter(Mandatory=$true)][string]$Name)
  return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

Write-Host "[init_repo] Verification des prerequis..." -ForegroundColor Green
if (-not (Test-Cmd -Name "python")) { Write-Error "Python non trouve"; exit $EXIT_PREREQ }
if (-not (Test-Cmd -Name "pip")) { Write-Error "pip non trouve"; exit $EXIT_PREREQ }
if (-not (Test-Cmd -Name "node")) { Write-Error "Node.js non trouve"; exit $EXIT_PREREQ }
if (-not (Test-Cmd -Name "npm"))  { Write-Error "npm non trouve"; exit $EXIT_PREREQ }
if (-not (Test-Cmd -Name "git"))  { Write-Error "git non trouve"; exit $EXIT_PREREQ }

# Backend venv + deps
$backend = Join-Path $PSScriptRoot "..\backend"
Push-Location $backend
try {
  if (-not (Test-Path ".venv")) {
    python -m venv .venv
  }
  & ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
  & ".\.venv\Scripts\python.exe" -m pip install -r requirements-dev.txt
} finally { Pop-Location }

# Frontend deps
$frontend = Join-Path $PSScriptRoot "..\frontend"
Push-Location $frontend
try {
  npm ci --no-audit --no-fund
} finally { Pop-Location }

# pre-commit
Write-Host "[init_repo] Installation pre-commit..." -ForegroundColor Green
& "$backend\.venv\Scripts\python.exe" -m pip install pre-commit
& "$backend\.venv\Scripts\python.exe" -m pre-commit install

Write-Host "[init_repo] OK." -ForegroundColor Green
exit $EXIT_OK
