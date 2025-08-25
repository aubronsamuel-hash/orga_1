#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

param(
  [Parameter(Mandatory=$true)][string]$Email,
  [Parameter(Mandatory=$true)][string]$Password
)

$backend = Join-Path $PSScriptRoot "..\backend"
$py = Join-Path $backend ".venv\Scripts\python.exe"

$code = @"
from app.db import get_engine, session_scope, Base
from app.models import User
from app.security import hash_password

Base.metadata.create_all(get_engine())
with session_scope() as s:
    u = s.query(User).filter(User.email == "$Email").first()
    if not u:
        u = User(email="$Email", password_hash=hash_password("$Password"), is_admin=True, is_active=True)
        s.add(u)
        print("Admin cree:", u.email)
    else:
        u.is_admin = True
        s.commit()
        print("Admin deja present, flag admin mis a True:", u.email)
"@

Push-Location $backend
try {
  & $py - <<PY
$code
PY
} finally { Pop-Location }

