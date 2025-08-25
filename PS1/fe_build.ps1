#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$frontend = Join-Path $PSScriptRoot "..\frontend"
Push-Location $frontend
try {
  npm run build
} finally { Pop-Location }
Write-Host "[fe_build] Build OK." -ForegroundColor Green

