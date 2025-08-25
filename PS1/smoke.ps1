#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

param([string]$BaseUrl = "http://localhost:8000/api/v1")

function Invoke-Json {
param([string]$Url)
$r = Invoke-WebRequest -UseBasicParsing -Uri $Url -Method GET -Headers @{"X-Request-ID"="ps1-smoke"}
if ($r.StatusCode -ne 200) { throw "HTTP $($r.StatusCode) sur $Url" }
return ($r.Content | ConvertFrom-Json)
}

$h = Invoke-Json -Url ($BaseUrl + "/health")
if ($h.status -ne "ok") { throw "Health != ok" }

$v = Invoke-Json -Url ($BaseUrl + "/version")
if (-not $v.version) { throw "Version vide" }

Write-Host "[smoke] OK health/version." -ForegroundColor Green
exit 0

