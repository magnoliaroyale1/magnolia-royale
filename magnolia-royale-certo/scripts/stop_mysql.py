"""Encerra somente a instância portátil; não apaga os dados."""
import json
from pathlib import Path
import pymysql
root = Path(__file__).resolve().parents[1]
path = root / '.runtime/mysql-local.json'
if not path.exists():
    raise SystemExit('Nenhuma instância portátil configurada.')
config = json.loads(path.read_text())
try:
    conn = pymysql.connect(host='127.0.0.1', port=config['port'], user='root', password=config['root_password'], connect_timeout=3)
except pymysql.err.OperationalError as error:
    raise SystemExit(f'Não foi possível conectar à instância portátil (código {error.args[0]}).')
with conn.cursor() as cursor:
    cursor.execute('SELECT @@datadir')
    if Path(cursor.fetchone()[0]).resolve() != (root / '.runtime/mysql-data').resolve():
        raise SystemExit('O diretório de dados não pertence a este projeto. Nada foi encerrado.')
    cursor.execute('SHUTDOWN')
print('MySQL portátil encerrado. Dados preservados.')
