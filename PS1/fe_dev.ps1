#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$frontend = Join-Path $PSScriptRoot "..\frontend"

Write-Host "[fe_dev] Lancement Vite (port 5173)..." -ForegroundColor Green
Push-Location $frontend
try {
  npm run dev
} finally { Pop-Location }

