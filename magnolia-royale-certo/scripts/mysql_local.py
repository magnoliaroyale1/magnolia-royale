"""Inicializa uma instância MySQL isolada, vinculada apenas a 127.0.0.1."""
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import time
import pymysql

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.runtime'
RUNTIME.mkdir(exist_ok=True)
config_path = RUNTIME / 'mysql-local.json'
if config_path.exists():
    config = json.loads(config_path.read_text())
else:
    config = {'port': 3307, 'root_password': secrets.token_urlsafe(30), 'password': secrets.token_urlsafe(30)}
    config_path.write_text(json.dumps(config), encoding='utf-8')
port = config['port']
binary = next(RUNTIME.glob('mysql-*-winx64/bin/mysqld.exe'), None)
if not binary:
    raise SystemExit('Extraia o ZIP oficial MySQL 8.4 para .runtime/ antes de iniciar.')
data = RUNTIME / 'mysql-data'
args = [str(binary), '--no-defaults', f'--basedir={binary.parents[1]}', f'--datadir={data}']
flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
if not (data / 'mysql').exists():
    data.mkdir(exist_ok=True)
    subprocess.run(args + ['--initialize-insecure'], check=True, creationflags=flags)
try:
    conn = pymysql.connect(host='127.0.0.1', port=port, user='root', password=config['root_password'], connect_timeout=2)
except pymysql.MySQLError:
    with socket.socket() as probe:
        if probe.connect_ex(('127.0.0.1', port)) != 0:
            log = open(RUNTIME / 'mysql-process.log', 'ab')
            process = subprocess.Popen(args + [f'--port={port}', '--bind-address=127.0.0.1', '--mysqlx=0', '--skip-log-bin', '--max-connections=50'],
                stdout=log, stderr=log, creationflags=flags)
            (RUNTIME / 'mysql.pid').write_text(str(process.pid))
    conn = None
    for attempt in range(40):
        for password in (config['root_password'], ''):
            try:
                conn = pymysql.connect(host='127.0.0.1', port=port, user='root', password=password, connect_timeout=1)
                break
            except pymysql.MySQLError:
                pass
        if conn:
            break
        time.sleep(0.5)
    if not conn:
        raise SystemExit('MySQL não iniciou. Consulte .runtime/mysql-process.log.')
with conn:
    with conn.cursor() as cursor:
        cursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED BY %s", (config['root_password'],))
        for name in ('magnolia_royale', 'magnolia_royale_test'):
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {name} CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci')
        cursor.execute("CREATE USER IF NOT EXISTS 'magnolia'@'localhost' IDENTIFIED BY %s", (config['password'],))
        cursor.execute("GRANT ALL ON magnolia_royale.* TO 'magnolia'@'localhost'")
        cursor.execute("GRANT ALL ON magnolia_royale_test.* TO 'magnolia'@'localhost'")
    conn.commit()
env = ROOT / 'backend' / '.env'
if not env.exists():
    env.write_text(f"SECRET_KEY={secrets.token_urlsafe(48)}\nDATABASE_URL=mysql+pymysql://magnolia:{config['password']}@127.0.0.1:{port}/magnolia_royale?charset=utf8mb4\nTEST_DATABASE_URL=mysql+pymysql://magnolia:{config['password']}@127.0.0.1:{port}/magnolia_royale_test?charset=utf8mb4\nDEMO_MODE=1\nFRONTEND_URL=http://127.0.0.1:5000\n", encoding='utf-8')
print(f'MySQL disponível em 127.0.0.1:{port}. Credenciais salvas localmente, fora do pacote de entrega.')
