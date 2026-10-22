"""Caso de uso ConsultarCaixaDemoService: uma ação pública, com validações e persistência nas Models/Repositories."""
import hashlib
import json
import secrets
from datetime import timedelta
from flask import current_app, session
from werkzeug.security import generate_password_hash, check_password_hash
from backend.errors import AppError
from backend.models import Usuario, TokenConta, Agendamento, Profissional
from backend.models.usuario import agora
from backend.services.base import BaseService, texto, email

from backend.services.auxiliares.auth import AuthHelpers


class ConsultarCaixaDemoService(AuthHelpers):
    def executar(self):
        if not current_app.config['DEMO_MODE']:
            raise AppError('Recurso disponível somente no modo de demonstração.', 404)
        user = self.usuario(required=False, verified=False)
        result = []
        for path in current_app.config['MAILBOX_DIR'].glob('*.json'):
            message = json.loads(path.read_text(encoding='utf-8'))
            # A caixa local é exclusiva para dados fictícios, como Mailpit.
            if not user or user.role == 'admin' or message['to'] == user.email:
                result.append(message)
        return sorted(result, key=lambda m: m['createdAt'], reverse=True)[:50]
