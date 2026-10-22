$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $projectRoot
# Usa sempre Node.js portatil versionado pelo projeto, evitando o Node antigo do Windows.
. (Join-Path $PSScriptRoot 'ensure_node.ps1')
$nodeDir = Ensure-MagnoliaNode -ProjectRoot $projectRoot
$env:PATH = $nodeDir + ';' + $env:PATH
$nodeExe = Join-Path $nodeDir 'node.exe'
$npxExe = Join-Path $nodeDir 'npx.cmd'
$npmExe = Join-Path $nodeDir 'npm.cmd'
Write-Host ('Node.js em uso: ' + (& $nodeExe --version)) -ForegroundColor Green
$runtimeBase = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies'
$pythonExe = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonExe)) {
    $pythonCandidates = @((Join-Path $runtimeBase 'python\python.exe'))
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCommand) { $pythonCandidates += $pythonCommand.Source }
    $basePython = $null
    foreach ($candidate in $pythonCandidates) {
        if ((Test-Path -LiteralPath $candidate) -and ($candidate -notlike '*WindowsApps*')) {
            & $candidate -c 'import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)'
            if ($LASTEXITCODE -eq 0) { $basePython = $candidate; break }
        }
    }
    if (-not $basePython) { throw 'Instale Python 3.11 ou superior de python.org com Add Python to PATH.' }
    & $basePython -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao criar ambiente Python.' }
}
& $pythonExe -m pip install -r backend/requirements-lock.txt
if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar dependencias Python.' }
& $pythonExe scripts/download_mysql.py
if ($LASTEXITCODE -ne 0) { throw 'Falha ao preparar MySQL.' }
& $pythonExe scripts/mysql_local.py
if ($LASTEXITCODE -ne 0) { throw 'Falha ao iniciar MySQL.' }
& $pythonExe -m backend.seed
if ($LASTEXITCODE -ne 0) { throw 'Falha ao preparar banco.' }
# O pnpm fixado em frontend/package.json e executado com o Node portatil acima.
# Nao utiliza pnpm global, Corepack global nem o Node antigo da escola.
$env:CI = 'true'
$env:COREPACK_ENABLE_DOWNLOAD_PROMPT = '0'
$env:npm_config_update_notifier = 'false'
Push-Location frontend
try {
    & $npxExe --yes pnpm@11.19.0 install --frozen-lockfile
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar dependencias do frontend.' }
    & $npmExe run build
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao compilar o frontend React/TypeScript.' }
} finally { Pop-Location }
Write-Host 'Preparacao concluida. Abra iniciar.cmd.' -ForegroundColor Green
