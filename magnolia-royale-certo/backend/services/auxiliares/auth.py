"""Apoio compartilhado para autenticação, autorização e normalização."""
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


class AuthHelpers(BaseService):
    def validar_senha(self, password):
        if not isinstance(password, str) or not 8 <= len(password) <= 128:
            raise AppError('A senha deve ter entre 8 e 128 caracteres.')
        return password

    def entrar_sessao(self, user):
        csrf = session.get('csrf', secrets.token_urlsafe(32))
        session.clear()
        session.update(user_id=user.id, version=user.session_version, csrf=csrf)
