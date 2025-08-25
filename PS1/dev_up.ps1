#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Import-DotEnv {
param([string]$Path = (Join-Path (Split-Path $PSScriptRoot -Parent) ".env"))
if (-not (Test-Path $Path)) { return }
Get-Content $Path | ForEach-Object {
if ($_ -match '^\s*#') { return }
if ($_ -match '^\s*$') { return }
$kv = $_ -split '=', 2
if ($kv.Length -eq 2) {
$name = $kv[0].Trim()
$value = $kv[1].Trim()
if (-not [string]::IsNullOrWhiteSpace($name)) { $Env:$name = $value }
}
}
}

Import-DotEnv

$backend = Join-Path $PSScriptRoot "..\backend"
$py = Join-Path $backend ".venv\Scripts\python.exe"
$host = $Env:API_HOST
$port = [int]($Env:API_PORT)

if (-not (Test-Path $py)) { throw "Environnement Python manquant (.venv). Lancez PS1\init_repo.ps1." }

Write-Host "[dev_up] Lancement Uvicorn sur http://$host:$port ..." -ForegroundColor Green
Push-Location $backend
try {
& $py -m uvicorn app.main:app --reload --host $host --port $port
} finally {
Pop-Location
}

