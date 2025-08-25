#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

param(
[int]$Port = 8000
)

Write-Host "[dev_down] Tentative d'arret du serveur sur port $Port..." -ForegroundColor Yellow
$tcp = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
if ($tcp) {
$pid = ($tcp | Select-Object -First 1).OwningProcess
if ($pid) {
try {
Stop-Process -Id $pid -Force -ErrorAction Stop
Write-Host "[dev_down] Processus $pid arrete." -ForegroundColor Green
exit 0
} catch {
Write-Warning "[dev_down] Echec arret PID $pid: $($_.Exception.Message)"
exit 10
}
}
}
Write-Host "[dev_down] Aucun processus ecoute sur $Port." -ForegroundColor Yellow
exit 0

