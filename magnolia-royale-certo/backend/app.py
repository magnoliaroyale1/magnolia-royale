from pathlib import Path
import secrets
from flask import Flask, jsonify, request, session, send_from_directory
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.exceptions import HTTPException
from backend.config import Config
from backend.database import db
from backend.errors import AppError
from backend.routes import registrar_rotas


def create_app(test_config=None):
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    if not app.config['SECRET_KEY'] or not app.config['SQLALCHEMY_DATABASE_URI'].startswith('mysql+pymysql://'):
        raise RuntimeError('Configure SECRET_KEY e DATABASE_URL para MySQL em backend/.env.')
    db.init_app(app)
    registrar_rotas(app)
    app.config['UPLOAD_DIR'].mkdir(parents=True, exist_ok=True)
    app.config['MAILBOX_DIR'].mkdir(parents=True, exist_ok=True)

    @app.before_request
    def proteger_requisicao():
        if request.path.startswith('/api/') and request.method not in ('GET', 'HEAD', 'OPTIONS'):
            expected = session.get('csrf', '')
            supplied = request.headers.get('X-CSRF-Token', '')
            if not expected or not secrets.compare_digest(expected, supplied):
                raise AppError('Sessão expirada. Atualize a página e tente novamente.', 403)

    @app.after_request
    def cabecalhos(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'same-origin'
        if request.path.startswith('/api/'):
            response.headers['Cache-Control'] = 'no-store'
        return response

    @app.errorhandler(AppError)
    def erro_negocio(error):
        db.session.rollback()
        return jsonify({'error': error.message}), error.status

    @app.errorhandler(IntegrityError)
    def erro_integridade(error):
        db.session.rollback()
        return jsonify({'error': 'Os dados conflitam com um registro existente ou com um vínculo obrigatório.'}), 409

    @app.errorhandler(SQLAlchemyError)
    def erro_banco(error):
        db.session.rollback()
        app.logger.exception('Falha no banco de dados')
        return jsonify({'error': 'Não foi possível concluir a operação no banco. Tente novamente.'}), 503

    @app.errorhandler(HTTPException)
    def erro_http(error):
        return jsonify({'error': 'Requisição inválida.' if error.code != 404 else 'Rota não encontrada.'}), error.code

    @app.get('/api/health')
    def health():
        version = db.session.execute(text('SELECT VERSION()')).scalar()
        return jsonify({'status': 'ok', 'database': 'mysql', 'version': version})

    @app.get('/')
    @app.get('/<path:path>')
    def frontend(path=''):
        if path.startswith('api/'):
            raise AppError('Rota não encontrada.', 404)
        directory = Path(__file__).resolve().parents[1] / 'frontend' / 'dist'
        if path and (directory / path).is_file():
            return send_from_directory(directory, path)
        if not (directory / 'index.html').exists():
            return 'Compile o frontend para abrir a aplicação.', 503
        return send_from_directory(directory, 'index.html')

    return app


if __name__ == '__main__':
    from waitress import serve
    print('Magnolia Royale: http://127.0.0.1:5000', flush=True)
    serve(create_app(), host='127.0.0.1', port=5000, threads=8)
