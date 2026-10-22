"""Caso de uso RedefinirSenhaService: uma ação pública, com validações e persistência nas Models/Repositories."""
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


class RedefinirSenhaService(AuthHelpers):
    def executar(self, data):
        purpose = 'reset'
        token_hash = hashlib.sha256(texto(data, 'token', 200).encode()).hexdigest()
        item = TokenConta.primeiro(token_hash=token_hash, purpose=purpose)
        if not item:
            raise AppError('Link inválido ou expirado.')
        item = TokenConta.buscar(item.id, bloquear=True)
        if item.used or item.expiresAt < agora():
            raise AppError('Link inválido ou expirado.')
        user = Usuario.buscar(item.userId)
        if purpose == 'verify':
            user.atualizar(emailVerified=True)
        else:
            user.atualizar(password_hash=generate_password_hash(self.validar_senha(data.get('password'))), session_version=user.session_version + 1)
        item.atualizar(used=True)
        return {'ok': True}
