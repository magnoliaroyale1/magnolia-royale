$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $projectRoot
$pythonExe = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonExe)) { throw 'Execute preparar.cmd primeiro.' }
if (Test-Path -LiteralPath '.runtime\mysql-local.json') {
    & $pythonExe scripts/mysql_local.py
    if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel iniciar o MySQL.' }
}
if (-not (Test-Path -LiteralPath 'frontend\dist\index.html')) { throw 'Execute preparar.cmd para compilar as telas.' }
& $pythonExe -m backend.seed
if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel acessar o banco. Confira backend/.env.' }
try {
    $health = Invoke-RestMethod -Uri 'http://127.0.0.1:5000/api/health' -TimeoutSec 2
    if ($health.status -eq 'ok') { Write-Host 'Sistema ja disponivel em http://127.0.0.1:5000'; exit 0 }
} catch { }
Write-Host 'Abra http://127.0.0.1:5000 no navegador. Ctrl+C encerra a API.' -ForegroundColor Green
& $pythonExe -m backend.app
exit $LASTEXITCODE
