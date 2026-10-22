"""Caso de uso AlterarSenhaService: uma ação pública, com validações e persistência nas Models/Repositories."""
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


class AlterarSenhaService(AuthHelpers):
    def executar(self, data):
        user = self.usuario(verified=False)
        if not check_password_hash(user.password_hash, str(data.get('currentPassword', ''))):
            raise AppError('Senha atual incorreta.')
        user.atualizar(password_hash=generate_password_hash(self.validar_senha(data.get('newPassword'))), session_version=user.session_version + 1)
        session['version'] = user.session_version
        return {'ok': True}
