# Prepara Node.js LTS portatil e reproduzivel, sem precisar de administrador.
# Este script e carregado por scripts/prepare.ps1.
function Ensure-MagnoliaNode {
    param([Parameter(Mandatory = $true)][string]$ProjectRoot)

    $version = '24.22.1'
    if (-not [Environment]::Is64BitOperatingSystem) {
        throw 'Esta preparacao automatica do Node requer Windows 64 bits.'
    }

    $arch = if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64') { 'win-arm64' } else { 'win-x64' }
    $packageName = "node-v${version}-${arch}"
    $runtime = Join-Path $ProjectRoot '.runtime'
    $nodeDir = Join-Path $runtime $packageName
    $nodeExe = Join-Path $nodeDir 'node.exe'

    # So reutiliza instalacao do proprio projeto com a versao esperada.
    if (Test-Path -LiteralPath $nodeExe) {
        $foundVersion = (& $nodeExe --version 2>$null)
        if (($LASTEXITCODE -eq 0) -and ($foundVersion -eq "v$version")) {
            Write-Host "Node.js $foundVersion ja preparado no projeto." -ForegroundColor Green
            return $nodeDir
        }
    }

    $archiveName = "$packageName.zip"
    $downloadDir = Join-Path $runtime 'downloads'
    $archive = Join-Path $downloadDir $archiveName
    $shaFile = Join-Path $downloadDir "node-v$version-SHASUMS256.txt"
    $officialBase = "https://nodejs.org/dist/v$version"

    New-Item -ItemType Directory -Force -Path $downloadDir | Out-Null
    # PowerShell 5.1 pode usar TLS antigo se nao ativarmos TLS 1.2.
    [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12

    Write-Host "Baixando/verificando Node.js v$version do site oficial..." -ForegroundColor Cyan
    try {
        Invoke-WebRequest -Uri "$officialBase/SHASUMS256.txt" -OutFile $shaFile -UseBasicParsing -ErrorAction Stop
    } catch {
        throw "Nao foi possivel consultar os checksums oficiais do Node em nodejs.org. Confira a internet da escola. Detalhe: $($_.Exception.Message)"
    }

    $expectedSha = $null
    foreach ($line in (Get-Content -LiteralPath $shaFile -Encoding UTF8)) {
        if ($line -match '^([0-9a-fA-F]{64})\s+\*?(.+)$') {
            if ($Matches[2].Trim() -eq $archiveName) {
                $expectedSha = $Matches[1].ToLowerInvariant()
                break
            }
        }
    }
    if (-not $expectedSha) {
        throw "O checksum do arquivo $archiveName nao foi encontrado na lista oficial."
    }

    $archiveValid = $false
    if (Test-Path -LiteralPath $archive) {
        $archiveValid = ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -eq $expectedSha)
    }
    if (-not $archiveValid) {
        if (Test-Path -LiteralPath $archive) { Remove-Item -LiteralPath $archive -Force }
        try {
            Invoke-WebRequest -Uri "$officialBase/$archiveName" -OutFile $archive -UseBasicParsing -ErrorAction Stop
        } catch {
            throw "Nao foi possivel baixar Node.js do endereco oficial. Confira internet/proxy da escola. Detalhe: $($_.Exception.Message)"
        }
    }

    $actualSha = (Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actualSha -ne $expectedSha) {
        Remove-Item -LiteralPath $archive -Force -ErrorAction SilentlyContinue
        throw 'O checksum SHA-256 do Node.js nao corresponde ao valor oficial. O arquivo foi descartado.'
    }

    $temporary = Join-Path $runtime ('node-extract-' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Force -Path $temporary | Out-Null
    try {
        Expand-Archive -LiteralPath $archive -DestinationPath $temporary -Force
        $expanded = Join-Path $temporary $packageName
        if (-not (Test-Path -LiteralPath (Join-Path $expanded 'node.exe'))) {
            throw 'Pacote do Node baixado sem node.exe na pasta esperada.'
        }
        if (Test-Path -LiteralPath $nodeDir) { Remove-Item -LiteralPath $nodeDir -Recurse -Force }
        Move-Item -LiteralPath $expanded -Destination $nodeDir
    } finally {
        if (Test-Path -LiteralPath $temporary) {
            Remove-Item -LiteralPath $temporary -Recurse -Force
        }
    }

    $verifiedVersion = (& $nodeExe --version)
    if (($LASTEXITCODE -ne 0) -or ($verifiedVersion -ne "v$version")) {
        throw "A versao de Node extraida nao corresponde a v$version."
    }
    Write-Host "Node.js $verifiedVersion instalado somente neste projeto." -ForegroundColor Green
    return $nodeDir
}
