#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$frontend = Join-Path $PSScriptRoot "..\frontend"
Push-Location $frontend
try {
  npm run lint
  npm run typecheck
} finally { Pop-Location }
Write-Host "[fe_lint] Lint + typecheck OK." -ForegroundColor Green

