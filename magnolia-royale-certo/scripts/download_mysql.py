"""Baixa o pacote oficial para uma instalação portátil dentro do projeto."""
import hashlib
from pathlib import Path
from urllib.request import urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]
runtime = ROOT / '.runtime'
runtime.mkdir(exist_ok=True)
version = '8.4.11'
expected = 'a492371d687d2bab088b0062581144a0044b8964baefdf4faa579292b423d25c'
binary = runtime / f'mysql-{version}-winx64/bin/mysqld.exe'
if binary.exists():
    print('MySQL portátil já instalado.')
    raise SystemExit(0)
archive = runtime / 'mysql.zip'
def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()
if not archive.exists() or digest(archive) != expected:
    print('Baixando MySQL 8.4.11 do site oficial...', flush=True)
    with urlopen(f'https://cdn.mysql.com/Downloads/MySQL-8.4/mysql-{version}-winx64.zip', timeout=60) as source, archive.open('wb') as target:
        while chunk := source.read(1024 * 1024):
            target.write(chunk)
if digest(archive) != expected:
    raise SystemExit('A verificação do pacote MySQL falhou. O arquivo não será executado.')
with zipfile.ZipFile(archive) as package:
    for entry in package.infolist():
        if not (runtime / entry.filename).resolve().is_relative_to(runtime.resolve()):
            raise SystemExit('Caminho inválido no pacote MySQL.')
    package.extractall(runtime)
print('MySQL extraído e verificado.')
