#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$frontend = Join-Path $PSScriptRoot "..\frontend"
Push-Location $frontend
try {
  npm run test
} finally { Pop-Location }
Write-Host "[fe_test] Tests Vitest OK." -ForegroundColor Green

